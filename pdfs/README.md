# PDF Input Directory

This folder is where you place PDF files for processing with The PDFinator tool.

## Usage

1. **Add PDFs**: Place PDF files you want to process into this folder
2. **Organize**: Create subdirectories to organize your PDFs (optional)
3. **Process**: Use The PDFinator GUI to select and process files
4. **Results**: Processed files appear in this same directory structure

## Supported Files

- **Extensions**: `.pdf` and `.PDF` (case-insensitive)
- **Encryption**: Encrypted PDFs supported with password or automatic decryption
- **Subdirectories**: PDFs in nested folders are automatically detected
- **File Types**: Standard PDF documents, forms, and scanned documents

## Output Organization

### Single File Operations
Results are saved directly in the `pdfs/` folder:
- **Merged PDFs**: `(Document1)+(Document2).pdf`
- **Decrypted PDFs**: `Document (Unlocked).pdf`
- **Modified PDFs**: `Document (Page 3 Removed).pdf`
- **Text Files**: `Document - Text.txt`

### Multiple File Operations
Results are saved in subdirectories:
- **Split Pages**: `Document/Document - Page 1.pdf`, `Document - Page 2.pdf`, etc.

## Example Structure

```
pdfs/
├── report.pdf                    # Original file
├── (report)+(appendix).pdf       # Merged result
├── report (Unlocked).pdf         # Decrypted result
├── report - Text.txt             # Extracted text
├── report/                       # Split results
│   ├── report - Page 1.pdf
│   ├── report - Page 2.pdf
│   └── report - Page 3.pdf
├── archive/                      # Subdirectory
│   └── old-document.pdf
└── projects/
    ├── project1.pdf
    └── project2.pdf
```

## Tips

- **Refresh**: Click "Refresh" in the GUI after adding/removing files
- **Organization**: Use subdirectories to keep related PDFs together
- **Backup**: Keep backups of important original files
- **Naming**: Use descriptive filenames for easier identification

## File Processing

The PDFinator automatically:
- Scans this directory and all subdirectories
- Displays files in a visual tree structure
- Updates the file list when operations complete
- Handles both encrypted and unencrypted PDFs
- Preserves your original files (creates new processed versions)
