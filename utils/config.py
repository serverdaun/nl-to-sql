import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "ecommerce.db"
SCHEMA_JSON_PAHT = "schema.json"
CHROMA_DIR = "chroma_store"
EMBEDDING_MODEL = "senstence_transformers/all-MiniLM-L6-v2"
HF_API_KEY = os.getenv("HF_API_KEY")
