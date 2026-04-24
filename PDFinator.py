"""
The PDFinator - A comprehensive PDF manipulation tool
Supports splitting, merging, page operations, text extraction, and decryption
"""

import os
import sys
from datetime import datetime
import logging

# Setup early logging to catch startup errors
LOGS_DIR = "./logs"
os.makedirs(LOGS_DIR, exist_ok=True)
log_filename = datetime.now().strftime("pdf_processing_%Y-%m-%d_%H-%M-%S.log")
log_path = os.path.join(LOGS_DIR, log_filename)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler(sys.stderr)
    ]
)

logger = logging.getLogger(__name__)

# Now import dependencies with error logging
try:
    import customtkinter as cctk
    from customtkinter import CTkToplevel, CTkInputDialog
except Exception as e:
    logger.error(f"Failed to import customtkinter: {e}")
    raise

try:
    from tkinter import messagebox
except Exception as e:
    logger.error(f"Failed to import tkinter: {e}")
    raise

try:
    import PyPDF2
except Exception as e:
    logger.error(f"Failed to import PyPDF2: {e}")
    raise

try:
    import fitz  # PyMuPDF for text extraction
except Exception as e:
    logger.error(f"Failed to import PyMuPDF (fitz): {e}")
    raise

INPUT_DIR = "./pdfs"

# Test pycryptodome availability
try:
    from Crypto.Cipher import AES
    CRYPTO_AVAILABLE = True
except ImportError:
    logger.warning("PyCryptodome not available - some encrypted PDFs may not work")
    CRYPTO_AVAILABLE = False

# Setup directories and logging
def setup_environment():
    """Initialize directories and logging configuration"""
    for directory in [INPUT_DIR, LOGS_DIR]:
        os.makedirs(directory, exist_ok=True)
    
    log_filename = datetime.now().strftime("pdf_processing_%Y-%m-%d_%H-%M-%S.log")
    log_path = os.path.join(LOGS_DIR, log_filename)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    
    if not CRYPTO_AVAILABLE:
        logging.warning("PyCryptodome not available - some encrypted PDFs may not work")
    
    return logging.getLogger(__name__)

logger = setup_environment()

# Utility Functions
def get_output_subdir(pdf_path):
    """Create and return output subdirectory for a PDF file"""
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    subdir = os.path.join(INPUT_DIR, base_name)
    os.makedirs(subdir, exist_ok=True)
    return subdir

def get_single_output_dir():
    """Return the main pdfs directory for single file outputs"""
    return INPUT_DIR

def get_base_name(file_path):
    """Extract base filename without extension"""
    return os.path.splitext(os.path.basename(file_path))[0]

def safe_file_operation(operation_func):
    """Decorator for safe file operations with error handling"""
    def wrapper(*args, **kwargs):
        try:
            return operation_func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {operation_func.__name__}: {e}", exc_info=True)
            return False
    return wrapper

# PDF Processing Functions
@safe_file_operation
def merge_pdfs(input1, input2, output_file=None):
    """Merge two PDF files"""
    logger.info(f"Merging: {os.path.basename(input1)} + {os.path.basename(input2)}")
    
    # Single output file - save to main pdfs directory
    output_dir = get_single_output_dir()
    if output_file is None:
        name1, name2 = get_base_name(input1), get_base_name(input2)
        output_file = os.path.join(output_dir, f"({name1})+({name2}).pdf")

    merger = PyPDF2.PdfMerger()
    for pdf in [input1, input2]:
        if os.path.exists(pdf):
            merger.append(pdf)
        else:
            logger.error(f"File not found: {pdf}")
            return False
    
    merger.write(output_file)
    merger.close()
    logger.info(f"Merge complete: {os.path.basename(output_file)}")
    return True

@safe_file_operation
def perform_multi_merge(pdf_list, output_file=None):
    """Merge multiple PDF files"""
    if len(pdf_list) < 2:
        return False
    
    output_dir = get_single_output_dir()
    if output_file is None:
        pdf_names = [get_base_name(pdf) for pdf in pdf_list]
        output_filename = "(" + ")+(".join(pdf_names) + ").pdf"
        output_file = os.path.join(output_dir, output_filename)

    logger.info(f"Starting multi-merge of {len(pdf_list)} PDFs")
    merger = PyPDF2.PdfMerger()
    
    for i, pdf_path in enumerate(pdf_list):
        if os.path.exists(pdf_path):
            logger.info(f"Adding PDF {i+1}/{len(pdf_list)}: {os.path.basename(pdf_path)}")
            merger.append(pdf_path)
        else:
            logger.error(f"File not found: {pdf_path}")
    
    merger.write(output_file)
    merger.close()
    logger.info(f"Multi-merge complete: {output_file}")
    return True

@safe_file_operation
def split_pdf(input_file):
    """Split PDF into individual pages"""
    if not os.path.exists(input_file):
        logger.error(f"File not found: {input_file}")
        return False
    
    reader = PyPDF2.PdfReader(input_file)
    # Multiple output files - use subdirectory
    output_dir = get_output_subdir(input_file)
    base_name = get_base_name(input_file)
    
    for i, page in enumerate(reader.pages):
        writer = PyPDF2.PdfWriter()
        writer.add_page(page)
        output_path = os.path.join(output_dir, f"{base_name} - Page {i+1}.pdf")
        
        with open(output_path, "wb") as output_pdf:
            writer.write(output_pdf)
    
    logger.info(f"Split complete: {len(reader.pages)} pages created")
    return True

@safe_file_operation
def delete_page(input_file, page_number, output_file=None):
    """Remove a specific page from PDF"""
    if not os.path.exists(input_file):
        logger.error(f"File not found: {input_file}")
        return False
    
    # Single output file - save to main pdfs directory
    output_dir = get_single_output_dir()
    if output_file is None:
        base_name = get_base_name(input_file)
        output_file = os.path.join(output_dir, f"{base_name} (Page {page_number} Removed).pdf")

    reader = PyPDF2.PdfReader(input_file)
    writer = PyPDF2.PdfWriter()
    
    for i, page in enumerate(reader.pages):
        if i != page_number - 1:  # Skip the page to delete
            writer.add_page(page)
    
    with open(output_file, "wb") as f:
        writer.write(f)
    
    logger.info(f"Page {page_number} deleted from {os.path.basename(input_file)}")
    return True

@safe_file_operation
def duplicate_page(input_file, page_number, output_file=None):
    """Duplicate a specific page in PDF"""
    if not os.path.exists(input_file):
        logger.error(f"File not found: {input_file}")
        return False
    
    # Single output file - save to main pdfs directory
    output_dir = get_single_output_dir()
    if output_file is None:
        base_name = get_base_name(input_file)
        output_file = os.path.join(output_dir, f"{base_name} (Page {page_number} Duplicated).pdf")

    reader = PyPDF2.PdfReader(input_file)
    writer = PyPDF2.PdfWriter()
    
    # Add pages up to and including the target page
    for i in range(page_number):
        writer.add_page(reader.pages[i])
    
    # Add duplicate of target page
    writer.add_page(reader.pages[page_number - 1])
    
    # Add remaining pages
    for i in range(page_number, len(reader.pages)):
        writer.add_page(reader.pages[i])
    
    with open(output_file, "wb") as f:
        writer.write(f)
    
    logger.info(f"Page {page_number} duplicated in {os.path.basename(input_file)}")
    return True

@safe_file_operation
def ocr_pdf(input_file, output_file=None):
    """Extract text from PDF using OCR"""
    if not os.path.exists(input_file):
        logger.error(f"File not found: {input_file}")
        return False
    
    # Single output file - save to main pdfs directory
    output_dir = get_single_output_dir()
    if output_file is None:
        base_name = get_base_name(input_file)
        output_file = os.path.join(output_dir, f"{base_name} - Text.txt")

    logger.info(f"Starting text extraction for {os.path.basename(input_file)}")
    
    doc = fitz.open(input_file)
    with open(output_file, "w", encoding="utf-8") as out_txt:
        for i, page in enumerate(doc):
            text = page.get_text()
            out_txt.write(f"--- Page {i+1} ---\n{text}\n\n")
    
    doc.close()
    logger.info(f"Text extraction complete: {os.path.basename(output_file)}")
    return True

def decrypt_pdf(input_file, password=None, output_file=None):
    """Remove encryption from PDF file"""
    if not os.path.exists(input_file):
        logger.error(f"File not found: {input_file}")
        return False
    
    if not CRYPTO_AVAILABLE:
        logger.error("PyCryptodome not available - cannot decrypt AES encrypted PDFs")
        return False
    
    try:
        # Single output file - save to main pdfs directory
        output_dir = get_single_output_dir()
        if output_file is None:
            base_name = get_base_name(input_file)
            output_file = os.path.join(output_dir, f"{base_name} (Unlocked).pdf")

        logger.info(f"Starting decryption for {os.path.basename(input_file)}")
        
        reader = PyPDF2.PdfReader(input_file)
        
        # Handle unencrypted PDFs
        if not reader.is_encrypted:
            logger.info("PDF is not encrypted")
            import shutil
            shutil.copy2(input_file, output_file)
            return True
        
        # Try common passwords
        common_passwords = ["", "password", "123456", "admin", "user", "pdf", "document"]
        if password:
            common_passwords.insert(0, password)
        
        # Attempt decryption
        for pwd in common_passwords:
            if reader.decrypt(pwd):
                logger.info(f"Decryption successful with password: {'(empty)' if pwd == '' else '***'}")
                break
        else:
            logger.error("Could not decrypt with available passwords")
            return False
        
        # Try PyMuPDF first (more reliable)
        return _decrypt_with_pymupdf(input_file, output_file, common_passwords) or \
               _decrypt_with_pypdf2(reader, output_file)
        
    except Exception as e:
        logger.error(f"Decryption failed: {e}", exc_info=True)
        return False

def _decrypt_with_pymupdf(input_file, output_file, passwords):
    """Decrypt using PyMuPDF (preferred method)"""
    try:
        doc = fitz.open(input_file)
        
        for pwd in passwords:
            if doc.authenticate(pwd):
                doc.save(output_file)
                doc.close()
                logger.info("Decryption successful using PyMuPDF")
                return True
        
        doc.close()
        return False
        
    except Exception as e:
        logger.warning(f"PyMuPDF decryption failed: {e}")
        return False

def _decrypt_with_pypdf2(reader, output_file):
    """Fallback decryption using PyPDF2"""
    try:
        writer = PyPDF2.PdfWriter()
        successful_pages = 0
        
        for i in range(len(reader.pages)):
            try:
                writer.add_page(reader.pages[i])
                successful_pages += 1
            except Exception as e:
                logger.warning(f"Failed to process page {i+1}: {e}")
        
        if successful_pages == 0:
            return False
        
        with open(output_file, "wb") as f:
            writer.write(f)
        
        logger.info(f"PyPDF2 decryption complete: {successful_pages} pages processed")
        return True
        
    except Exception as e:
        logger.error(f"PyPDF2 decryption failed: {e}")
        return False

@safe_file_operation
def rotate_pdf(input_file, rotation, output_file=None):
    """Rotate pages in PDF by 90, 180, or 270 degrees"""
    if not os.path.exists(input_file):
        logger.error(f"File not found: {input_file}")
        return False
    
    valid_rotations = {90, 180, 270}
    if rotation not in valid_rotations:
        logger.error(f"Invalid rotation: {rotation}. Must be 90, 180, or 270")
        return False
    
    output_dir = get_single_output_dir()
    if output_file is None:
        base_name = get_base_name(input_file)
        output_file = os.path.join(output_dir, f"{base_name} ({rotation}° Rotated).pdf")

    logger.info(f"Rotating {os.path.basename(input_file)} by {rotation}°")
    
    doc = fitz.open(input_file)
    for page in doc:
        page.set_rotation(page.rotation + rotation)
    
    doc.save(output_file)
    doc.close()
    logger.info(f"Rotation complete: {os.path.basename(output_file)}")
    return True

@safe_file_operation
def get_pdf_metadata(input_file):
    """Get metadata from PDF"""
    if not os.path.exists(input_file):
        logger.error(f"File not found: {input_file}")
        return None
    
    doc = fitz.open(input_file)
    metadata = doc.metadata
    doc.close()
    return metadata

@safe_file_operation
def set_pdf_metadata(input_file, metadata, output_file=None):
    """Set metadata for PDF"""
    if not os.path.exists(input_file):
        logger.error(f"File not found: {input_file}")
        return False
    
    output_dir = get_single_output_dir()
    if output_file is None:
        base_name = get_base_name(input_file)
        output_file = os.path.join(output_dir, f"{base_name} (Metadata Updated).pdf")

    logger.info(f"Updating metadata for {os.path.basename(input_file)}")
    
    doc = fitz.open(input_file)
    if metadata.get('title'):
        doc.set_metadata({'/Title': metadata['title']})
    if metadata.get('author'):
        doc.set_metadata({'/Author': metadata['author']})
    if metadata.get('subject'):
        doc.set_metadata({'/Subject': metadata['subject']})
    if metadata.get('creator'):
        doc.set_metadata({'/Creator': metadata['creator']})
    if metadata.get('producer'):
        doc.set_metadata({'/Producer': metadata['producer']})
    
    doc.save(output_file)
    doc.close()
    logger.info(f"Metadata update complete: {os.path.basename(output_file)}")
    return True

@safe_file_operation
def compress_pdf(input_file, compression_level=6, output_file=None):
    """Compress PDF to reduce file size"""
    if not os.path.exists(input_file):
        logger.error(f"File not found: {input_file}")
        return False
    
    if not 0 <= compression_level <= 9:
        compression_level = 6
    
    output_dir = get_single_output_dir()
    if output_file is None:
        base_name = get_base_name(input_file)
        output_file = os.path.join(output_dir, f"{base_name} (Compressed).pdf")

    logger.info(f"Compressing {os.path.basename(input_file)} (level {compression_level})")
    
    doc = fitz.open(input_file)
    doc.save(
        output_file,
        garbage=4,
        deflate=True,
        compression=compression_level,
        clean=True
    )
    doc.close()
    
    original_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(output_file)
    ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
    logger.info(f"Compression complete: {ratio:.1f}% size reduction")
    return True

class PDFToolGUI:
    """Main GUI application for PDF manipulation tools"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("The PDFinator")
        self.root.geometry("900x650")
        
        cctk.set_appearance_mode("dark")
        cctk.set_default_color_theme("blue")
        
        self.file_paths = {}
        self._setup_gui()
        self.refresh_file_list()
        self._bind_shortcuts()

    def _setup_gui(self):
        """Initialize the GUI components"""
        header_frame = cctk.CTkFrame(self.root)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = cctk.CTkLabel(
            header_frame,
            text="The PDFinator",
            font=cctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left", pady=10)
        
        main_frame = cctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.file_tree = cctk.CTkTextbox(main_frame, wrap="none", font=cctk.CTkFont(size=12))
        self.file_tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = cctk.CTkScrollbar(main_frame, command=self.file_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.file_tree.configure(yscrollcommand=scrollbar.set)
        
        self._create_button_panel(self.root)
        
        status_frame = cctk.CTkFrame(self.root)
        status_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.status_label = cctk.CTkLabel(
            status_frame,
            text="Ready",
            font=cctk.CTkFont(size=12)
        )
        self.status_label.pack(side="left", pady=10)

    def _create_button_panel(self, parent):
        """Create the button panel with all PDF operations"""
        button_frame = cctk.CTkFrame(parent)
        button_frame.pack(fill="x", padx=20, pady=10)

        buttons = [
            ("Split", self._split_pdf),
            ("Delete Page", self._delete_page),
            ("Duplicate Page", self._duplicate_page),
            ("Rotate", self._rotate_pdf),
            ("Merge", self._merge_pdfs),
            ("Text", self._extract_text),
            ("Decrypt", self._decrypt_pdf),
            ("Compress", self._compress_pdf),
            ("Metadata", self._edit_metadata),
            ("Refresh", self.refresh_file_list)
        ]

        for text, command in buttons:
            cctk.CTkButton(
                button_frame,
                text=text,
                command=command,
                width=100
            ).pack(side="left", padx=5, pady=10)

    def _bind_shortcuts(self):
        """Bind keyboard shortcuts"""
        self.root.bind('<Control-r>', lambda e: self.refresh_file_list())
        self.root.bind('<Control-s>', lambda e: self._split_pdf())
        self.root.bind('<Control-d>', lambda e: self._delete_page())
        self.root.bind('<Control-m>', lambda e: self._merge_pdfs())
        self.root.bind('<Control-t>', lambda e: self._extract_text())

    def refresh_file_list(self):
        """Refresh the file tree with current PDF files"""
        self.file_tree.delete("1.0", "end")
        self.file_paths = {}
        
        dir_structure = self._build_directory_structure()
        self._populate_display('', dir_structure, 0)
        
        self._set_status(f"Loaded {len(self.file_paths)} PDF(s)")

    def _build_directory_structure(self):
        """Build nested dictionary representing directory structure"""
        structure = {}
        
        for root, dirs, files in os.walk(INPUT_DIR):
            for file in files:
                if file.lower().endswith(".pdf"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, INPUT_DIR)
                    path_parts = rel_path.split(os.sep)
                    
                    current_dict = structure
                    for part in path_parts[:-1]:
                        if part not in current_dict:
                            current_dict[part] = {}
                        current_dict = current_dict[part]
                    
                    current_dict[path_parts[-1]] = full_path
        
        return structure

    def _populate_display(self, parent_id, structure, indent):
        """Recursively populate display from directory structure"""
        for name, content in sorted(structure.items()):
            prefix = "  " * indent
            if isinstance(content, dict):
                self.file_tree.insert("end", f"{prefix}📁 {name}/\n")
                self.file_tree.tag_add("folder", f"{end}-1l", f"{end}")
                self._populate_display(name, content, indent + 1)
            else:
                file_id = f"file_{len(self.file_paths)}"
                self.file_paths[file_id] = content
                self.file_tree.insert("end", f"{prefix}📄 {name}\n")
                end = self.file_tree.index("end")
                self.file_tree.tag_add("file", f"{end}-2l", f"{end}")

    def _get_selected_file(self):
        """Get the currently selected PDF file path"""
        try:
            cursor_pos = self.file_tree.index("insert")
            line_num = int(cursor_pos.split('.')[0])
            
            for file_id, path in self.file_paths.items():
                line_key = f"{line_num}.0"
                if self.file_tree.get(line_key, f"{line_key}+1c").strip():
                    return path
            
            messagebox.showerror("Error", "Please select a PDF file.")
            return None
        except Exception:
            messagebox.showerror("Error", "Please select a PDF file.")
            return None

    def _set_status(self, message):
        """Update status label"""
        self.status_label.configure(text=message)

    def _show_success_and_refresh(self, message):
        """Show success message and refresh file list"""
        messagebox.showinfo("Success", message)
        self.refresh_file_list()

    # PDF Operation Methods
    def _split_pdf(self):
        """Handle PDF splitting operation"""
        pdf_path = self._get_selected_file()
        if pdf_path and split_pdf(pdf_path):
            self._show_success_and_refresh("PDF split successfully.")

    def _delete_page(self):
        """Handle page deletion operation"""
        pdf_path = self._get_selected_file()
        if not pdf_path:
            return
        
        page_num = CTkInputDialog(title="Delete Page", text="Enter page number to delete:").get_input()
        if page_num:
            try:
                page_num = int(page_num)
                if delete_page(pdf_path, page_num):
                    self._show_success_and_refresh("Page deleted successfully.")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid page number.")

    def _duplicate_page(self):
        """Handle page duplication operation"""
        pdf_path = self._get_selected_file()
        if not pdf_path:
            return
        
        page_num = CTkInputDialog(title="Duplicate Page", text="Enter page number to duplicate:").get_input()
        if page_num:
            try:
                page_num = int(page_num)
                if duplicate_page(pdf_path, page_num):
                    self._show_success_and_refresh("Page duplicated successfully.")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid page number.")

    def _rotate_pdf(self):
        """Handle PDF rotation operation"""
        pdf_path = self._get_selected_file()
        if not pdf_path:
            return
        
        rotation = CTkInputDialog(
            title="Rotate PDF",
            text="Enter rotation angle (90, 180, or 270):"
        ).get_input()
        if rotation:
            try:
                rotation = int(rotation)
                if rotation in {90, 180, 270}:
                    if rotate_pdf(pdf_path, rotation):
                        self._show_success_and_refresh(f"PDF rotated {rotation}° successfully.")
                else:
                    messagebox.showerror("Error", "Please enter 90, 180, or 270.")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")

    def _extract_text(self):
        """Handle text extraction operation"""
        pdf_path = self._get_selected_file()
        if pdf_path and ocr_pdf(pdf_path):
            self._show_success_and_refresh("Text extraction complete.")

    def _decrypt_pdf(self):
        """Handle PDF decryption operation"""
        pdf_path = self._get_selected_file()
        if not pdf_path:
            return
        
        use_password = messagebox.askyesno(
            "Password", 
            "Do you want to provide a password?\n(Click 'No' to try common passwords automatically)"
        )
        
        password = None
        if use_password:
            password = CTkInputDialog(title="Password", text="Enter PDF password:").get_input()
            if password is None:
                return
        
        if decrypt_pdf(pdf_path, password):
            self._show_success_and_refresh("PDF decryption complete.")
        else:
            messagebox.showerror(
                "Error", 
                "Could not decrypt PDF. This may be due to:\n"
                "• Incorrect password\n"
                "• PDF not actually encrypted\n"
                "• Unsupported encryption method\n\n"
                "Check the logs for more details."
            )

    def _compress_pdf(self):
        """Handle PDF compression operation"""
        pdf_path = self._get_selected_file()
        if not pdf_path:
            return
        
        level = CTkInputDialog(
            title="Compress PDF",
            text="Enter compression level (0-9, default 6):"
        ).get_input()
        
        compression_level = 6
        if level:
            try:
                compression_level = int(level)
                if not 0 <= compression_level <= 9:
                    compression_level = 6
            except ValueError:
                pass
        
        if compress_pdf(pdf_path, compression_level):
            self._show_success_and_refresh("PDF compressed successfully.")

    def _edit_metadata(self):
        """Handle metadata editing operation"""
        pdf_path = self._get_selected_file()
        if not pdf_path:
            return
        
        metadata = get_pdf_metadata(pdf_path)
        if not metadata:
            messagebox.showerror("Error", "Could not read metadata.")
            return
        
        dialog = CTkToplevel(self.root)
        dialog.title("Edit Metadata")
        dialog.geometry("500x400")
        
        cctk.CTkLabel(dialog, text="Edit PDF Metadata", font=cctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        
        fields = ['title', 'author', 'subject', 'creator', 'producer']
        entries = {}
        
        for field in fields:
            frame = cctk.CTkFrame(dialog)
            frame.pack(fill="x", padx=20, pady=5)
            
            cctk.CTkLabel(frame, text=field.capitalize() + ":", width=80).pack(side="left", padx=5)
            
            entry = cctk.CTkEntry(frame)
            entry.pack(side="left", fill="x", expand=True, padx=5)
            
            value = metadata.get(field, '')
            if value:
                entry.insert(0, value)
            
            entries[field] = entry
        
        def save_metadata():
            new_metadata = {}
            for field, entry in entries.items():
                value = entry.get()
                if value:
                    new_metadata[field] = value
            
            if set_pdf_metadata(pdf_path, new_metadata):
                messagebox.showinfo("Success", "Metadata saved successfully.")
                dialog.destroy()
                self.refresh_file_list()
            else:
                messagebox.showerror("Error", "Could not save metadata.")
        
        cctk.CTkButton(dialog, text="Save", command=save_metadata).pack(pady=20)

    def _merge_pdfs(self):
        """Handle multi-PDF merge operation"""
        self._set_status("Select PDFs to merge...")
        
        dialog = CTkToplevel(self.root)
        dialog.title("Merge PDFs")
        dialog.geometry("600x450")
        
        cctk.CTkLabel(
            dialog,
            text="Select PDFs to Merge",
            font=cctk.CTkFont(size=18, weight="bold")
        ).pack(pady=20)
        
        selected_frame = cctk.CTkFrame(dialog)
        selected_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        selected_listbox = cctk.CTkTextbox(selected_frame, height=150)
        selected_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        selected_listbox.configure(state="disabled")
        
        available_frame = cctk.CTkFrame(dialog)
        available_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        cctk.CTkLabel(available_frame, text="Available PDFs:").pack(anchor='w', padx=10, pady=(10, 5))
        
        available_listbox = cctk.CTkTextbox(available_frame, height=150)
        available_listbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self._populate_available_pdfs(available_listbox)
        
        button_frame = cctk.CTkFrame(dialog)
        button_frame.pack(pady=20)
        
        selected_pdfs = []
        
        def add_to_selection():
            selection = available_listbox.index("insert")
            if selection:
                line = available_listbox.get(f"{selection}.0", f"{selection}.end")
                dir_struct = self._build_directory_structure()
                for path in self.file_paths.values():
                    if line.strip() in path:
                        selected_pdfs.append(path)
                        selected_listbox.configure(state="normal")
                        selected_listbox.insert("end", os.path.relpath(path, INPUT_DIR))
                        selected_listbox.configure(state="disabled")
                        break
        
        def do_merge():
            if len(selected_pdfs) < 2:
                messagebox.showerror("Error", "Select at least 2 PDFs.")
                return
            if perform_multi_merge(selected_pdfs):
                messagebox.showinfo("Success", f"Merged {len(selected_pdfs)} PDFs.")
                dialog.destroy()
                self.refresh_file_list()

        cctk.CTkButton(button_frame, text="Add", command=add_to_selection).pack(side="left", padx=5)
        cctk.CTkButton(button_frame, text="Merge", command=do_merge).pack(side="left", padx=5)
        cctk.CTkButton(button_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)

    def _populate_available_pdfs(self, listbox):
        dir_struct = self._build_directory_structure()
        def add_entries(structure):
            for name, content in sorted(structure.items()):
                if isinstance(content, dict):
                    add_entries(content)
                else:
                    rel = os.path.relpath(content, INPUT_DIR)
                    listbox.insert('end', rel)
        add_entries(dir_struct)

# Main Application Entry Point
def main():
    """Initialize and run the PDFinator application"""
    root = cctk.CTk()
    app = PDFToolGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()