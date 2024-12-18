import argparse
import pyperclip

# Set up argument parsing
parser = argparse.ArgumentParser(description='Copy file content to clipboard')
parser.add_argument('file_path', nargs='?', help='Path to the file')
parser.add_argument('--verbosity', type=str, choices=['no', 'aggressive'], default='no', help='Verbosity level')
args = parser.parse_args()

def copy_file_content(file_path, verbosity='no'):
    # Read the file content
    with open(file_path, 'r') as file:
        content = file.read()
    if verbosity == 'aggressive':
        print(f"Copying content of {file_path} to clipboard.")
    # Copy the file content to the clipboard
    pyperclip.copy(content)

if __name__ == '__main__':
    if args.file_path:
        copy_file_content(args.file_path, args.verbosity)
    else:
        print("No file path provided.")
