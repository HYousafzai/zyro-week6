import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORAGE_DIR = os.getenv("STORAGE_DIR", os.path.join(BASE_DIR, "storage_files"))
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'document_platform.db')}")

os.makedirs(STORAGE_DIR, exist_ok=True)