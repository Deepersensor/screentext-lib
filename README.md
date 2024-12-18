# ScreenText Library

Welcome to the ScreenText Library! This project provides a powerful and flexible pipeline for extracting text from images and copying it to the clipboard. It leverages Tesseract OCR for text extraction and offers a modular, customizable, and efficient workflow.

## Features

- **Text Extraction**: Extract text from images using Tesseract OCR.
- **Clipboard Integration**: Copy extracted text directly to the clipboard.
- **Configurable**: Use a `config.json` file to set up paths and behaviors.
- **Daemon Mode**: Watch a directory for new images and process them automatically.
- **Run on Startup**: Optionally configure the script to run on system startup.
- **Verbosity Levels**: Control the output verbosity for detailed logging or silent operation.
- **Modular Design**: Use each component independently or as part of the pipeline.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/screentext-lib.git
    cd screentext-lib
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Install Tesseract OCR**:
    - **Ubuntu**:
        ```bash
        sudo apt-get install tesseract-ocr
        ```
    - **MacOS**:
        ```bash
        brew install tesseract
        ```
    - **Windows**:
        Download and install from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).

## Configuration

Create a `config.json` file in the project directory to customize the behavior:
