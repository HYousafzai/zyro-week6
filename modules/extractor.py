import re

def classify_and_extract(text):
    """Rule-based or pattern-based entity extraction for documents."""
    text_lower = text.lower()
    
    # Simple classification logic
    if "invoice" in text_lower or "bill to" in text_lower:
        category = "Invoice"
    elif "cv" in text_lower or "resume" in text_lower or "experience" in text_lower:
        category = "Resume"
    elif "contract" in text_lower or "agreement" in text_lower:
        category = "Contract"
    else:
        category = "General Document"
        
    extracted_data = {}
    
    # Extract emails if present
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    if emails:
        extracted_data["email"] = emails[0]
        
    # Extract total amounts if invoice
    if category == "Invoice":
        amounts = re.findall(r"\b\d+\.\d{2}\b", text)
        if amounts:
            extracted_data["total_amount"] = amounts[-1]
            
    confidence = 0.85 if extracted_data else 0.60
    return category, extracted_data, confidence