import json

from google import genai

from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

DOCUMENT_TYPES = [
    "lecture_notes",
    "financial_report",
    "meeting_notes",
    "research_article",
    "other"
]

CLASSIFICATION_PROMPT = """You are classifying a document into exactly one category. 

Categories: lecture_notes, financial_report, meeting_notes, research_article, other 

Respond with a JSON object giving the categpry and your confidence. 

Document test: 
{text}"""

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"type": "string", "enum": DOCUMENT_TYPES},
        "confidence": {"type": "number"},
    },
    "required": ["type", "confidence"],
}

def classify_document(text: str) -> dict:
    prompt = CLASSIFICATION_PROMPT.format(text=text[:4000])

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
        response_format={"type": "text",
                         "mime_type": "application/json",
                         "schema": RESPONSE_SCHEMA
                         },
    )

    result = json.loads(interaction.output_text)

    if result["type"] not in DOCUMENT_TYPES:
        result["type"] = "other"

    return result