import os
import fitz  # PyMuPDF
from PIL import Image
import tkinter as tk
from tkinter import filedialog

def extract_pages_as_images(pdf_path, output_folder):
    # Extract the base filename without extension
    base_filename = os.path.splitext(os.path.basename(pdf_path))[0]

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Loop through all the pages in the PDF
    for page_number in range(pdf_document.page_count):
        # Get the page object
        page = pdf_document.load_page(page_number)

        # Convert the page to an image
        image = page.get_pixmap()

        # Generate a unique image filename
        image_filename = f"{base_filename}_page_{page_number + 1}.png"
        unique_filename = image_filename
        counter = 1

        # Check if the filename already exists, if yes, append an increment
        while os.path.exists(os.path.join(output_folder, unique_filename)):
            unique_filename = f"{base_filename}_page_{page_number + 1}_{counter}.png"
            counter += 1

        # Save the image to the output folder
        image_path = os.path.join(output_folder, unique_filename)
        image.save(image_path)
        print(f"Page {page_number + 1} of {base_filename} saved as {unique_filename}")

    # Close the PDF document
    pdf_document.close()

def process_all_pdfs(input_folder, output_folder):
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                extract_pages_as_images(pdf_path, output_folder)

if __name__ == "__main__":
    # Create a Tkinter root window (it won't be shown)
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Prompt the user to select the input folder using a folder dialog
    input_folder = filedialog.askdirectory(title="Select Input Folder")
    if not input_folder:
        print("No input folder selected. Exiting.")
        exit()

    # Set the output folder where images will be saved
    output_folder = input_folder

    # Process all PDF files in the input folder and its subfolders
    process_all_pdfs(input_folder, output_folder)
