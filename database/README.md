# AI Document Intelligence & Workflow Platform

An end-to-end document intelligence and workflow automation system built with **Streamlit**, **FastAPI**, **SQLite**, and custom Python processing modules. Developed as part of the Zyroo AI/ML Internship program.

---

## **Features**

* **Document Processing & OCR:** Supports multi-format file ingestion (PDF, TXT, images) with automated text extraction and preprocessing.
* **Intelligent Search & RAG:** Contextual document retrieval and semantic querying engine to extract key information.
* **Validation & Security:** Built-in duplicate detection (SHA-256) and schema validation rules.
* **Workflow Automation:** Tracks multi-stage document lifecycle states from ingestion to validation and completion.
* **Interactive UI & API:** Real-time dashboards built in Streamlit backed by a FastAPI scoring and processing service.

---

## **Project Directory Structure**

```text
week6/
├── app.py                 # Master Streamlit UI application
├── requirements.txt       # Python project dependencies
├── .env.example           # Environment variable template
├── config/
│   └── settings.py        # Configuration and path loader
├── database/
│   └── db.py              # SQLite connection & schema initialization
├── modules/
│   ├── __init__.py        # Package initialization
│   ├── processor.py       # File handling & text extraction (OCR/pdfplumber)
│   ├── extractor.py       # Information extraction utilities
│   ├── rag.py             # Simple RAG document storage and search engine
│   ├── validator.py       # Document validation & integrity checks
│   └── workflow.py        # Workflow state tracking & lifecycle management
└── storage_files/         # Local storage directory for uploaded assets


Installation & Setup
Clone or Open Project Folder:
Open your terminal and navigate to your project directory:

Bash
cd path/to/week6
Create a Python Virtual Environment:

Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install Dependencies:

Bash
pip install -r requirements.txt
Configure Environment Variables:
Copy .env.example to .env and update any required settings.

Running the Application
Launch the interactive Streamlit application dashboard:

Bash
streamlit run app.py
Author
Hania Yousafzai

Zyroo AI/ML Internship Program