from fastapi import FastAPI
import sqlite3

app = FastAPI(title="RAG Translation Backend")

conn = sqlite3.connect("rag.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS pairs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_lang TEXT,
        target_lang TEXT,
        sentence TEXT,
        translation TEXT
    )
""")
conn.commit()

@app.get("/")
def root():
    return {"db": "initialized"}
