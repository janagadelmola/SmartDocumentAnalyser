# handles loading the Gemini API key from a .env file, so the actual
# key never sits directly in any .py file and never gets committed to
# git (.env is listed in .gitignore)

import os

# python-dotenv docs: https://pypi.org/project/python-dotenv/
# python-dotenv README: https://github.com/theskumar/python-dotenv
from dotenv import load_dotenv

load_dotenv() # reads .env and loads it into this programs's environment

# os.environ reference: https://docs.python.org/3/library/os.html#os.environ
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    # better to crash immediately with a clear message here than have
    # the app start fine and then fail confusingly later the first
    # time something actually tries to call Gemini
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Create a .env file in the project "
        "root with a line like: GEMINI_API_KEY=your_api_key_here"
    )