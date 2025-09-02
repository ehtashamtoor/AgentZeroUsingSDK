import os
from dotenv import load_dotenv

load_dotenv()

# App settings
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# LLM settings
MODEL = os.getenv("model")
BASE_URL = os.getenv("BASE_URL")

# supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


required_vars = {
    "GEMINI_API_KEY": GEMINI_API_KEY,
    "model": MODEL,
    "SUPABASE_URL": SUPABASE_URL,
    "SUPABASE_KEY": SUPABASE_KEY,
}
missing = [k for k, v in required_vars.items() if not v]
if missing:
    raise RuntimeError(f"Missing required environment variables: {missing}")
