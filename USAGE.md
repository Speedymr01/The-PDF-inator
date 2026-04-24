# The PDFinator - Detailed Usage Guide

This comprehensive guide covers all features and operations available in The PDFinator. The PDFinator uses a modern dark theme GUI built with customtkinter.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Interface Overview](#interface-overview)
3. [File Management](#file-management)
4. [PDF Operations](#pdf-operations)
5. [Keyboard Shortcuts](#keyboard-shortcuts)
6. [Advanced Features](#advanced-features)
7. [Troubleshooting](#troubleshooting)
8. [Tips and Best Practices](#tips-and-best-practices)

## Getting Started

### First Launch
1. **Start the application**: Run `python PDFinator.py`
2. **Add PDFs**: Place PDF files in the `pdfs/` directory
3. **Refresh**: Click "Refresh" to see your files in the tree view
4. **Select and Process**: Choose a PDF and click an operation button

### Directory Setup
```
PDFinator/
├── pdfs/                 # Place your PDF files here
│   ├── document.pdf      # Your input files
│   └── subfolder/        # Organize in folders (optional)
├── logs/                 # Automatic logging
└── PDFinator.py          # Run this file
```

## Interface Overview

### Main Window Components

The PDFinator features a modern dark-themed interface built with customtkinter.

#### File Tree View
- **📁 Folders**: Expandable directories containing PDFs
- **📄 PDF Files**: Individual PDF documents
- **Hierarchy**: Shows nested folder structure
- **Selection**: Click to select files for operations

#### Operation Buttons
- **Split**: Break PDF into individual pages
- **Delete Page**: Remove specific pages
- **Duplicate Page**: Copy pages within PDF
- **Rotate**: Rotate pages 90°, 180°, or 270°
- **Merge**: Combine multiple PDFs
- **Text**: Extract text content
- **Decrypt**: Remove password protection
- **Compress**: Reduce PDF file size
- **Metadata**: View and edit PDF metadata
- **Refresh**: Update file list

### Visual Indicators
- **Collapsed Folders**: `📁 folder [+]` - Click to expand
- **Expanded Folders**: `📁 folder [-]` - Click to collapse
- **PDF Files**: `📄 filename.pdf` - Ready for processing

## File Management

### Adding Files
1. **Direct Copy**: Copy PDFs to `pdfs/` directory
2. **Subfolders**: Create folders to organize related PDFs
3. **Refresh**: Click "Refresh" button to update the tree
4. **Auto-Detection**: Both `.pdf` and `.PDF` extensions supported

### File Organization
```
pdfs/
├── reports/
│   ├── monthly-report.pdf
│   └── annual-report.pdf
├── invoices/
│   ├── 2024/
│   │   └── invoice-001.pdf
│   └── 2025/
│       └── invoice-002.pdf
└── contracts/
    └── service-agreement.pdf
```

### Output Files
- **Single Operations**: Results appear in main `pdfs/` folder
- **Multiple Operations**: Results in subfolders (e.g., split pages)

## PDF Operations

### 1. Splitting PDFs

**Purpose**: Break a PDF into individual page files

**Steps**:
1. Select a PDF from the tree
2. Click "Split" button
3. Wait for processing to complete
4. Find pages in `pdfs/filename/` subfolder

**Output**:
```
pdfs/
├── document.pdf                    # Original
└── document/                       # Split results
    ├── document - Page 1.pdf
    ├── document - Page 2.pdf
    └── document - Page 3.pdf
```

**Use Cases**:
- Extract specific pages for sharing
- Create individual page files for editing
- Break large documents into manageable pieces

### 2. Merging PDFs

**Purpose**: Combine multiple PDFs into a single document

#### Simple Merge (2 PDFs)
1. Select first PDF
2. Click "Merge"
3. Choose second PDF from dialog
4. Click "Select"

#### Multi-PDF Merge (Unlimited)
1. Select first PDF
2. Click "Merge"
3. In dialog, select next PDF
4. Click "Next" to add more PDFs
5. Repeat steps 3-4 for additional PDFs
6. Click "Merge Now" when ready

**Output**: `(PDF1)+(PDF2)+(PDF3).pdf`

**Features**:
- **Order Control**: PDFs merge in selection order
- **Progress Tracking**: See selected files in merge dialog
- **Unlimited Files**: No limit on number of PDFs to merge
- **Visual Feedback**: Current selection displayed during process

### 3. Page Operations

#### Delete Page
**Purpose**: Remove specific pages from a PDF

**Steps**:
1. Select PDF
2. Click "Delete Page"
3. Enter page number to remove
4. Confirm operation

**Output**: `filename (Page X Removed).pdf`

#### Duplicate Page
**Purpose**: Create copies of specific pages within a PDF

**Steps**:
1. Select PDF
2. Click "Duplicate Page"
3. Enter page number to duplicate
4. Confirm operation

**Output**: `filename (Page X Duplicated).pdf`

**Note**: Duplicate page appears immediately after the original

### 4. Text Extraction

**Purpose**: Extract text content from PDFs

**Steps**:
1. Select PDF
2. Click "Text"
3. Wait for text extraction
4. Find text file in `pdfs/` folder

**Output**: `filename - Text.txt`

**Features**:
- **Page Separation**: Text organized by page numbers
- **UTF-8 Encoding**: Supports international characters
- **Formatted Output**: Clear page breaks and structure

**Sample Output**:
```
--- Page 1 ---
Document title and content from page 1...

--- Page 2 ---
Content from page 2...
```

### 5. PDF Decryption

**Purpose**: Remove password protection from encrypted PDFs

**Steps**:
1. Select encrypted PDF
2. Click "Decrypt"
3. Choose password option:
   - **Automatic**: Try common passwords
   - **Manual**: Enter specific password
4. Wait for decryption process

**Output**: `filename (Unlocked).pdf`

**Password Attempts**:
- Empty password (no password)
- "password"
- "123456"
- "admin"
- "user"
- "pdf"
- "document"

**Features**:
- **Dual Method**: PyMuPDF and PyPDF2 fallback
- **Error Recovery**: Handles partial decryption failures
- **Unencrypted Handling**: Copies unencrypted PDFs as-is

### 6. PDF Rotation

**Purpose**: Rotate pages in a PDF

**Steps**:
1. Select PDF
2. Click "Rotate"
3. Choose rotation angle (90°, 180°, or 270°)
4. Confirm operation

**Output**: `filename (90° Rotated).pdf`

**Features**:
- **Multiple Angles**: 90°, 180°, and 270° options
- **All Pages**: Rotates all pages in the PDF

### 7. PDF Compression

**Purpose**: Reduce PDF file size

**Steps**:
1. Select PDF
2. Click "Compress"
3. Choose compression level (0-9)
4. Wait for compression

**Output**: `filename (Compressed).pdf`

**compression Levels**:
- **0-3**: Lower compression, better quality
- **4-6**: Balanced (default)
- **7-9**: Higher compression, smaller file size

### 8. Metadata Editor

**Purpose**: View and edit PDF metadata

**Steps**:
1. Select PDF
2. Click "Metadata"
3. View current metadata
4. Edit desired fields
5. Save

**Fields**:
- **Title**: Document title
- **Author**: Document author
- **Subject**: Document subject
- **Creator**: Application that created the PDF
- **Producer**: Application that produced the PDF

**Output**: `filename (Metadata Updated).pdf`

### Keyboard Shortcuts

The PDFinator supports keyboard shortcuts for quick access:

| Shortcut | Action |
|----------|--------|
| Ctrl+R | Refresh file list |
| Ctrl+S | Split PDF |
| Ctrl+D | Delete Page |
| Ctrl+M | Merge PDFs |
| Ctrl+T | Extract Text |

## Advanced Features

### Multi-PDF Merge Workflow

The multi-PDF merge feature allows unlimited PDF combination:

1. **Initial Selection**: Choose first PDF from tree
2. **Sequential Addition**: Add PDFs one by one in desired order
3. **Visual Tracking**: See selected files and order in dialog
4. **Flexible Control**: Add more or merge current selection
5. **Order Preservation**: Final PDF follows selection sequence

**Dialog Features**:
- **Selected List**: Shows PDFs in merge order (numbered)
- **Available List**: Shows remaining PDFs to choose from
- **Next Button**: Add another PDF to selection
- **Merge Now Button**: Process current selection
- **Cancel Button**: Abort merge operation

### Encryption Support

The PDFinator handles various encryption types:

**Supported Formats**:
- Standard PDF encryption (RC4, AES-128, AES-256)
- User and owner passwords
- Various permission levels

**Decryption Process**:
1. **Detection**: Automatically identifies encrypted PDFs
2. **Password Testing**: Tries common passwords first
3. **User Input**: Prompts for specific password if needed
4. **Dual Processing**: Uses both PyMuPDF and PyPDF2
5. **Error Handling**: Graceful failure with detailed logging

### Error Recovery

**Automatic Recovery**:
- **Partial Failures**: Continues processing remaining pages
- **File Access**: Retries operations with different methods
- **Memory Issues**: Optimizes processing for large files
- **Corruption Handling**: Skips damaged pages when possible

**User Feedback**:
- **Progress Indicators**: Shows operation status
- **Error Messages**: Clear, actionable error descriptions
- **Log References**: Directs users to detailed logs
- **Recovery Suggestions**: Provides troubleshooting steps

## Troubleshooting

### Common Issues and Solutions

#### Files Not Appearing
**Problem**: PDFs don't show in tree view
**Solutions**:
- Ensure files are in `pdfs/` directory
- Check file extensions (.pdf or .PDF)
- Click "Refresh" button
- Verify file permissions

#### Decryption Failures
**Problem**: Cannot decrypt encrypted PDFs
**Solutions**:
- Verify PDF is actually encrypted
- Try manual password entry
- Check for unsupported encryption
- Review logs for detailed errors

#### Permission Errors
**Problem**: Cannot write output files
**Solutions**:
- Close PDFs in other applications
- Check folder write permissions
- Run as administrator (Windows)
- Verify disk space availability

#### Memory Issues
**Problem**: Large PDFs cause crashes
**Solutions**:
- Process smaller PDFs first
- Close other applications
- Increase system memory
- Split large PDFs before other operations

### Log Analysis

**Finding Logs**:
- Location: `logs/` directory
- Format: `pdf_processing_YYYY-MM-DD_HH-MM-SS.log`
- Content: Timestamped operation details

**Key Information**:
- **INFO**: Successful operations
- **WARNING**: Non-critical issues
- **ERROR**: Operation failures
- **File paths**: Exact locations of processed files

## Tips and Best Practices

### File Organization
- **Use Subfolders**: Organize related PDFs together
- **Descriptive Names**: Use clear, descriptive filenames
- **Backup Originals**: Keep copies of important documents
- **Regular Cleanup**: Remove unnecessary processed files

### Performance Optimization
- **Process Smaller Files First**: Test operations on small PDFs
- **Close Other Applications**: Free up system resources
- **Monitor Disk Space**: Ensure adequate storage for outputs
- **Regular Maintenance**: Clean up old logs and temporary files

### Security Considerations
- **Password Management**: Don't store passwords in plain text
- **File Permissions**: Set appropriate access controls
- **Sensitive Documents**: Use secure deletion for confidential files
- **Log Privacy**: Review logs before sharing for support

### Workflow Efficiency
- **Batch Operations**: Group similar operations together
- **Naming Conventions**: Use consistent naming patterns
- **Quality Checks**: Verify outputs before deleting originals
- **Documentation**: Keep notes on complex operations

### Advanced Usage
- **Scripting**: Automate repetitive tasks with batch files
- **Integration**: Combine with other PDF tools for complex workflows
- **Customization**: Modify code for specific organizational needs
- **Monitoring**: Use logs to track processing patterns and issues

## Getting Help

### Self-Help Resources
1. **Check Logs**: Review detailed operation logs
2. **Verify Setup**: Ensure proper installation and file placement
3. **Test Simple Operations**: Start with basic functions
4. **Review Documentation**: Consult README and usage guides

### Support Information
- **Error Details**: Include specific error messages
- **Log Excerpts**: Provide relevant log entries
- **System Information**: OS version, Python version, file details
- **Reproduction Steps**: Describe exact steps that cause issues

This comprehensive guide should help you make the most of The PDFinator's powerful PDF processing capabilities!