import streamlit as st
import uuid
from database.db import init_db, get_db_connection
from modules.processor import save_uploaded_file, extract_text_from_file, compute_file_hash
from modules.extractor import classify_and_extract
from modules.validator import validate_document_data
from modules.rag import rag_engine
from modules.workflow import update_workflow_status

# Initialize DB
init_db()

st.set_page_config(page_title="AI Document Intelligence Platform", layout="wide")

st.title("📄 AI Document Intelligence & Workflow Platform")
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Upload & Process", "Workflow Dashboard", "AI Assistant (RAG)"])

if page == "Upload & Process":
    st.header("Document Upload & Pipeline Integration")
    uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg"])
    
    if uploaded_file and st.button("Run Pipeline"):
        with st.spinner("Processing document through pipeline..."):
            file_path, file_hash = save_uploaded_file(uploaded_file)
            
            # Duplicate check
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM documents WHERE file_hash = ?", (file_hash,))
            existing = cursor.fetchone()
            
            if existing:
                st.warning("⚠️ Duplicate document detected! Using existing record.")
                doc_id = existing["id"]
            else:
                doc_id = str(uuid.uuid4())[:8]
                text = extract_text_from_file(file_path)
                category, extracted_data, confidence = classify_and_extract(text)
                errors, anomalies = validate_document_data(category, extracted_data)
                
                status = "Manual Review" if errors or anomalies else "Approved"
                
                cursor.execute("""
                    INSERT INTO documents (id, filename, file_hash, file_type, category, status, extracted_data, confidence)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (doc_id, uploaded_file.name, file_hash, uploaded_file.type, category, status, str(extracted_data), confidence))
                conn.commit()
                
                rag_engine.add_document(doc_id, text)
                st.success(f"Successfully processed! Assigned Status: **{status}**")
                
            conn.close()

elif page == "Workflow Dashboard":
    st.header("Workflow Dashboard & Audit History")
    conn = get_db_connection()
    docs = conn.execute("SELECT * FROM documents").fetchall()
    conn.close()
    
    for doc in docs:
        with st.expander(f"[{doc['status']}] {doc['filename']} ({doc['category']})"):
            st.write(f"**ID:** {doc['id']}")
            st.write(f"**Confidence:** {doc['confidence']}")
            st.write(f"**Extracted Data:** {doc['extracted_data']}")
            
            col1, col2 = st.columns(2)
            if col1:
                if st.button(f"Approve {doc['id']}", key=f"app_{doc['id']}"):
                    update_workflow_status(doc['id'], "Approved", actor="Hania Yousafzai")
                    st.rerun()
            if col2:
                if st.button(f"Reject {doc['id']}", key=f"rej_{doc['id']}"):
                    update_workflow_status(doc['id'], "Rejected", actor="Hania Yousafzai")
                    st.rerun()

elif page == "AI Assistant (RAG)":
    st.header("Document Q&A Assistant")
    question = st.text_input("Ask a question about your uploaded documents:")
    if question:
        answer = rag_engine.query(question)
        st.info(f"**Answer:** {answer}")