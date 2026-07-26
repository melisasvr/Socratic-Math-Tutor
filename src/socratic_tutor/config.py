import os

from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile").strip(chr(34)).strip(chr(39))
PROGRESS_DB_PATH = os.getenv("PROGRESS_DB_PATH", "data/progress.db")
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")
DEFAULT_THEME = os.getenv("DEFAULT_THEME", "Classic")

WELCOME_MESSAGE = (
    "I'm ready to be your Socratic Math Tutor! I'll guide you with hints and questions "
    "rather than just giving answers - because that's how real understanding sticks.\n\n"
    "What problem are you working on today?\n"
    "Just type it out (or paste it), and we'll work through it together step by step!"
)

