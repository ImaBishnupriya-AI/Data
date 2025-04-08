import pytesseract
import pdf2image
import os
import re
import traceback

poppler_path = '/usr/bin'
os.environ['PATH'] = f"{poppler_path}:{os.environ.get('PATH', '')}"

class Extract_Pdf :
  def __init__(self , pdf_path , language = 'ben'):
    self.pdf_path = pdf_path
    self.language = language

  def extract_text(self):
    """
    Robust PDF text extraction with OCR for Bishnupriya Manipuri language preservation.

    Args:
        pdf_path (str): Path to the PDF file
        language (str): Tesseract language code

    Returns:
        list: Paths of created text file
    """
    try:
        # Increase DPI for better OCR quality
        images = pdf2image.convert_from_path(self.pdf_path, dpi=300 , poppler_path=poppler_path)

        # Extract text from images using OCR
        full_text = ""
        for idx, image in enumerate(images, 1):
            try:
                # Extract text with Tesseract, specifying language
                page_text = pytesseract.image_to_string(image, lang=self.language)
                full_text += page_text + "\n"
                print(f"Successfully processed page {idx}")
                # print(full_text)
            except Exception as page_error:
                print(f"Error processing page {idx}: {page_error}")

        # Advanced text cleaning
        full_text = re.sub(r'\s+', ' ', full_text)  # Remove extra whitespaces
        #full_text = re.sub(r'[^\u0980-\u09FF\s]', '', full_text)  # Keep only Bengali script
        full_text = full_text.strip()

        # Get base filename without extension
        base_filename = os.path.splitext(os.path.basename(self.pdf_path))[0]

        # Create output files

        # Create filename with incremental number
        output_filename = f"{base_filename}.txt"


            # Write to file with extra care for encoding
        with open(output_filename, 'w', encoding='utf-8') as f:
              f.write(full_text)


        return output_filename

    except Exception as e:
        print(f"Comprehensive error details:")
        print(f"Error type: {type(e)}")
        print(f"Error message: {str(e)}")
        traceback.print_exc()
        return []
