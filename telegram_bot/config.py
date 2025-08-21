import os
from dotenv import load_dotenv

load_dotenv()
env_path_local = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path_local):
    load_dotenv(env_path_local, override=True)

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME", "")
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api")
PAGE_SIZE = int(os.getenv("PAGE_SIZE", "10"))
