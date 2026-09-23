# .txt, .pdf, and .docx all store their text completely differently
# so each needs its own way of getting the text out
# you cant decode PDF of Word bytes like you can with plain text

import io

from pypdf import PdfReader
from docx import Document

def extract_text(filename: str, content: bytes) -> str:
    # routes to the right extractor based on the extension
    """Turn the raw bytes of an uploaded file into plain text."""
    name = filename.lower() # so it still matches if someone uploads NOTES.TXT

    # UTF-8 / str.decode() docs: https://docs.python.org/3/library/stdtypes.html#bytes.decode
    # full list of error handling modes: https://docs.python.org/3/library/codecs.html#error-handlers
    if name.endswith(".txt"):
        # errors="replace" means if a byte isnt valid UTF-8 it gets
        # swapped for a "?" instead of the whole thing crashing
        return content.decode("utf-8", errors="replace")

    if name.endswith(".pdf"):
        return _extract_pdf_text(content)

    if name.endswith(".docx"):
        return _extract_docx_text(content)

    raise ValueError(f"Unsupported file type: {filename}")

# pypdf docs: https://pypdf.readthedocs.io/en/stable/
# pypdf PdfReader reference: https://pypdf.readthedocs.io/en/stable/modules/PdfReader.html
def _extract_pdf_text(content: bytes) -> str:
    # PdfReader wants something that looks like an open file, not raw
    # bytes, so io.BytesIO wraps the bytes to make that work
    # io.BytesIO docs: https://docs.python.org/3/library/io.html#io.BytesIO
    reader = PdfReader(io.BytesIO(content))

    # page.extract_text() can come back None on some pages, the "or ''"
    # just avoids that blowing up when we join everything together
    # extract_text() reference: https://pypdf.readthedocs.io/en/stable/modules/PageObject.html
    pages = [page.extract_text() or "" for page in reader.pages]
    text = "\n".join(pages).strip()

    if not text:
        # this happens with scanned pdfs, theyrejust photos of pages
        # and no real text underneath
        raise ValueError(
            "Could not extract any text from this PDF. "
            "It may be a scanned document without selectable text."
        )

    return text

# python-docx docs: https://python-docx.readthedocs.io/en/latest/
# we 'pip install python-docx' but 'import docx', not 'import python-docx',
# because the package name and import name are different
# https://pypi.org/project/python-docx/
def _extract_docx_text(content: bytes) -> str:
    document = Document(io.BytesIO(content))

    # Document.paragraphs reference: https://python-docx.readthedocs.io/en/latest/api/document.html
    parts = [p.text for p in document.paragraphs]

    # found out that tables in a .docx are stored completely separately
    # from paragraphs, i tested it with my CV (which uses some tables)
    # and the character count came back lower than expected until i added
    # this loop to pull text out of tables
    # Document.tables / table structure reference:
    # https://python-docx.readthedocs.io/en/latest/api/table.html
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text.strip(): # skip empty cells
                    parts.append(cell.text)

    text = "\n".join(parts).strip()

    if not text:
        raise ValueError("Could not extract any text from this Word document.")

    return text