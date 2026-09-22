import io

from pypdf import PdfReader
from docx import Document

def extract_text(filename: str, content: bytes) -> str:
    """Turn the raw bytes of an uploaded file into plain text."""
    name = filename.lower()

    if name.endswith(".txt"):
        return content.decode("utf-8", errors="replace")

    if name.endswith(".pdf"):
        return _extract_pdf_text(content)

    if name.endswith(".docx"):
        return _extract_docx_text(content)

    raise ValueError(f"Unsupported file type: {filename}")

def _extract_pdf_text(content: bytes) -> str:
    reader = PdfReader(io.BytesIO(content))

    pages = [page.extract_text() or "" for page in reader.pages]
    text = "\n".join(pages).strip()

    if not text:
        raise ValueError(
            "Could not extract any text from this PDF. "
            "It may be a scanned document without selectable text."
        )

    return text

def _extract_docx_text(content: bytes) -> str:
    document = Document(io.BytesIO(content))

    parts = [p.text for p in document.paragraphs]

    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text.strip():
                    parts.append(cell.text)

    text = "\n".join(parts).strip()

    if not text:
        raise ValueError("Could not extract any text from this Word document.")

    return text