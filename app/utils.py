import os
from dotenv import load_dotenv

load_dotenv()

def get_env(key: str):
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Missing environment variable: {key}")
    return value
