import paddleocr
import easyocr

def extract_text(image_path):
    try:
        # Try PaddleOCR first
        ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang="en")
        results = ocr.ocr(image_path)
        text = " ".join([line[1][0] for res in results for line in res]) if results else ""

        # If PaddleOCR fails, use EasyOCR
        if not text.strip():
            reader = easyocr.Reader(["en"])
            text = " ".join(reader.readtext(image_path, detail=0))

        return text
    except Exception as e:
        return f"OCR error: {str(e)}"
