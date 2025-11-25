from fastapi import FastAPI
from pydantic import BaseModel
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

class Pair(BaseModel):
    source_lang: str
    target_lang: str
    sentence: str
    translation: str

@app.post("/pairs")
def add_pair(pair: Pair):
    cursor.execute(
        "Insert into pairs (source_lang, target_lang, sentence, translation) VALUES (?, ?, ?, ?)",
        (pair.source_lang, pair.target_lang, pair.sentence, pair.translation)
    )
    conn.commit()
    return {"status": "ok"}
