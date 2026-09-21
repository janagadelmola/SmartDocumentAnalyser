from fastapi import FastAPI

app = FastAPI(title="Smart Document Analyser")

@app.get("/health")
def health_check():
    return {"status": "ok"}