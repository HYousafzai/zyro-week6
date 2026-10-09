import os
import hashlib
import pdfplumber
import pytesseract
from PIL import Image
from config.settings import STORAGE_DIR

def compute_file_hash(file_bytes):
    """Generate SHA-256 hash for duplicate detection."""
    return hashlib.sha256(file_bytes).hexdigest()

def save_uploaded_file(uploaded_file):
    """Save file safely, avoiding directory traversal."""
    file_bytes = uploaded_file.read()
    file_hash = compute_file_hash(file_bytes)
    
    safe_filename = os.path.basename(uploaded_file.name)
    file_path = os.path.join(STORAGE_DIR, f"{file_hash}_{safe_filename}")
    
    with open(file_path, "wb") as f:
        f.write(file_bytes)
        
    return file_path, file_hash

def extract_text_from_file(file_path):
    """Extract text via PDFplumber or Fallback OCR."""
    text = ""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception:
            pass
            
    if not text.strip() and ext in [".pdf", ".png", ".jpg", ".jpeg"]:
        try:
            if ext == ".pdf":
                # Convert PDF page to image if needed or use pdfplumber images
                pass
            else:
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image)
        except Exception as e:
            text = f"OCR Error: {str(e)}"
            
    return text