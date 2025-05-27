# PDF Processing Folder

This folder is designated for storing PDF files that you want to process with the PDF Consolidator tool.

## Usage

1. Place the PDF files you want to process into this folder.
2. Make sure the files are valid, non-password-protected PDF documents.
3. Start the tool (`manipulator.py`) and use the GUI to select and process the PDFs as needed.

## Notes

- Only PDF files (`.pdf`) in this folder will be shown in the tool for processing.
- The tool does not process password-protected or corrupted PDFs.
- All results (split pages, merged files, deleted/duplicated pages, OCR text) will be saved in the `output` directory, organized by the original PDF's name.
- You can add or remove PDFs from this folder at any time; use the "Refresh" button in the GUI to update the file list.
