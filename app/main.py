# this file is the "front door" of the backend, it defines the
# web addresses (endpoints) that people can hit, and decides what to do
# when a request comes in. it doesnt know how text extraction works, just
# that extract_text() will give it text back, and thats the point of keeping
# extraction.py separate

# FastAPI docs (file uploads): https://fastapi.tiangolo.com/tutorial/request-files/

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.extraction import extract_text

app = FastAPI(title="Smart Document Analyser")

# 1024 bytes = 1 KB, 1024 KB = 1 MB
# keeping it as a constant so its easy to change later

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

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

    # only returning a preview right now, nothing gets saved yet

    return {
        "filename": file.filename,
        "characters": len(text),
        "preview": text[:200],
    }