# this file is the "front door" of the backend, it defines the
# web addresses (endpoints) that people can hit, and decides what to do
# when a request comes in. it doesnt know how text extraction works, just
# that extract_text() will give it text back, and thats the point of keeping
# extraction.py separate

# FastAPI docs (file uploads): https://fastapi.tiangolo.com/tutorial/request-files/

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.classification import classify_document
from app.extraction import extract_text
from app.generation import generate_flashcards, generate_summary

app = FastAPI(title="Smart Document Analyser")

# 1024 bytes = 1 KB, 1024 KB = 1 MB
# keeping it as a constant so its easy to change later

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

# matches the DOCUMENT_TYPES -> OUTPUT_TYPES mapping table in
# docs/design.md. lecture notes -> flashcards, everything else -> summary 
# for now
TYPE_TO_GENERATOR = {
    "lecture_notes": generate_flashcards,
    "financial_report": generate_summary,
    "meeting_notes": generate_summary,
    "research_article": generate_summary,
    "other": generate_summary,
}

@app.get("/health")
def health_check():
    # checking if the server is "alive"
    return {"status": "ok"}

@app.post("/documents")
async def upload_document(file: UploadFile = File(...)):
    # POST because were sending/creating something, not fetching
    # async + await so the server isnt frozen waiting for the upload
    # reference: https://fastapi.tiangolo.com/async/
    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        # 413 is the HTTP code for "too big", using it properly
        # instead of just returning a generic error
        # reference: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
        raise HTTPException(status_code=413, detail="File is too large (max 5 MB).")

    try:
        text = extract_text(file.filename, content)
    except ValueError as error:
        # extraction.py raises ValueError for bad file types, catching it
        # here so the user gets a proper 400 with a real message instead
        # of it crashing into a 500 error with no explanation
        # reference: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400
        raise HTTPException(status_code=400, detail=str(error))

    # step 1: figure out what kind of document this is
    classification = classify_document(text)
    doc_type = classification["type"]

    # step 2: run the right generator for that type
    generator = TYPE_TO_GENERATOR[doc_type]
    output = generator(text)

    return {
        "filename": file.filename,
        "characters": len(text),
        "document_type": doc_type,
        "confidence": classification["confidence"],
        "output": output,
    }