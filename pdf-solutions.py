import os
import logging
from datetime import datetime
from pypdf import PdfReader, PdfWriter
import fitz  # PyMuPDF for text extraction
import time

# Constants
LOG_DIR = 'logs'
PROCESSED_FILES_PATH = 'processed.txt'
SLEEP_INTERVAL = 10  # seconds
INPUT_DIR = './pdfs'
OUTPUT_DIR = './output'

# Configure logging with dynamic filename
log_filename = os.path.join(LOG_DIR, f'pdf_processing_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
os.makedirs(os.path.dirname(log_filename), exist_ok=True)
logging.basicConfig(filename=log_filename, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_processed_files():
    """Load the set of processed files from the processed.txt file."""
    if os.path.exists(PROCESSED_FILES_PATH):
        with open(PROCESSED_FILES_PATH, 'r') as file:
            return set(file.read().splitlines())
    return set()

def save_processed_file(filename):
    """Save a processed file name to the processed.txt file."""
    with open(PROCESSED_FILES_PATH, 'a') as file:
        file.write(filename + '\n')

def split_pdf(input_path, output_dir, pages_per_split):
    """
    Splits a PDF file into multiple files, each containing a specified number of pages.

    Args:
        input_path (str): Path to the input PDF file.
        output_dir (str): Directory to save the split PDF files.
        pages_per_split (int): Number of pages to include in each split file.

    Returns:
        int: Number of split files created.
    """
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"Splitting PDF: {input_path} into {pages_per_split}-page files.")

    reader = PdfReader(input_path)
    total_pages = len(reader.pages)

    start_page = 0
    file_number = 1
    splits = 0

    while start_page < total_pages:
        end_page = min(start_page + pages_per_split, total_pages)
        writer = PdfWriter()

        for i in range(start_page, end_page):
            writer.add_page(reader.pages[i])

        output_path = os.path.join(output_dir, f"split_{file_number}.pdf")
        with open(output_path, "wb") as output_file:
            writer.write(output_file)

        logging.info(f"Created split PDF: {output_path} with {end_page - start_page} pages")

        start_page = end_page
        file_number += 1
        splits += 1

    return splits

def ocr_pdf(pdf_path, output_path):
    """
    Extracts text from a PDF file using PyMuPDF.

    Args:
        pdf_path (str): Path to the input PDF file.
        output_path (str): Path to save the extracted text file.
    """
    try:
        # Open the PDF
        pdf_document = fitz.open(pdf_path)
        text = ""

        # Extract text from each page
        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            text += page.get_text() + "\n"

        # Save the extracted text to a file
        output_txt_file = output_path + ".txt"
        with open(output_txt_file, "w", encoding="utf-8") as f:
            f.write(text)
        logging.info(f"OCR completed for {pdf_path}. Output saved to {output_txt_file}")

    except (fitz.FileDataError, fitz.FileNotFoundError, fitz.PdfError) as e:
        logging.error(f"Error during OCR for {pdf_path}: {e}")

def process_pdf(input_pdf):
    """
    Process a PDF file by splitting it and performing OCR on the split files.

    Args:
        input_pdf (str): Path to the input PDF file.
    """
    try:
        # Get user input for the number of pages per split
        while True:
            try:
                pages_per_split = int(input(f"Enter the number of pages per split for {input_pdf}: "))
                if pages_per_split > 0:
                    break
                else:
                    print("Please enter a positive number of pages.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        logging.info(f"Pages per split for {input_pdf}: {pages_per_split}")

        # Extract the filename from the input path
        input_file_name = os.path.splitext(os.path.basename(input_pdf))[0]
        
        # Set the output directory to the ./output/ folder
        output_dir = os.path.join(OUTPUT_DIR, f"SPLIT - {input_file_name}")

        splits = split_pdf(input_pdf, output_dir, pages_per_split)
        logging.info(f"PDF split successfully! Files are located in: {output_dir}. There were {splits} files created.")

        # Ask if the user wants to perform OCR
        ocr_choice = input(f"Do you want to perform OCR on the split files for {input_pdf}? (y/n): ").lower()
        if ocr_choice == 'y':
            # Perform OCR on the split files
            ocr_output_dir = os.path.join(output_dir, "ocr_output")
            os.makedirs(ocr_output_dir, exist_ok=True)
            logging.info(f"OCR output will be saved in: {ocr_output_dir}")

            for filename in [f for f in os.listdir(output_dir) if f.endswith(".pdf") and f.startswith("split_")]:
                pdf_path = os.path.join(output_dir, filename)
                ocr_output_base = os.path.splitext(filename)[0]  # Remove .pdf extension
                output_txt_path = os.path.join(ocr_output_dir, ocr_output_base)  # Output path for OCR'd text, inside ocr_output dir

                ocr_pdf(pdf_path, output_txt_path)
            logging.info(f"OCR completed for all split files in {output_dir}. There are {splits} OCRs in total.")
    except Exception as e:
        logging.error(f"Error processing PDF {input_pdf}: {e}")

def monitor_directory(input_dir):
    """Monitor the input directory for new PDF files and process them if they haven't been processed."""
    processed_files = load_processed_files()

    while True:
        try:
            for filename in os.listdir(input_dir):
                if filename.endswith(".pdf") and filename not in processed_files:
                    input_pdf = os.path.join(input_dir, filename)
                    
                    # Read the PDF to get the number of pages
                    reader = PdfReader(input_pdf)
                    total_pages = len(reader.pages)
                    
                    logging.info(f"New file detected: {input_pdf} with {total_pages} pages")
                    process_pdf(input_pdf)
                    processed_files.add(filename)
                    save_processed_file(filename)
                    print(f"Processed {filename}")
                    logging.info(f"Processed {filename}")
        except Exception as e:
            logging.error(f"Error monitoring directory {input_dir}: {e}")

        time.sleep(SLEEP_INTERVAL)  # Check for new files every SLEEP_INTERVAL seconds

if __name__ == "__main__":
    logging.info(f"Input directory: {INPUT_DIR}")
    logging.info(f"Output directory: {OUTPUT_DIR}")

    monitor_directory(INPUT_DIR)
