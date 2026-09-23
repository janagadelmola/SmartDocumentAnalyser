# sends the extracted document text to Gemini and gets back which of
# the 5 doc types it thinks it is, plus a confidence score

# using client.interactions.create() instead of client.models.generate_content()
# because generate_content stated throwing 404 errors partway through building
# this because gemini-2.5-flash got retired for new users, so had to switch
# over to Google's newer interactions API mid-project

# also using "structured outputs" (a JSON schema passed through response_format)
# so Gemini's reply is actually forced into a shape, instead of just asking
# for JSON in the prompt text
import json

# python-genai SDK on Github: https://github.com/googleapis/python-genai
from google import genai

from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

# matches the DOCUMENT_TYPES table in docs/design.md, kept as one list
# so theres a single place to update if a category ever changes
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

# the "enum" here is the important part, it means Gemini cannot return
# a type outisde these 5 categories, this is enforced by the API itself
# not just in the prompt
# JSON schema enum keyword: https://json-schema.org/understanding-json-schema/reference/enum
RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"type": "string", "enum": DOCUMENT_TYPES},
        "confidence": {"type": "number"},
    },
    "required": ["type", "confidence"],
}

# interactions API overview: https://ai.google.dev/gemini-api/docs/interactions
# interactions API full reference: https://ai.google.dev/api/interactions-api
def classify_document(text: str) -> dict:
    # only sending the first ~4000 characters, dont need the whole document to
    # figure out what type it is, and a smaller request is faster and cheaper
    prompt = CLASSIFICATION_PROMPT.format(text=text[:4000])

    # first attemot nested things under "json_schema" and got a 400 back, had 
    # to check the docs to find the correct structure
    # structures outputs guide: https://ai.google.dev/gemini-api/docs/structured-output
    # JSON schema spec (what RESPONSE_SCHEMA follows): https://json-schema.org/understanding-json-schema/
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
        # just a safety net in case Gemini ever ignores the schema and
        # returns something unexpected
        result["type"] = "other"

    return result