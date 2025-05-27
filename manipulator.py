import PyPDF2
import os
import time
import logging
from datetime import datetime

INPUT_DIR = "./pdfs"
OUTPUT_DIR = "./output"
PROCESSED_FILE = "processed-manipulator.txt"

# Ensure output and logs directories exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("./logs", exist_ok=True)

# Setup logging with required filename format
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

def load_processed_files():
    if not os.path.exists(PROCESSED_FILE):
        logger.info("No processed file list found, starting fresh.")
        return set()
    with open(PROCESSED_FILE, "r") as f:
        processed = set(line.strip() for line in f)
    logger.info(f"Loaded {len(processed)} processed files.")
    return processed

def save_processed_file(filepath):
    with open(PROCESSED_FILE, "a") as f:
        f.write(filepath + "\n")
    logger.info(f"Marked as processed: {filepath}")

def merge_pdfs(input1, input2, output_file):
    logger.info(f"Attempting to merge: {input1} + {input2} -> {output_file}")
    merger = PyPDF2.PdfMerger()
    for pdf in [input1, input2]:
        if os.path.exists(pdf):
            merger.append(pdf)
            logger.info(f"Appended {pdf}")
        else:
            logger.error(f"File not found for merging: {pdf}")
    merger.write(output_file)
    logger.info(f"Merged PDFs into {output_file}")

def split_pdf(input_file):
    if not os.path.exists(input_file):
        logger.error(f"File not found for splitting: {input_file}")
        print(f"Error: File not found - {input_file}")
        return

    try:
        reader = PyPDF2.PdfReader(input_file)
        logger.info(f"Splitting {input_file} with {len(reader.pages)} pages.")
        for i in range(len(reader.pages)):
            writer = PyPDF2.PdfWriter()
            writer.add_page(reader.pages[i])
            split_output = os.path.join(
                OUTPUT_DIR,
                f"{os.path.basename(input_file).replace('.pdf', '')}_page_{i+1}.pdf"
            )
            with open(split_output, "wb") as output_pdf:
                writer.write(output_pdf)
            logger.info(f"Created split PDF: {split_output}")
        print("Split PDF into individual pages.")
        logger.info(f"Split complete for {input_file}")
    except Exception as e:
        logger.error(f"Error splitting {input_file}: {e}", exc_info=True)

def delete_page(input_file, page_number, output_file):
    if not os.path.exists(input_file):
        logger.error(f"File not found for deleting page: {input_file}")
        print(f"Error: File not found - {input_file}")
        return

    try:
        reader = PyPDF2.PdfReader(input_file)
        writer = PyPDF2.PdfWriter()
        for i in range(len(reader.pages)):
            if i != page_number - 1:
                writer.add_page(reader.pages[i])
        with open(output_file, "wb") as f:
            writer.write(f)
        print(f"Deleted page {page_number} and saved as {output_file}")
        logger.info(f"Deleted page {page_number} from {input_file}, saved as {output_file}")
    except Exception as e:
        logger.error(f"Error deleting page {page_number} from {input_file}: {e}", exc_info=True)

def duplicate_page(input_file, page_number, output_file):
    if not os.path.exists(input_file):
        logger.error(f"File not found for duplicating page: {input_file}")
        print(f"Error: File not found - {input_file}")
        return

    try:
        reader = PyPDF2.PdfReader(input_file)
        writer = PyPDF2.PdfWriter()
        writer.add_page(reader.pages[page_number - 1])
        writer.add_page(reader.pages[page_number - 1])
        with open(output_file, "wb") as f:
            writer.write(f)
        print(f"Duplicated page {page_number} and saved as {output_file}")
        logger.info(f"Duplicated page {page_number} from {input_file}, saved as {output_file}")
    except Exception as e:
        logger.error(f"Error duplicating page {page_number} from {input_file}: {e}", exc_info=True)

def handle_file(filepath):
    while True:
        logger.info(f"PDF detected: {filepath}")
        print(f"\nPDF detected: {filepath}")
        print("Choose an action:")
        print("1. Split PDF")
        print("2. Delete Page")
        print("3. Duplicate Page")
        print("4. Merge with another file in ./pdfs")
        print("5. Toggle processed status and return to menu")
        print("6. Skip")

        choice = input("Enter choice: ").strip()
        base_name = os.path.splitext(os.path.basename(filepath))[0]
        output_path = os.path.join(OUTPUT_DIR, base_name + "_modified.pdf")

        if choice == "1":
            logger.info(f"User chose to split PDF: {filepath}")
            split_pdf(filepath)
            break
        elif choice == "2":
            try:
                page = int(input("Enter page number to delete: "))
                logger.info(f"User chose to delete page {page} from {filepath}")
                delete_page(filepath, page, output_path)
            except Exception as e:
                logger.error(f"Invalid input for delete page: {e}")
            break
        elif choice == "3":
            try:
                page = int(input("Enter page number to duplicate: "))
                logger.info(f"User chose to duplicate page {page} from {filepath}")
                duplicate_page(filepath, page, output_path)
            except Exception as e:
                logger.error(f"Invalid input for duplicate page: {e}")
            break
        elif choice == "4":
            all_pdfs = [f for f in os.listdir(INPUT_DIR)
                        if f.endswith(".pdf") and f != os.path.basename(filepath)]
            if not all_pdfs:
                print("No other PDFs to merge with.")
                logger.info("No other PDFs found for merging.")
                continue
            for i, f in enumerate(all_pdfs, start=1):
                print(f"{i}. {f}")
            try:
                idx = int(input("Enter number: ")) - 1
                if 0 <= idx < len(all_pdfs):
                    merge_target = os.path.join(INPUT_DIR, all_pdfs[idx])
                    logger.info(f"User chose to merge {filepath} with {merge_target}")
                    merge_pdfs(filepath, merge_target, output_path)
            except Exception as e:
                logger.error(f"Invalid input for merge: {e}")
            break
        elif choice == "5":
            save_processed_file(filepath)
            print(f"{filepath} marked as processed.")
            logger.info(f"User marked {filepath} as processed.")
            continue
        else:
            print("Skipping.")
            logger.info(f"User skipped file: {filepath}")
            break

def main():
    logger.info("Monitoring PDF folder...")
    print("Monitoring PDF folder...")

    while True:
        seen = load_processed_files()  # Reload processed files each iteration
        found_new = False
        for filename in os.listdir(INPUT_DIR):
            if filename.endswith(".pdf"):
                full_path = os.path.join(INPUT_DIR, filename)
                if full_path not in seen:
                    logger.info(f"New PDF found: {full_path}")
                    handle_file(full_path)
                    save_processed_file(full_path)  # Mark as processed after handling
                    found_new = True
        if not found_new:
            logger.info("No new PDF files found.")
            print("No new PDF files found.")
        time.sleep(3)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}", exc_info=True)
