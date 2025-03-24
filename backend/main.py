from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from ocr import extract_text
from summarize import summarize_text
from file_generator import generate_pdf, generate_docx, generate_ppt
import shutil
import os
import urllib.parse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Ensure necessary directories exist
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

temp_dir = "temp"
os.makedirs(temp_dir, exist_ok=True)

@app.post("/process/")
async def process_file(file: UploadFile = File(...)):
    file_path = os.path.join(temp_dir, file.filename)
    
    try:
        # Save uploaded file to temporary directory
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text from the image/PDF
        text = extract_text(file_path)
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text extracted from file.")

        # Summarize extracted text
        summary = summarize_text(text)

        # Generate output files
        pdf_path = generate_pdf(summary, "output.pdf")
        docx_path = generate_docx(summary, "output.docx")
        ppt_path = generate_ppt(summary, "output.pptx")

        return {
            "summary": summary,
            "pdf": pdf_path,
            "docx": docx_path,
            "ppt": ppt_path
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)  # Clean up temporary file

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(output_dir, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")
