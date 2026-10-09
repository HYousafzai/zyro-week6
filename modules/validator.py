def validate_document_data(category, data):
    """Check required fields and consistency rules."""
    errors = []
    anomalies = []
    
    if category == "Invoice":
        if "total_amount" not in data:
            errors.append("Missing required financial field: total_amount")
            
    if not data:
        anomalies.append("Low extraction confidence or empty structured attributes.")
        
    return errors, anomalies