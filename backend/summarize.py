import google.generativeai as genai
import os

def summarize_text(text):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "API key not found! Please set GEMINI_API_KEY."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro-vision")
        response = model.generate_content(text)
        return response.text if response else "Error generating summary"
    except Exception as e:
        return f"Summarization error: {str(e)}"
