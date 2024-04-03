import os
from dotenv import load_dotenv

load_dotenv()

B_TOKEN = os.getenv("B_TOKEN")
BACKEND_BASE_URL = os.getenv("BACKEND_URL")
BACKEND_TOKEN = os.getenv("BACKEND_TOKEN")
BOT_AGENT = os.getenv("BOT_AGENT")
