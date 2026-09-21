from fastapi import FastAPI, File, HTTPException, UploadFile

from app.extraction import extract_text

app = FastAPI(title="Smart Document Analyser")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/documents")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File is too large (max 5 MB).")

    try:
        text = extract_text(file.filename, content)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return {
        "filename": file.filename,
        "characters": len(text),
        "preview": text[:200],
    }