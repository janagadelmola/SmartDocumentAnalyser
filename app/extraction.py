def extract_text(filename: str, content: bytes) -> str:
    """Turn the raw bytes of an uploaded file into plain text."""
    name = filename.lower()

    if name.endswith(".txt"):
        return content.decode("utf-8", errors="replace")

    raise ValueError(f"Unsupported file type: {filename}")