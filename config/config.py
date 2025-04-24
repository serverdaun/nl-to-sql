import os
from dotenv import load_dotenv
import json

load_dotenv()

DB_PATH = "db/ecommerce.db"
SCHEMA_JSON_PATH = "config/schema.json"
CHROMA_DIR = "chroma_store"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-MiniLM-L6-v2"
HF_API_KEY = os.getenv("HF_API_KEY")

with open("db/db_mockup.sql", "r") as f:
    DDL_AND_DATA = f.read()

with open(SCHEMA_JSON_PATH, "r", encoding="utf-8") as f:
    SCHEMA_JSON = json.load(f)
