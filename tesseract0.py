import argparse
import subprocess
import random
import string
import os

def extract_text(image_path, verbosity='no'):
    # Ensure the .dist/ folder exists
    dist_folder = os.path.join(os.path.dirname(__file__), '.dist')
    if not os.path.exists(dist_folder):
        os.makedirs(dist_folder)

    # Generate a random 16-character alphanumeric filename
    random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    output_file = os.path.abspath(os.path.join(dist_folder, random_name + '.txt'))

    # Run Tesseract OCR
    if verbosity == 'aggressive':
        print(f"Running Tesseract OCR on {image_path}")
    subprocess.run(['tesseract', image_path, output_file[:-4]])

    # Return the absolute path of the output file
    return output_file

if __name__ == '__main__':
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Extract text from image using Tesseract')
    parser.add_argument('image_path', nargs='?', help='Path to the image file')
    args = parser.parse_args()

    if args.image_path:
        # Extract text and print the output file path
        output_path = extract_text(args.image_path)
        print(output_path)
    else:
        print("No image path provided.")
