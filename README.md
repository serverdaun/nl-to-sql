# NL-to-SQL Demo

A demo project that translates natural language analytics questions into SQL queries and executes them on a local SQLite database. It leverages LLMs, vector search, and schema-aware tools to generate and run safe, read-only SQL queries.

## Features

- Converts natural language questions into SQL queries.
- Uses a local SQLite database with a sample e-commerce schema and data.
- Employs vector search (ChromaDB + sentence-transformers) to retrieve relevant schema context.
- Integrates with HuggingFace LLMs via API for code generation.
- CLI interface for interactive querying.
- Ensures only safe, read-only SQL queries are executed.

## Project Structure

```
main.py                # Main entry point and CLI
requirements.txt       # Python dependencies
config/
  config.py            # Configuration and environment loading
  schema.json          # Database schema metadata
db/
  db_mockup.sql        # SQL to create and populate the demo DB
  ecommerce.db         # SQLite database (auto-generated)
chroma_store/          # ChromaDB vector index (auto-generated)
README.md
```

## Setup

1. **Clone the repository** and navigate to the project directory.
2. **Install dependencies** (preferably in a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables**:
   - Create a `.env` file in the project root.
   - Add your HuggingFace API key:
     ```
     HF_API_KEY=your_huggingface_api_key
     ```
4. **Run the demo**:
   ```bash
   python main.py
   ```
   The script will initialize the database and vector index if needed.

## Usage

- At the prompt, type a natural language analytics question (e.g., "Show all orders placed in March 2025").
- The system will display the answer or an error message.
- Press Enter on an empty line to exit.


## Notes

- The database and vector index are created automatically if missing.
- Only SELECT queries are allowed for safety.
- The schema and data are mockups for demonstration purposes.

---

Feel free to modify the schema, data, or models for your own use cases!
