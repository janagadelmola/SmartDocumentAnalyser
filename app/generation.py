# takes extracted text + the classified document type, and generates the
# right kind of output for it (flashcards for lecture notes, a summary
# for reports/meeting notes)

# same pattern as classification.py, prompt template +JSON schema +
# client.interactions.create(), just a different prompt/schema per
# output type

import json
from google import genai
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

FLASHCARD_PROMPT = """
You are creating study flashcards from a set of lecture notes. 

Create as many flashcards as needed to cover all the important 
concepts definitions, and examples in the notes, don't limit 
yourself to a small number, longer notes should produce more 
flashcards. Each flashcard has a short question and a clear, 
concise answer. 

Respond with a JSON object containing a "flashcards" list. 

Lecture notes: 
{text}"""

# JSON schema reference (same one used in classification.py):
# https://json-schema.org/understanding-json-schema/
FLASHCARD_SCHEMA = {
    "type": "object",
    "properties": {
        "flashcards": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "answer": {"type": "string"},
                },
                "required": ["question", "answer"],
            },
        },
    },
    "required": ["flashcards"],
}

def generate_flashcards(text: str) -> dict:
    # sending the full extracted text
    # go back to truncating (or splitting into chunks) if someone
    # uploads something huge (could have)
    prompt = FLASHCARD_PROMPT.format(text=text)

    # same response_format shape figured out in classification.py, 
    # type="text" + mime_type="application/json" +schema=...
    # docs: https://ai.google.dev/gemini-api/docs/structured-output
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": FLASHCARD_SCHEMA,
        },
    )

    return json.loads(interaction.output_text)

SUMMARY_PROMPT = """
You are summarising a document for someone who has limited time to read it. 

Write a summary whose length matches the document, a short document gets a 
short summary, a long or detailed one gets a longer summary (a SUMMARY nonetheless) 
that still covers everything important. Also list the key takeaways as short bullet 
points, as mant as the document actually has, don't pad or artificially limit the count. 

Respond with a JSON object. 

Document: 
{text}"""

SUMMARY_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "key_points": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": ["summary", "key_points"],
}

def generate_summary(text: str) -> dict:
    # sending the full text, same reasoning as flashcards
    prompt = SUMMARY_PROMPT.format(text=text)

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": SUMMARY_SCHEMA,
        },
    )

    return json.loads(interaction.output_text)