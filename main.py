from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from stammering import detect_stammering

app = FastAPI(title="RAG Translation Backend")

# Database initialization
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
    source_language: str
    target_language: str
    sentence: str
    translation: str

@app.post("/pairs")
def add_pair(pair: Pair):
    cursor.execute(
        "INSERT INTO pairs (source_lang, target_lang, sentence, translation) VALUES (?, ?, ?, ?)",
        (pair.source_language, pair.target_language, pair.sentence, pair.translation)
    )
    conn.commit()
    return {"status": "ok"}


@app.get("/prompt")
def get_prompt(source_language: str, target_language: str, query_sentence: str):
    cursor.execute(
        "SELECT sentence, translation FROM pairs WHERE source_lang=? AND target_lang=?",
        (source_language, target_language)
    )
    rows = cursor.fetchall()

    if not rows:
        return {"prompt": f"Translate from {source_language} to {target_language}: {query_sentence}"}

    corpus = [query_sentence] + [row[0] for row in rows]
    vectorizer = TfidfVectorizer().fit(corpus)
    vectors = vectorizer.transform(corpus)
    sims = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

    top_k = min(4, len(rows))
    idx = np.argsort(sims)[-top_k:][::-1]

    examples = []
    for i in idx:
        src, tgt = rows[i]
        examples.append(f"Source: {src}\nTarget: {tgt}")

    prompt = (
        f"Translate from {source_language} to {target_language}:\n"
        f"Input: {query_sentence}\n\n"
        f"Examples:\n\n" + "\n\n".join(examples)
    )

    return {"prompt": prompt}

@app.get("/stammering")
def stammering(source_sentence: str, translated_sentence: str):
    return {"has_stammer": detect_stammering(source_sentence, translated_sentence)}