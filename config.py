import os

from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")


if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is not configured. "
        "Please set the BOT_TOKEN environment variable."
    )


try:
    ADMIN_ID = int(ADMIN_ID) if ADMIN_ID else 0
except ValueError:
    raise RuntimeError(
        "ADMIN_ID must be a valid integer."
    )
