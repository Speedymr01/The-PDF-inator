# Changelog

All notable changes to The PDFinator project will be documented in this file.

## [3.0.1] - 2026-02-28

### 📚 Documentation Update

This patch release focuses exclusively on documentation improvements and consistency fixes. No code changes were made.

#### Changed
- **README.md**: Updated directory structure to include all documentation files
  - Added USAGE.md, CHANGELOG.md, SECURITY.md to structure diagram
  - Added pdfs/README.md and logs/README.md references
  - Included .gitignore, .git/, and .github/ folders
  - Added example log file pattern in logs directory
- **Directory Structure**: Now accurately reflects all files in the project
- **Package Name**: Corrected manual installation command from `pypdf` to `pypdf2`

#### Fixed
- **Consistency**: All README files now 100% consistent with actual code implementation
- **File Naming**: Verified all documented naming patterns match code exactly
- **Log Format**: Confirmed log filename format matches code: `pdf_processing_YYYY-MM-DD_HH-MM-SS.log`
- **Dependencies**: Ensured all documentation references correct package names

#### Documentation
- **README.md**: Enhanced directory structure section with complete file listing
- **pdfs/README.md**: Verified consistency with output organization
- **logs/README.md**: Confirmed log format and examples match implementation
- **CHANGELOG.md**: Updated to v3.0.0 with comprehensive feature documentation

### 📝 Files Updated
- README.md (directory structure, package names)
- CHANGELOG.md (version history, feature documentation)
- All README files verified for consistency

### ✅ Verification
- All file naming conventions verified against code
- All directory paths verified against actual structure
- All dependencies verified against requirements.txt
- All log formats verified against logging configuration
- All features verified against implementation

## [3.0.0] - 2026-01-19

### 🎉 Major Release - Complete Architecture Overhaul

This release represents a complete rewrite of The PDFinator with significant improvements to code quality, user experience, and functionality.

#### Added
- **Visual Tree Interface**: Hierarchical folder/file tree view with expandable/collapsible folders
- **Visual Icons**: 📁 folder and 📄 file icons for intuitive navigation
- **Multi-PDF Merge**: Sequential selection of unlimited PDFs with visual progress tracking
- **PDF Decryption**: Comprehensive password removal with dual-method approach (PyMuPDF + PyPDF2)
- **Smart Output Organization**: Single files to main folder, multiple files to subdirectories
- **Subdirectory Support**: Automatic recursive detection of PDFs in nested folders
- **Case-Insensitive Extensions**: Support for both `.pdf` and `.PDF` files
- **Intuitive File Naming**: Descriptive output names that clearly indicate operations
  - Merge: `(Document1)+(Document2).pdf`
  - Split: `Document - Page 1.pdf`
  - Delete: `Document (Page 3 Removed).pdf`
  - Duplicate: `Document (Page 2 Duplicated).pdf`
  - Decrypt: `Document (Unlocked).pdf`
  - OCR: `Document - Text.txt`
- **Enhanced Merge Dialog**: 
  - "Next" button to add more PDFs
  - "Merge Now" button to process current selection
  - Visual list showing selected PDFs in order
  - Counter showing number of selected PDFs
- **Comprehensive Documentation**:
  - USAGE.md with detailed operation guides
  - Updated README.md with complete feature documentation
  - Enhanced pdfs/README.md with examples
  - Detailed logs/README.md with troubleshooting
- **Improved Installation**: Enhanced install.bat with error checking and user feedback

#### Enhanced
- **Code Architecture**: Complete refactor with clean separation of concerns
  - Modular function design
  - Decorator-based error handling
  - Private method naming conventions
  - Comprehensive docstrings
- **Error Handling**: 
  - Graceful recovery from partial failures
  - Detailed error messages with actionable suggestions
  - Automatic fallback methods for decryption
  - Safe file operation decorator
- **Logging System**:
  - Cleaner log filenames: `pdf_processing_YYYY-MM-DD_HH-MM-SS.log`
  - More descriptive log messages
  - Better error context and stack traces
  - Performance information tracking
- **Text Extraction (OCR)**: 
  - More reliable using PyMuPDF
  - Better page separation in output
  - UTF-8 encoding support
- **PDF Splitting**: 
  - Improved page handling
  - Better error recovery
  - Cleaner output organization
- **Page Operations**: 
  - More robust delete functionality
  - Improved duplicate page handling
  - Better validation and error messages
- **User Interface**:
  - Modern, intuitive design
  - Consistent button layout
  - Better visual feedback
  - Automatic file list refresh after operations
- **File Management**:
  - Automatic directory creation
  - Better path handling
  - Improved file existence checking

#### Changed
- **Output Structure**: 
  - Single file operations → main `pdfs/` folder
  - Multi-file operations (split) → subdirectories in `pdfs/`
  - Removed complex nested output directory structure
- **File Naming Convention**: Complete overhaul for clarity
  - Old: `filename_merged.pdf` → New: `(name1)+(name2).pdf`
  - Old: `filename_page_1.pdf` → New: `filename - Page 1.pdf`
  - Old: `filename_deleted.pdf` → New: `filename (Page X Removed).pdf`
  - Old: `filename_duplicated.pdf` → New: `filename (Page X Duplicated).pdf`
  - Old: `filename_decrypted.pdf` → New: `filename (Unlocked).pdf`
  - Old: `filename_ocr.txt` → New: `filename - Text.txt`
- **Dependencies**: 
  - Updated to PyPDF2 (from pypdf)
  - Confirmed PyMuPDF (fitz) for text extraction
  - Added pycryptodome for encryption support
- **Log Format**: 
  - Old: `pdf_processing_manipulator_YYYY-MM-DD_HH-MM-SS.log`
  - New: `pdf_processing_YYYY-MM-DD_HH-MM-SS.log`
- **GUI Framework**: Switched from Listbox to Treeview for hierarchical display
- **Merge Workflow**: From simple 2-PDF merge to unlimited sequential selection

#### Fixed
- **Encryption Handling**: 
  - Proper AES encryption support with pycryptodome
  - Dual-method decryption (PyMuPDF primary, PyPDF2 fallback)
  - Better password attempt logging
  - Graceful handling of unencrypted PDFs
- **Memory Management**: 
  - Optimized handling of large PDF files
  - Better resource cleanup
  - Reduced memory footprint
- **Error Recovery**: 
  - Graceful handling of corrupted files
  - Better permission error messages
  - Improved file access error handling
- **Cross-Platform Compatibility**: 
  - Better path handling for Windows/macOS/Linux
  - Consistent directory separators
  - Proper file encoding
- **Crypto Library Conflicts**: 
  - Resolved conflicts between crypto and pycryptodome
  - Better dependency checking
  - Clear error messages for missing dependencies

#### Technical Improvements
- **Code Quality**:
  - Comprehensive docstrings for all functions
  - Type hints where appropriate
  - Consistent naming conventions
  - Reduced code duplication
- **Error Handling**:
  - Decorator-based error handling pattern
  - Consistent error logging
  - Better exception context
- **Documentation**:
  - Complete inline comments
  - Function-level documentation
  - Module-level documentation
- **Modularity**:
  - Separated GUI logic from PDF operations
  - Utility functions for common operations
  - Helper functions for decryption methods
- **Performance**:
  - Optimized file operations
  - Better memory usage
  - Faster directory scanning
- **Testing**:
  - Better error handling for edge cases
  - Validation of user inputs
  - Graceful degradation

#### Removed
- **Complex Output Structure**: Eliminated nested subdirectories in separate output folder
- **Cryptic File Names**: Removed underscore-based naming scheme
- **CLI Monitoring**: Removed automatic file detection (GUI-only now)
- **Processed File Tracking**: Simplified to focus on GUI operations

### 🔧 Infrastructure
- **Installation**: Enhanced install.bat with Python version checking and better feedback
- **Documentation**: 
  - Complete README.md rewrite
  - New USAGE.md with detailed guides
  - Updated CHANGELOG.md with version history
  - Enhanced pdfs/README.md and logs/README.md
- **Requirements**: Updated dependencies for better compatibility
- **Directory Structure**: Cleaner organization with proper file separation
- **Git Configuration**: Added .gitignore and .github configuration

### 📝 Documentation
- **README.md**: Complete rewrite with current features and examples
- **USAGE.md**: New comprehensive usage guide with step-by-step instructions
- **CHANGELOG.md**: Detailed version history
- **pdfs/README.md**: Enhanced with examples and tips
- **logs/README.md**: Comprehensive logging documentation

## [2.0.0] - Previous Version

### Features (Legacy)
- Basic PDF splitting
- Simple PDF merging (2 files only)
- Page deletion and duplication
- Basic text extraction
- Simple GUI interface
- Output to separate directory structure
- Basic encryption support

### Limitations (Resolved in 3.0.0)
- Limited merge functionality (2 PDFs only)
- Complex output directory structure
- No subdirectory support
- Basic error handling
- Limited file naming options
- No visual tree interface
- Cryptic file naming conventions

## [1.0.0] - Initial Release

### Features (Original)
- Basic PDF splitting
- Simple PDF merging (2 files only)
- Page deletion and duplication
- Basic text extraction
- Simple GUI interface
- Output to separate directory structure

### Limitations (Resolved in Later Versions)
- No encryption support
- Limited merge functionality
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

## Migration Guide

### From 2.0.0 to 3.0.0

**Output Location Changes:**
- Single file operations now save to main `pdfs/` folder (not subdirectories)
- Only split operations create subdirectories

**File Naming Changes:**
- Update any scripts that depend on old naming conventions
- New names are more descriptive and human-readable

**Merge Workflow:**
- Can now merge unlimited PDFs (not just 2)
- Use sequential selection dialog

**Dependencies:**
- Ensure pycryptodome is installed (not just crypto)
- Update to PyPDF2 if using pypdf

**Directory Structure:**
- Output files now appear in `pdfs/` folder
- Legacy `output/` folder is no longer used