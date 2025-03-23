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

# Ensure output directory exists
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Ensure temp directory exists
temp_dir = "temp"
os.makedirs(temp_dir, exist_ok=True)

@app.post("/process/")
async def process_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(temp_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = extract_text(file_path)
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text extracted from file.")

        summary = summarize_text(text)
        pdf_path = os.path.join(output_dir, "output.pdf")
        docx_path = os.path.join(output_dir, "output.docx")
        ppt_path = os.path.join(output_dir, "output.pptx")

        generate_pdf(summary, pdf_path)
        generate_docx(summary, docx_path)
        generate_ppt(summary, ppt_path)

        return {
            "summary": summary,
            "pdf": f"/download/{pdf_path}",
            "docx": f"/download/{docx_path}",
            "ppt": f"/download/{ppt_path}"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    
    finally:
        os.remove(file_path)  # Clean up temporary file after processing

@app.get("/download/{file_path:path}")
async def download_file(file_path: str):
    decoded_path = urllib.parse.unquote(file_path)  # Decode URL-encoded path
    if os.path.exists(decoded_path):
        return FileResponse(decoded_path, filename=os.path.basename(decoded_path))
    raise HTTPException(status_code=404, detail="File not found")