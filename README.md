# PDF Consolidator

This application is a desktop tool for processing PDF files, featuring both a graphical user interface (GUI) and a command-line interface (CLI). It allows users to split, merge, delete, and duplicate PDF pages, with all actions logged for traceability.

## Features

- **Split PDF**: Split a PDF file into individual pages.
- **Merge PDFs**: Merge two PDF files into one.
- **Delete Page**: Remove a specific page from a PDF.
- **Duplicate Page**: Duplicate a specific page in a PDF.
- **Processed File Tracking**: Keeps track of processed files to avoid duplicate work.
- **Logging**: All operations are logged in the `logs` directory with timestamped filenames.
- **GUI**: User-friendly interface for all PDF operations.
- **CLI Monitoring**: Automatically detects new PDFs in the `pdfs` folder and prompts for actions.

## Requirements

- Python 3.12.x
- PyPDF2
- Tkinter (usually included with Python)
- Pypdf
- Pymupdf (fitz)
- Frontend

## Installation

1. Double-click on the `install.bat` file to install the required Python modules.

## Usage

### GUI

1. Run the script:
    ```sh
    python PDFinator.py
    ```
2. Use the graphical interface to select and process PDF files in the `pdfs` directory.

## Output

Processed files are saved in the `output` directory, organized by the original PDF's name.

```
output/
└── <filename>/
    ├── <filename>_page_1.pdf
    ├── <filename>_page_2.pdf
    ├── <filename>_merged.pdf
    ├── <filename>_deleted.pdf
    └── <filename>_duplicated.pdf
```

## Logging

Logs are saved in the `logs` directory. Each run creates a log file named like:
```
logs/pdf_processing_manipulator_YYYY-MM-DD_HH-MM-SS.log
```
Check these logs for detailed information about processing tasks and any errors.

## Notes

- Ensure that input PDF files are not password-protected.
- Large PDF files may take longer to process.
- The OCR feature from previous versions is not included in the current tool. If you need OCR, see previous releases or request integration.

## License


The PDFinator  © 2025 by M R is licensed under CC BY-ND 4.0.
To view a copy of this license, visit https://creativecommons.org/licenses/by-nd/4.0/, or see the `LICENCE` file.

Creator: @Speedymr01 at [https://github.com/Speedymr01]
Project: [https://github.com/Speedymr01/The-PDF-inator]
