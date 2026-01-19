# The PDFinator

A comprehensive PDF manipulation tool with an intuitive graphical interface. The PDFinator provides powerful PDF processing capabilities including splitting, merging, page operations, text extraction, and decryption.

## Features

### Core PDF Operations
- **Split PDFs** - Break PDFs into individual pages
- **Merge PDFs** - Combine multiple PDFs in any order
- **Delete Pages** - Remove specific pages from PDFs
- **Duplicate Pages** - Copy pages within PDFs
- **Text Extraction (OCR)** - Extract text content from PDFs
- **Decrypt PDFs** - Remove password protection from encrypted PDFs

### User Interface
- **Visual Tree Structure** - Browse PDFs in an intuitive folder/file hierarchy
- **Drag-and-Drop Workflow** - Easy file selection and management
- **Multi-PDF Merge** - Select unlimited PDFs for merging in custom order
- **Real-time Updates** - File list refreshes automatically after operations

### Dependancies

- Python 3.12.x
- pypdf
- PyMuPDF
- pycryptodome


## Installation

### Prerequisites
- Python 3.7 or higher
- Windows, macOS, or Linux

### Quick Install
1. Clone or download this repository
2. Run the installation script:
   ```bash
   # Windows
   install.bat
   
   # macOS/Linux
   pip install -r requirements.txt
   ```

### Manual Installation
```bash
pip install pypdf PyMuPDF pycryptodome
```

## Usage

### Starting the Application
```bash
python PDFinator.py
```

### File Organization
Place your PDF files in the `pdfs/` directory. The application will automatically detect:
- PDFs in the main folder
- PDFs in subdirectories
- Both `.pdf` and `.PDF` extensions

### Operations

#### Splitting PDFs
1. Select a PDF from the tree
2. Click "Split"
3. Individual pages are saved to a subdirectory: `filename/filename - Page 1.pdf`

#### Merging PDFs
1. Select the first PDF
2. Click "Merge"
3. Choose additional PDFs in order
4. Click "Merge Now" when ready
5. Output: `(PDF1)+(PDF2)+(PDF3).pdf`

#### Page Operations
- **Delete Page**: Select PDF → "Delete Page" → Enter page number
  - Output: `filename (Page X Removed).pdf`
- **Duplicate Page**: Select PDF → "Duplicate Page" → Enter page number  
  - Output: `filename (Page X Duplicated).pdf`

#### Text Extraction
1. Select a PDF
2. Click "OCR"
3. Text is extracted and saved as: `filename - Text.txt`

#### Decryption
1. Select an encrypted PDF
2. Click "Decrypt"
3. Choose to provide password or try common passwords automatically
4. Output: `filename (Unlocked).pdf`

## File Naming Convention

The PDFinator uses intuitive naming for all output files:

| Operation | Output Format | Example |
|-----------|---------------|---------|
| Split | `filename - Page X.pdf` | `Report - Page 1.pdf` |
| Merge (2 PDFs) | `(name1)+(name2).pdf` | `(Report)+(Appendix).pdf` |
| Multi-merge | `(name1)+(name2)+(name3).pdf` | `(A)+(B)+(C).pdf` |
| Delete Page | `filename (Page X Removed).pdf` | `Report (Page 3 Removed).pdf` |
| Duplicate Page | `filename (Page X Duplicated).pdf` | `Report (Page 2 Duplicated).pdf` |
| Text Extraction | `filename - Text.txt` | `Report - Text.txt` |
| Decrypt | `filename (Unlocked).pdf` | `Report (Unlocked).pdf` |

## Directory Structure

```
PDFinator/
├── PDFinator.py          # Main application
├── requirements.txt      # Python dependencies
├── install.bat          # Windows installer
├── README.md            # This file
├── LICENCE              # License information
├── pdfs/                # Input PDF directory
│   ├── document.pdf     # Your PDF files
│   ├── merged_file.pdf  # Single-file outputs
│   └── document/        # Multi-file outputs (split pages)
├── logs/                # Application logs
└── output/              # Legacy output directory (unused)
```

## Output Organization

- **Single File Operations**: Save directly to `pdfs/` folder
  - Merge, Delete Page, Duplicate Page, Decrypt, OCR
- **Multiple File Operations**: Save to subdirectories in `pdfs/`
  - Split (creates multiple page files)

## Advanced Features

### Multi-PDF Merging
- Select unlimited PDFs in sequence
- Visual progress tracking shows selected files in order
- "Next" button to add more PDFs
- "Merge Now" button when ready

### Encryption Handling
- Automatic detection of encrypted PDFs
- Common password attempts: empty, "password", "123456", etc.
- Custom password input option
- Supports AES encryption with pycryptodome

### Error Handling
- Comprehensive logging to `logs/` directory
- User-friendly error messages
- Graceful handling of corrupted or inaccessible files
- Automatic recovery from partial failures

## Troubleshooting

### Common Issues

**"No module named 'Crypto'" Error**
```bash
pip uninstall crypto
pip install pycryptodome
```

**PDFs Not Appearing**
- Ensure PDFs are in the `pdfs/` directory
- Check file extensions (.pdf or .PDF)
- Click "Refresh" button

**Decryption Fails**
- Verify the PDF is actually encrypted
- Try providing the correct password
- Check logs for detailed error information

**Permission Errors**
- Ensure PDFs are not open in other applications
- Check file/folder permissions
- Run as administrator if necessary

## Dependencies

- **PyPDF2** - Core PDF manipulation
- **PyMuPDF (fitz)** - Text extraction and advanced PDF operations
- **pycryptodome** - Encryption/decryption support
- **tkinter** - GUI framework (included with Python)

## Logging

Logs are saved in the `logs` directory. Each run creates a log file named like:
```
logs/pdf_processing_manipulator_YYYY-MM-DD_HH-MM-SS.log
```
Check these logs for detailed information about processing tasks and any errors.

## Notes

- Ensure that input PDF files are not password-protected.
- Large PDF files may take longer to process.

## License

The PDFinator © 2025 by M R is licensed under CC BY-ND 4.0.
To view a copy of this license, visit https://creativecommons.org/licenses/by-nd/4.0/, or see the `LICENCE` file.

Creator: @Speedymr01 at [https://github.com/Speedymr01]
Project: [https://github.com/Speedymr01/The-PDF-inator]

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues, questions, or feature requests:
1. Check the troubleshooting section
2. Review the logs for error details
3. Create an issue with detailed information about your problem
