# PDF Consolidator

This project provides a set of scripts to process PDF files, including splitting PDFs into smaller files and performing OCR (Optical Character Recognition) on them.

## Features

- **Split PDF**: Split a PDF file into multiple smaller files, each containing a specified number of pages.
- **OCR PDF**: Extract text from PDF files using OCR and save the extracted text to a file.

## Requirements

- Python 3.12.x
- PyMuPDF
- PyPDF2

## Installation

1. Double click on the `install.bat` file. this installs the required python modules.

## Usage

1. Run the script:
    ```sh
    python pdf-solutions.py
    ```

2. Follow the prompts to provide the input PDF file path and the number of pages per split.

3. Optionally, choose to perform OCR on the split PDF files.

## Output

The output files will be saved in the `output` directory. The structure of the output directory is as follows:

```
output/
└── SPLIT - <filename>/
    ├── split_1.pdf
    ├── split_2.pdf
    ├── ...
    └── ocr_output/
        ├── split_1.txt
        ├── split_2.txt
        ├── ...
```

## Logging

Logs are saved in the `logs` directory. Check the log files for detailed information about the processing tasks and any errors encountered.

## Notes

- Ensure that the input PDF files are not password-protected.
- The OCR functionality requires an internet connection.
- Large PDF files may take longer to process.

## License

PDF-Consolidator © 2025 by M R and H Y is licensed under CC BY-NC-ND 4.0. To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-nd/4.0/, or access the `LICENCE` file for a copy.

Link to Creators: https://github.com/Speedymr01, https://github.com/Haozheeyu
Link to this project: https://github.com/Speedymr01/pdf-consolidator
