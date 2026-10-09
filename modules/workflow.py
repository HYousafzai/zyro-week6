from database.db import get_db_connection

def update_workflow_status(doc_id, status, actor="System"):
    """Update workflow decision and record audit history."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE documents SET status = ? WHERE id = ?", (status, doc_id))
    cursor.execute(
        "INSERT INTO audit_logs (document_id, action, actor) VALUES (?, ?, ?)",
        (doc_id, f"Status updated to {status}", actor)
    )
    
    conn.commit()
    conn.close()