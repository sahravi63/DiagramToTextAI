from reportlab.pdfgen import canvas
from docx import Document
from pptx import Presentation
import os

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

def generate_pdf(text, filename="output.pdf"):
    path = os.path.join(output_dir, filename)
    c = canvas.Canvas(path)
    c.drawString(100, 750, text)
    c.save()
    return os.path.abspath(path)

def generate_docx(text, filename="output.docx"):
    path = os.path.join(output_dir, filename)
    doc = Document()
    doc.add_paragraph(text)
    doc.save(path)
    return os.path.abspath(path)

def generate_ppt(text, filename="output.pptx"):
    path = os.path.join(output_dir, filename)
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Summary"
    slide.shapes.placeholders[1].text = text
    prs.save(path)
    return os.path.abspath(path)
