import pytesseract
import pdf2image
import os
import re


poppler_path = '/usr/bin'
os.environ['PATH'] = f"{poppler_path}:{os.environ.get('PATH', '')}"

def extract_text(pdf_path, words_per_file=1000, language='ben'):
    """
    Robust PDF text extraction with OCR for Bishnupriya Manipuri language preservation.

    Args:
        pdf_path (str): Path to the PDF file
        words_per_file (int): Number of words per output text file
        language (str): Tesseract language code

    Returns:
        list: Paths of created text files
    """
    try:
        # Increase DPI for better OCR quality
        images = pdf2image.convert_from_path(pdf_path, dpi=300 , poppler_path=poppler_path)

        # Extract text from images using OCR
        full_text = ""
        for idx, image in enumerate(images, 1):
            try:
                # Extract text with Tesseract, specifying language
                page_text = pytesseract.image_to_string(image, lang=language)
                full_text += page_text + "\n"
                print(f"Successfully processed page {idx}")
            except Exception as page_error:
                print(f"Error processing page {idx}: {page_error}")

        # Advanced text cleaning
        full_text = re.sub(r'\s+', ' ', full_text)  # Remove extra whitespaces
        full_text = re.sub(r'[^\u0980-\u09FF\s]', '', full_text)  # Keep only Bengali script
        full_text = full_text.strip()

        # Split text into words
        words = full_text.split()

        # Get base filename without extension
        base_filename = os.path.splitext(os.path.basename(pdf_path))[0]

        # Create output files
        output_files = []
        for i in range(0, len(words), words_per_file):
            # Create filename with incremental number
            output_filename = f"{base_filename}_{i//words_per_file + 1}.txt"

            # Get slice of words for this file
            file_words = words[i:i+words_per_file]
            file_text = " ".join(file_words)

            # Write to file with extra care for encoding
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(file_text)

            output_files.append(output_filename)
            print(f"Created file: {output_filename}")

        return output_files

    except Exception as e:
        print(f"Comprehensive error details:")
        print(f"Error type: {type(e)}")
        print(f"Error message: {str(e)}")
        import traceback
        traceback.print_exc()
        return []
