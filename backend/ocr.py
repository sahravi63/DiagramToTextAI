import pytesseract
import easyocr
import paddleocr
import cv2
from pdf2image import convert_from_path

def extract_text(image_path):
    try:
        ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang="en")
        results = ocr.ocr(image_path)
        text = " ".join([line[1][0] for res in results for line in res]) if results else ""

        if not text.strip():
            reader = easyocr.Reader(["en"])
            text = " ".join(reader.readtext(image_path, detail=0))

        return text
    except Exception as e:
        return f"OCR error: {str(e)}"
