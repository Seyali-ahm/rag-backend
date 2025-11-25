from fastapi import FastAPI

app = FastAPI(title="RAG Translation Backend")

@app.get("/")
def root():
    return {"status": "running"}
