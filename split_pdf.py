import os
from pypdf import PdfReader, PdfWriter

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