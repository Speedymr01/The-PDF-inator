import os
from pypdf import PdfReader, PdfWriter
import subprocess  # For running tesseract

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
    Performs OCR on a PDF file using Tesseract.

    Args:
        pdf_path (str): Path to the input PDF file.
        output_path (str): Path to save the OCRed PDF file (will be a text file).
    """
    try:
        # Use Tesseract to perform OCR.  Assumes tesseract is in your PATH.
        subprocess.run(["tesseract", pdf_path, output_path, "pdf"], check=True)
        print(f"OCR completed for {pdf_path}. Output saved to {output_path}.pdf")

    except subprocess.CalledProcessError as e:
        print(f"Error during OCR: {e}")
        print("Make sure Tesseract is installed and in your system's PATH.")
    except FileNotFoundError:
        print("Error: Tesseract is not found.  Please install it and ensure it's in your system's PATH.")

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
    print("PDF split successfully!")

    # Ask if the user wants to perform OCR
    ocr_choice = input("Do you want to perform OCR on the split files? (y/n): ").lower()
    if ocr_choice == 'y':
        for filename in os.listdir(output_dir):
            if filename.endswith(".pdf") and filename.startswith("split_"):
                pdf_path = os.path.join(output_dir, filename)
                output_base = os.path.splitext(filename)[0]  # Remove .pdf extension
                output_txt_path = os.path.join(output_dir, output_base) # Output path for OCR'd text

                ocr_pdf(pdf_path, output_txt_path)
                
