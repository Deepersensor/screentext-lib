#!/usr/bin/env python3.11
import argparse
import os
import subprocess
import sys
from tesseract0 import extract_text
from copy0 import copy_file_content
from setup0 import setup_environment, watch_screenshots

def ensure_venv():
    # Get the absolute path to the current directory
    base_dir = os.path.abspath(os.path.dirname(__file__))
    venv_dir = os.path.join(base_dir, '.venv')
    requirements_file = os.path.join(base_dir, 'requirements.txt')

    # Check if the virtual environment exists, if not, create it
    if not os.path.exists(venv_dir):
        subprocess.run(['python3.11', '-m', 'venv', venv_dir])

    # Activate the virtual environment
    activate_script = os.path.join(venv_dir, 'bin', 'activate')
    if os.name == 'nt':  # Windows
        activate_script = os.path.join(venv_dir, 'Scripts', 'activate.bat')
    elif os.name == 'posix':  # Unix/Linux/MacOS
        activate_script = os.path.join(venv_dir, 'bin', 'activate')

    # Ensure required packages are installed
    subprocess.run([os.path.join(venv_dir, 'bin', 'pip'), 'install', '-r', requirements_file])

def process_image(image_path, verbosity):
    # Extract text from the image
    if verbosity == 'aggressive':
        print(f"Processing image: {image_path}")
    output_file = extract_text(image_path, verbosity)
    if verbosity == 'aggressive':
        print(f"Extracted text saved to: {output_file}")
    # Copy the extracted text to the clipboard
    copy_file_content(output_file)
    if verbosity in ('normal', 'aggressive'):
        print("Text copied to clipboard.")

def main():
    # Ensure the virtual environment is set up
    ensure_venv()

    # Run setup
    config = setup_environment()
    
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Extract text from image and copy to clipboard')
    parser.add_argument('image_path', nargs='?', help='Path to the image file')
    parser.add_argument('--out', choices=['no', 'normal', 'aggressive'], default='no', help='Set output verbosity level')
    parser.add_argument('--screenshot_path', type=str, help='Override screenshot path from config')
    parser.add_argument('--watch_screenshot_path', action='store_true', help='Enable watching screenshot path')
    parser.add_argument('--no_watch_screenshot_path', action='store_true', help='Disable watching screenshot path')
    parser.add_argument('--run_on_startup', action='store_true', help='Enable run on startup')
    parser.add_argument('--no_run_on_startup', action='store_true', help='Disable run on startup')
    args = parser.parse_args()
    
    # Override configurations with CLI arguments
    if args.screenshot_path:
        config['screenshot_path'] = args.screenshot_path
    if args.watch_screenshot_path:
        config['watch_screenshot_path'] = True
    if args.no_watch_screenshot_path:
        config['watch_screenshot_path'] = False
    if args.run_on_startup:
        config['run_on_startup'] = True
    if args.no_run_on_startup:
        config['run_on_startup'] = False
    
    # Set output verbosity
    verbosity = args.out
    
    # Update environment with new configurations
    setup_environment(config)
    
    # Process image or watch screenshots
    if args.image_path:
        # Process the specified image
        process_image(args.image_path, verbosity)
    elif config.get('watch_screenshot_path') and config.get('screenshot_path'):
        # Watch the screenshot path for new images
        watch_screenshots(config.get('screenshot_path'), verbosity)
    else:
        # Run in daemon mode if watch_screenshot_path is True
        if config.get('watch_screenshot_path'):
            default_screenshot_path = config.get('screenshot_path', './screenshots')
            watch_screenshots(default_screenshot_path, verbosity)
        else:
            print("No image path provided and watch mode is not enabled. Exiting.")

if __name__ == '__main__':
    main()
