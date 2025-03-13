import os
import logging
from datetime import datetime
from pypdf import PdfReader, PdfWriter
import fitz  # PyMuPDF for text extraction

# Configure logging with dynamic filename
log_filename = f'logs/pdf_processing_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
os.makedirs(os.path.dirname(log_filename), exist_ok=True)
logging.basicConfig(filename=log_filename, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def split_pdf(input_path, output_dir, pages_per_split):
    """
    Splits a PDF file into multiple files, each containing a specified number of pages.

    Args:
        input_path (str): Path to the input PDF file.
        output_dir (str): Directory to save the split PDF files.
        pages_per_split (int): Number of pages to include in each split file.
    """
    os.makedirs(output_dir, exist_ok=True)

    reader = PdfReader(input_path)
    total_pages = len(reader.pages)

    start_page = 0
    file_number = 1

    while start_page < total_pages:
        end_page = min(start_page + pages_per_split, total_pages)
        writer = PdfWriter()

        for i in range(start_page, end_page):
            writer.add_page(reader.pages[i])

        output_path = os.path.join(output_dir, f"split_{file_number}.pdf")
        with open(output_path, "wb") as output_file:
            writer.write(output_file)

        logging.info(f"Created split PDF: {output_path}")

        start_page = end_page
        file_number += 1

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
        logging.error(f"Error during OCR: {e}")

if __name__ == "__main__":
    # Get user input for the PDF file
    input_pdf = input("Enter the path to the input PDF file: ")
    logging.info(f"Input PDF file: {input_pdf}")

    # Get user input for the number of pages per split
    while True:
        try:
            pages_per_split = int(input("Enter the number of pages per split: "))
            if pages_per_split > 0:
                break
            else:
                print("Please enter a positive number of pages.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    logging.info(f"Pages per split: {pages_per_split}")

    # Extract the filename from the input path
    input_file_name = os.path.splitext(os.path.basename(input_pdf))[0]
    
    # Set the output directory to the ./output/ folder
    output_dir = os.path.join(".", "output", f"SPLIT - {input_file_name}")

    split_pdf(input_pdf, output_dir, pages_per_split)
    print(f"PDF split successfully! Files are located in: {output_dir}")
    logging.info(f"PDF split successfully! Files are located in: {output_dir}")

    # Ask if the user wants to perform OCR
    ocr_choice = input("Do you want to perform OCR on the split files? (y/n): ").lower()
    if ocr_choice == 'y':
        ocr_output_dir = os.path.join(output_dir, "ocr_output")
        os.makedirs(ocr_output_dir, exist_ok=True)
        print(f"OCR output will be saved in: {ocr_output_dir}")
        logging.info(f"OCR output will be saved in: {ocr_output_dir}")

        for filename in [f for f in os.listdir(output_dir) if f.endswith(".pdf") and f.startswith("split_")]:
            pdf_path = os.path.join(output_dir, filename)
            ocr_output_base = os.path.splitext(filename)[0]  # Remove .pdf extension
            output_txt_path = os.path.join(ocr_output_dir, ocr_output_base)  # Output path for OCR'd text, inside ocr_output dir

            ocr_pdf(pdf_path, output_txt_path)
