import json
import sqlite3
import pathlib
import rich
import chromadb
from typing import List, Tuple
from langchain_huggingface import HuggingFaceEmbeddings
from smolagents import CodeAgent, InferenceClientModel, tool, HfApiModel
from config.config import DB_PATH, DDL_AND_DATA, CHROMA_DIR, SCHEMA_JSON, HF_API_KEY


embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
llm = HfApiModel(api_key=HF_API_KEY)


def init_resources() -> None:
    if not pathlib.Path(DB_PATH).exists():
        conn = sqlite3.connect(DB_PATH)
        conn.executescript(DDL_AND_DATA)
        conn.commit(); conn.close()
        rich.print("[green]SQLite demo DB created.[/]")
    else:
        rich.print("[green]SQLite demo DB already exists.[/]")

def build_index():
    if "ecom_meta" in [c.name for c in chroma_client.list_collections()]:
        rich.print("[green]Chroma collection already exists.[/]")
        return chroma_client.get_collection("ecom_meta")
     
    coll = chroma_client.create_collection("ecom_meta")
    for tbl in SCHEMA_JSON:
        tbl_doc = f"TABLE {tbl['name']}: {tbl['description']}"
        coll.add(ids=[tbl["name"]],
                  documents=[tbl_doc],
                  metadatas=[{"level": "table", "table": tbl["table"]}],
                  embeddings=[embedding_model.embed_documents([tbl_doc])[0]])
    
        for col in tbl["columns"]:
            col_doc = f"{tbl['table']}.{col['name']} — {col['description']}"
            coll.add(ids=[f"{tbl['table']}.{col['name']}"], documents=[col_doc],
                     metadatas=[{"level":"column","table":tbl['table'],"column":col['name']}],
                     embeddings=[embedding_model.embed_documents([col_doc])[0]])
            
    rich.print("[green]Chroma vector index built.[/]")
    return coll

coll = build_index()


@tool
def get_relevant_schema(question: str) -> str:
    """
    Return the most relevant subset of the database schema (tables and columns)
    for a give natual-language analytics question. The output is a multilene string,
    each line formatted as 'table.column - description'.
    
    Args:
        question (str): The natural-language analytics question from the user.
    """

    emb = embedding_model.embed_query(question)
    res = coll.query(query_embeddings=[emb],
                     n_results=5,
                     include=["documents", "metadatas"])
    
    tables, out = set(), []
    for doc, meta in zip(res["documents"][0], res["metadatas"][0]):
        if meta["level"] == "table":
            tables.add(meta["table"])
            out.append(f"{meta['table']} - {doc}")
        elif meta["level"] == "column" and meta["table"] in tables:
            out.append(doc)

    return "\n".join(out)


@tool
def run_sql_query(sql: str) -> str:
    """
    Safely execute a **read-only** SQL query against the local SQLite database
    and return at most 100 rows as a JSON string.

    Args:
        sql: SELECT statement to run.
    """

    forbidden = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "CREATE", "TRUNCATE"]
    if any(tok in sql.upper() for tok in forbidden):
        raise ValueError("Refused to run unsafe SQL query.")
    
    if "LIMIT" not in sql.upper():
        sql = f"SELECT * FROM ({sql}) AS sub LIMIT 100"
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    conn.close()

    if not rows:
        return json.dumps({"error": "No results found."})
    
    return json.dumps({"columns": cols, "rows": rows}, ensure_ascii=False)


agent = CodeAgent(
    tools=[get_relevant_schema, run_sql_query],
    model=llm,
    add_base_tools=False
)

def main():
    rich.print("[bold cyan]smolagents NL->SQL demo"
               "hit Enter on empty line to quit.[/]")
    while True:
        question = input("Question: ").strip()
        if not question:
            break
        answer = agent.run(question)
        rich.print(f"[bold green]Answer:[/] {answer}")


if __name__ == "__main__":
    init_resources()
    main()