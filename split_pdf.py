import os
from pypdf import PdfReader, PdfWriter
import fitz  # PyMuPDF for text extraction

def split_pdf(input_path, output_dir, pages_per_split):
    """
    Splits a PDF file into multiple files, each containing a specified number of pages.

    Args:
        input_path (str): Path to the input PDF file.
        output_dir (str): Directory to save the split PDF files.
        pages_per_split (int): Number of pages to include in each split file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

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
        with open(output_path + ".txt", "w", encoding="utf-8") as f:
            f.write(text)

        print(f"OCR completed for {pdf_path}. Output saved to {output_path}.txt")

    except Exception as e:
        print(f"Error during OCR: {e}")

if __name__ == "__main__":
    # Get user input for the PDF file
    input_pdf = input("Enter the path to the input PDF file: ")

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

    # Extract the filename from the input path
    file_name = os.path.splitext(os.path.basename(input_pdf))[0]
    
    # Set the output directory to the Downloads folder
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    output_dir = os.path.join(downloads_path, f"SPLIT - {file_name}")

    split_pdf(input_pdf, output_dir, pages_per_split)
    print(f"PDF split successfully! Files are located in: {output_dir}")

    # Ask if the user wants to perform OCR
    ocr_choice = input("Do you want to perform OCR on the split files? (y/n): ").lower()
    if ocr_choice == 'y':
        ocr_output_dir = os.path.join(output_dir, "ocr_output")
        if not os.path.exists(ocr_output_dir):
            os.makedirs(ocr_output_dir)
        print(f"OCR output will be saved in: {ocr_output_dir}")

        for filename in os.listdir(output_dir):
            if filename.endswith(".pdf") and filename.startswith("split_"):
                pdf_path = os.path.join(output_dir, filename)
                output_base = os.path.splitext(filename)[0]  # Remove .pdf extension
                output_txt_path = os.path.join(ocr_output_dir, output_base)  # Output path for OCR'd text, inside ocr_output dir

                ocr_pdf(pdf_path, output_txt_path)
