import PyPDF2
import os
import time
import logging
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog

import fitz  # PyMuPDF for text extraction

INPUT_DIR = "./pdfs"
OUTPUT_DIR = "./output"

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("./logs", exist_ok=True)

log_filename = datetime.now().strftime("pdf_processing_manipulator_%Y-%m-%d_%H-%M-%S.log")
log_path = os.path.join("./logs", log_filename)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_output_subdir(pdf_path):
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    subdir = os.path.join(OUTPUT_DIR, base_name)
    os.makedirs(subdir, exist_ok=True)
    return subdir

def merge_pdfs(input1, input2, output_file=None):
    logger.info(f"Attempting to merge: {input1} + {input2}")
    output_dir = get_output_subdir(input1)
    if output_file is None:
        output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input1))[0]}_merged.pdf")

    merger = PyPDF2.PdfMerger()
    for pdf in [input1, input2]:
        if os.path.exists(pdf):
            merger.append(pdf)
        else:
            logger.error(f"File not found for merging: {pdf}")
    merger.write(output_file)
    merger.close()
    logger.info(f"Merged PDFs into {output_file}")

def split_pdf(input_file):
    if not os.path.exists(input_file):
        return
    try:
        reader = PyPDF2.PdfReader(input_file)
        output_dir = get_output_subdir(input_file)
        for i in range(len(reader.pages)):
            writer = PyPDF2.PdfWriter()
            writer.add_page(reader.pages[i])
            split_output = os.path.join(
                output_dir,
                f"{os.path.splitext(os.path.basename(input_file))[0]}_page_{i+1}.pdf"
            )
            with open(split_output, "wb") as output_pdf:
                writer.write(output_pdf)
    except Exception as e:
        logger.error(f"Error splitting {input_file}: {e}", exc_info=True)

def delete_page(input_file, page_number, output_file=None):
    if not os.path.exists(input_file):
        return
    try:
        output_dir = get_output_subdir(input_file)
        if output_file is None:
            output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_file))[0]}_deleted.pdf")

        reader = PyPDF2.PdfReader(input_file)
        writer = PyPDF2.PdfWriter()
        for i in range(len(reader.pages)):
            if i != page_number - 1:
                writer.add_page(reader.pages[i])
        with open(output_file, "wb") as f:
            writer.write(f)
    except Exception as e:
        logger.error(f"Error deleting page {page_number} from {input_file}: {e}", exc_info=True)

def duplicate_page(input_file, page_number, output_file=None):
    if not os.path.exists(input_file):
        return
    try:
        output_dir = get_output_subdir(input_file)
        if output_file is None:
            output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_file))[0]}_duplicated.pdf")

        reader = PyPDF2.PdfReader(input_file)
        writer = PyPDF2.PdfWriter()
        
        # Add pages up to and including the page to duplicate
        for i in range(page_number):
            writer.add_page(reader.pages[i])
        
        # Add the duplicate of the specified page right after the original
        writer.add_page(reader.pages[page_number - 1])
        
        # Add remaining pages after the duplicated page
        for i in range(page_number, len(reader.pages)):
            writer.add_page(reader.pages[i])
            
        with open(output_file, "wb") as f:
            writer.write(f)
    except Exception as e:
        logger.error(f"Error duplicating page {page_number} from {input_file}: {e}", exc_info=True)

def ocr_pdf(input_file, output_file=None):
    """
    Extracts text from each page of the PDF using PyMuPDF and saves it as a .txt file.
    """
    if not os.path.exists(input_file):
        logger.error(f"File not found for OCR: {input_file}")
        return
    try:
        output_dir = get_output_subdir(input_file)
        if output_file is None:
            output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_file))[0]}_ocr.txt")

        logger.info(f"Starting OCR (text extraction) for {input_file}")
        doc = fitz.open(input_file)
        with open(output_file, "w", encoding="utf-8") as out_txt:
            for i, page in enumerate(doc):
                text = page.get_text()
                out_txt.write(f"--- Page {i+1} ---\n{text}\n\n")
                logger.info(f"OCR text extracted for page {i+1}")
        logger.info(f"OCR complete for {input_file}, saved as {output_file}")
    except Exception as e:
        logger.error(f"Error during OCR for {input_file}: {e}", exc_info=True)

class PDFToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("The PDFinator")
        self.file_list = []
        self.create_widgets()
        self.refresh_file_list()

    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.listbox = tk.Listbox(frame, height=10)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=5)

        ttk.Button(button_frame, text="Split", command=self.split_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Page", command=self.delete_page).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Duplicate Page", command=self.duplicate_page).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Merge", command=self.merge_pdfs).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="OCR", command=self.ocr_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_file_list).pack(side=tk.LEFT, padx=5)

    def refresh_file_list(self):
        self.file_list = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]
        self.listbox.delete(0, tk.END)
        for f in self.file_list:
            self.listbox.insert(tk.END, f)

    def get_selected_file(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "No file selected.")
            return None
        return os.path.join(INPUT_DIR, self.file_list[selection[0]])

    def split_pdf(self):
        pdf = self.get_selected_file()
        if pdf:
            split_pdf(pdf)
            messagebox.showinfo("Success", "PDF split successfully.")

    def delete_page(self):
        pdf = self.get_selected_file()
        if pdf:
            try:
                page = int(simpledialog.askstring("Delete Page", "Enter page number to delete:"))
                delete_page(pdf, page)
                messagebox.showinfo("Success", "Page deleted.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def duplicate_page(self):
        pdf = self.get_selected_file()
        if pdf:
            try:
                page = int(simpledialog.askstring("Duplicate Page", "Enter page number to duplicate:"))
                duplicate_page(pdf, page)
                messagebox.showinfo("Success", "Page duplicated.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def merge_pdfs(self):
        pdf1 = self.get_selected_file()
        if not pdf1:
            return
        
        # Get list of available PDFs excluding the currently selected one
        available_pdfs = [f for f in self.file_list if os.path.join(INPUT_DIR, f) != pdf1]
        
        if not available_pdfs:
            messagebox.showerror("Error", "No other PDFs available in the pdfs directory to merge with.")
            return
        
        # Create a selection dialog
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Select PDF to merge with")
        selection_window.geometry("400x300")
        
        tk.Label(selection_window, text="Select the second PDF to merge:").pack(pady=10)
        
        pdf_listbox = tk.Listbox(selection_window, height=10)
        pdf_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for pdf in available_pdfs:
            pdf_listbox.insert(tk.END, pdf)
        
        selected_pdf = [None]  # Use list to allow modification in nested function
        
        def on_select():
            selection = pdf_listbox.curselection()
            if not selection:
                messagebox.showerror("Error", "Please select a PDF to merge.")
                return
            selected_pdf[0] = os.path.join(INPUT_DIR, available_pdfs[selection[0]])
            selection_window.destroy()
        
        def on_cancel():
            selection_window.destroy()
        
        button_frame = tk.Frame(selection_window)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Select", command=on_select).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=on_cancel).pack(side=tk.LEFT, padx=5)
        
        # Wait for the selection window to close
        self.root.wait_window(selection_window)
        
        if selected_pdf[0]:
            merge_pdfs(pdf1, selected_pdf[0])
            messagebox.showinfo("Success", "PDFs merged.")

    def ocr_pdf(self):
        pdf = self.get_selected_file()
        if pdf:
            try:
                ocr_pdf(pdf)
                messagebox.showinfo("Success", "Text extraction complete. Text file saved in output folder.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToolGUI(root)
    root.mainloop()
