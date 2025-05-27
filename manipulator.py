import PyPDF2
import os
import time
import logging
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog

INPUT_DIR = "./pdfs"
OUTPUT_DIR = "./output"
PROCESSED_FILE = "processed-manipulator.txt"

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

def load_processed_files():
    if not os.path.exists(PROCESSED_FILE):
        return set()
    with open(PROCESSED_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_processed_file(filepath):
    with open(PROCESSED_FILE, "a") as f:
        f.write(filepath + "\n")

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
        for page in reader.pages:
            writer.add_page(page)
        writer.add_page(reader.pages[page_number - 1])
        with open(output_file, "wb") as f:
            writer.write(f)
    except Exception as e:
        logger.error(f"Error duplicating page {page_number} from {input_file}: {e}", exc_info=True)

class PDFToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Manipulator")
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
        pdf2_path = filedialog.askopenfilename(initialdir=INPUT_DIR, title="Select second PDF to merge", filetypes=[("PDF files", "*.pdf")])
        if not pdf2_path:
            return
        merge_pdfs(pdf1, pdf2_path)
        messagebox.showinfo("Success", "PDFs merged.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToolGUI(root)
    root.mainloop()
