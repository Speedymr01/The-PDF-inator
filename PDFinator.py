"""
The PDFinator - A comprehensive PDF manipulation tool
Supports splitting, merging, page operations, OCR, and decryption
"""

import os
import logging
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog

import PyPDF2
import fitz  # PyMuPDF for text extraction

# Constants
INPUT_DIR = "./pdfs"
OUTPUT_DIR = "./output"
LOGS_DIR = "./logs"

# Test pycryptodome availability
try:
    from Crypto.Cipher import AES
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

# Setup directories and logging
def setup_environment():
    """Initialize directories and logging configuration"""
    for directory in [INPUT_DIR, OUTPUT_DIR, LOGS_DIR]:
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

class PDFToolGUI:
    """Main GUI application for PDF manipulation tools"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("The PDFinator")
        self.file_paths = {}  # Maps tree item IDs to full file paths
        self._setup_gui()
        self.refresh_file_list()

    def _setup_gui(self):
        """Initialize the GUI components"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # File tree view
        self.tree = ttk.Treeview(main_frame, height=10)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.heading('#0', text='PDF Files', anchor='w')

        # Button panel
        self._create_button_panel(main_frame)

    def _create_button_panel(self, parent):
        """Create the button panel with all PDF operations"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=5)

        buttons = [
            ("Split", self._split_pdf),
            ("Delete Page", self._delete_page),
            ("Duplicate Page", self._duplicate_page),
            ("Merge", self._merge_pdfs),
            ("OCR", self._ocr_pdf),
            ("Decrypt", self._decrypt_pdf),
            ("Refresh", self.refresh_file_list)
        ]

        for text, command in buttons:
            ttk.Button(button_frame, text=text, command=command).pack(side=tk.LEFT, padx=5)

    def refresh_file_list(self):
        """Refresh the file tree with current PDF files"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.file_paths = {}
        dir_structure = self._build_directory_structure()
        self._populate_tree('', dir_structure)

    def _build_directory_structure(self):
        """Build nested dictionary representing directory structure"""
        structure = {}
        
        for root, dirs, files in os.walk(INPUT_DIR):
            for file in files:
                if file.lower().endswith(".pdf"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, INPUT_DIR)
                    path_parts = rel_path.split(os.sep)
                    
                    # Navigate to correct position in structure
                    current_dict = structure
                    for part in path_parts[:-1]:
                        if part not in current_dict:
                            current_dict[part] = {}
                        current_dict = current_dict[part]
                    
                    # Add file
                    current_dict[path_parts[-1]] = full_path
        
        return structure

    def _populate_tree(self, parent_id, structure):
        """Recursively populate tree view from directory structure"""
        for name, content in sorted(structure.items()):
            if isinstance(content, dict):
                # Directory
                folder_id = self.tree.insert(parent_id, 'end', text=f"📁 {name}", open=False)
                self._populate_tree(folder_id, content)
            else:
                # PDF file
                file_id = self.tree.insert(parent_id, 'end', text=f"📄 {name}")
                self.file_paths[file_id] = content

    def _get_selected_file(self):
        """Get the currently selected PDF file path"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Error", "No file selected.")
            return None
        
        selected_id = selection[0]
        if selected_id in self.file_paths:
            return self.file_paths[selected_id]
        else:
            messagebox.showerror("Error", "Please select a PDF file, not a folder.")
            return None

    def _get_page_number(self, operation):
        """Get page number from user input"""
        try:
            return int(simpledialog.askstring(operation, f"Enter page number to {operation.lower()}:"))
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Please enter a valid page number.")
            return None

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
        
        page_num = self._get_page_number("Delete Page")
        if page_num and delete_page(pdf_path, page_num):
            self._show_success_and_refresh("Page deleted successfully.")

    def _duplicate_page(self):
        """Handle page duplication operation"""
        pdf_path = self._get_selected_file()
        if not pdf_path:
            return
        
        page_num = self._get_page_number("Duplicate Page")
        if page_num and duplicate_page(pdf_path, page_num):
            self._show_success_and_refresh("Page duplicated successfully.")

    def _ocr_pdf(self):
        """Handle OCR text extraction operation"""
        pdf_path = self._get_selected_file()
        if pdf_path and ocr_pdf(pdf_path):
            self._show_success_and_refresh("Text extraction complete.")

    def _decrypt_pdf(self):
        """Handle PDF decryption operation"""
        pdf_path = self._get_selected_file()
        if not pdf_path:
            return
        
        # Get password from user
        use_password = messagebox.askyesno(
            "Password", 
            "Do you want to provide a password?\n(Click 'No' to try common passwords automatically)"
        )
        
        password = None
        if use_password:
            password = simpledialog.askstring("Password", "Enter PDF password:", show='*')
            if password is None:
                return
        
        # Attempt decryption
        if decrypt_pdf(pdf_path, password):
            self._show_success_and_refresh("PDF decryption complete.")
        else:
            messagebox.showerror(
                "Error", 
                "Could not decrypt PDF. This may be due to:\n"
                "• Incorrect password\n"
                "• PDF not actually encrypted\n"
                "• Unsupported encryption method\n"
                "• Missing dependencies\n\n"
                "Check the logs for more details."
            )

    def _merge_pdfs(self):
        """Handle multi-PDF merge operation"""
        first_pdf = self._get_selected_file()
        if not first_pdf:
            return
        
        selected_pdfs = [first_pdf]
        self._show_merge_selection(selected_pdfs)

    def _show_merge_selection(self, selected_pdfs):
        """Show PDF selection dialog for merging"""
        available_pdfs, available_paths = self._get_available_pdfs(selected_pdfs)
        
        if not available_pdfs:
            if len(selected_pdfs) >= 2:
                self._perform_multi_merge(selected_pdfs)
            else:
                messagebox.showerror("Error", "Need at least 2 PDFs to merge.")
            return

        # Create selection dialog
        dialog = self._create_merge_dialog(selected_pdfs, available_pdfs, available_paths)

    def _get_available_pdfs(self, excluded_paths):
        """Get list of available PDFs excluding already selected ones"""
        available_pdfs = []
        available_paths = []
        
        def collect_pdfs(parent_id=""):
            for item_id in self.tree.get_children(parent_id):
                if item_id in self.file_paths:
                    file_path = self.file_paths[item_id]
                    if file_path not in excluded_paths:
                        rel_path = os.path.relpath(file_path, INPUT_DIR)
                        available_pdfs.append(rel_path)
                        available_paths.append(file_path)
                else:
                    collect_pdfs(item_id)
        
        collect_pdfs()
        return available_pdfs, available_paths

    def _create_merge_dialog(self, selected_pdfs, available_pdfs, available_paths):
        """Create the merge selection dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Select PDF to merge ({len(selected_pdfs)} selected)")
        dialog.geometry("600x400")
        
        # Show currently selected PDFs
        self._add_selected_pdfs_display(dialog, selected_pdfs)
        
        # PDF selection listbox
        tk.Label(dialog, text="Select next PDF to add:", font=("Arial", 10)).pack(pady=(10,5))
        pdf_listbox = tk.Listbox(dialog, height=8)
        pdf_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for pdf in available_pdfs:
            pdf_listbox.insert(tk.END, pdf)
        
        # Buttons
        self._add_merge_dialog_buttons(dialog, selected_pdfs, pdf_listbox, available_paths)
        
        self.root.wait_window(dialog)

    def _add_selected_pdfs_display(self, dialog, selected_pdfs):
        """Add display of currently selected PDFs to dialog"""
        info_frame = tk.Frame(dialog)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(info_frame, text="Currently selected PDFs (in merge order):", 
                font=("Arial", 10, "bold")).pack(anchor='w')
        
        selected_listbox = tk.Listbox(info_frame, height=4)
        selected_listbox.pack(fill=tk.X, pady=5)
        
        for i, pdf_path in enumerate(selected_pdfs):
            rel_path = os.path.relpath(pdf_path, INPUT_DIR)
            selected_listbox.insert(tk.END, f"{i+1}. {rel_path}")

    def _add_merge_dialog_buttons(self, dialog, selected_pdfs, pdf_listbox, available_paths):
        """Add buttons to merge dialog"""
        def on_next():
            selection = pdf_listbox.curselection()
            if not selection:
                messagebox.showerror("Error", "Please select a PDF to add.")
                return
            
            new_pdf = available_paths[selection[0]]
            dialog.destroy()
            self._show_merge_selection(selected_pdfs + [new_pdf])

        def on_merge_now():
            if len(selected_pdfs) < 2:
                messagebox.showerror("Error", "Need at least 2 PDFs to merge.")
                return
            dialog.destroy()
            self._perform_multi_merge(selected_pdfs)

        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Next", command=on_next, 
                 bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text=f"Merge Now ({len(selected_pdfs)} PDFs)", 
                 command=on_merge_now, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", 
                 command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def _perform_multi_merge(self, pdf_list):
        """Perform the actual multi-PDF merge operation"""
        if len(pdf_list) < 2:
            messagebox.showerror("Error", "Need at least 2 PDFs to merge.")
            return
        
        try:
            # Single output file - save to main pdfs directory
            output_dir = get_single_output_dir()
            pdf_names = [get_base_name(pdf) for pdf in pdf_list]
            output_filename = "(" + ")+(".join(pdf_names) + ").pdf"
            output_file = os.path.join(output_dir, output_filename)
            
            # Perform merge
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
            
            # Show success message
            display_names = [os.path.basename(pdf) for pdf in pdf_list]
            message = f"Successfully merged {len(pdf_list)} PDFs:\n\n"
            message += "\n".join([f"{i+1}. {name}" for i, name in enumerate(display_names)])
            message += f"\n\nOutput: {output_filename}"
            
            messagebox.showinfo("Merge Complete", message)
            logger.info(f"Multi-merge complete: {output_file}")
            self.refresh_file_list()
            
        except Exception as e:
            logger.error(f"Multi-merge failed: {e}", exc_info=True)
            messagebox.showerror("Error", f"Failed to merge PDFs: {str(e)}")

# Main Application Entry Point
def main():
    """Initialize and run the PDFinator application"""
    root = tk.Tk()
    app = PDFToolGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()