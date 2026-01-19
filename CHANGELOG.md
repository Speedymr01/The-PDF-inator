# Changelog

All notable changes to The PDFinator project will be documented in this file.

## [2.0.0] - 2025-01-19

### 🎉 Major Release - Complete Rewrite

#### Added
- **Visual Tree Interface**: Replaced simple list with hierarchical folder/file tree view
- **Multi-PDF Merge**: Sequential selection of unlimited PDFs for merging
- **PDF Decryption**: Remove password protection with automatic and manual password attempts
- **Subdirectory Support**: Automatic detection of PDFs in nested folders
- **Case-Insensitive Extensions**: Support for both `.pdf` and `.PDF` files
- **Intuitive File Naming**: Descriptive output names that clearly indicate operations
- **Smart Output Organization**: Single files to main folder, multiple files to subdirectories
- **Enhanced Error Handling**: Comprehensive error recovery and user feedback
- **Improved Logging**: Detailed operation tracking with timestamps and context

#### Enhanced
- **Text Extraction (OCR)**: Improved reliability using PyMuPDF
- **PDF Splitting**: Better page handling and error recovery
- **Page Operations**: More robust delete and duplicate functionality
- **User Interface**: Modern, intuitive design with visual file icons
- **File Management**: Automatic refresh after operations

#### Changed
- **Output Structure**: 
  - Single file operations save to main `pdfs/` folder
  - Multi-file operations (split) use subdirectories
- **File Naming Convention**:
  - Merge: `(Document1)+(Document2).pdf`
  - Split: `Document - Page 1.pdf`
  - Delete: `Document (Page 3 Removed).pdf`
  - Duplicate: `Document (Page 2 Duplicated).pdf`
  - Decrypt: `Document (Unlocked).pdf`
  - OCR: `Document - Text.txt`
- **Dependencies**: Updated to use PyPDF2, PyMuPDF, and pycryptodome
- **Logging**: Renamed log files to `pdf_processing_YYYY-MM-DD_HH-MM-SS.log`

#### Fixed
- **Encryption Handling**: Proper support for AES-encrypted PDFs
- **Memory Management**: Better handling of large PDF files
- **Error Recovery**: Graceful handling of corrupted or inaccessible files
- **Cross-Platform**: Improved compatibility across Windows, macOS, and Linux

#### Technical Improvements
- **Code Architecture**: Complete refactor with clean separation of concerns
- **Error Handling**: Decorator-based error handling for consistent behavior
- **Documentation**: Comprehensive docstrings and inline comments
- **Modularity**: Separated GUI logic from PDF processing functions
- **Performance**: Optimized file operations and memory usage

### 🔧 Infrastructure
- **Installation**: Enhanced install.bat with better error checking
- **Documentation**: Complete rewrite of README.md and all documentation
- **Requirements**: Updated dependencies for better compatibility
- **Directory Structure**: Cleaner organization with proper separation

## [1.0.0] - Previous Version

### Features (Legacy)
- Basic PDF splitting
- Simple PDF merging (2 files only)
- Page deletion and duplication
- Basic text extraction
- Simple GUI interface
- Output to separate directory structure

### Limitations (Resolved in 2.0.0)
- No encryption support
- Limited merge functionality (2 PDFs only)
- Complex output directory structure
- No subdirectory support
- Basic error handling
- Limited file naming options

---

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes or major feature overhauls
- **MINOR**: New functionality in a backwards compatible manner
- **PATCH**: Backwards compatible bug fixes

## Categories

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Vulnerability fixes
- **Enhanced**: Improvements to existing features
- **Technical**: Internal improvements not visible to users