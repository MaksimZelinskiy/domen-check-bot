# prod
import os
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

DB_HOST, DB_NAME, DB_PASSWORD, DB_USER, DB_PORT = os.environ.get("DB_HOST", ""), os.environ.get("DB_NAME", ""), os.environ.get("DB_PASSWORD", ""), os.environ.get("DB_USER", ""), os.environ.get("DB_PORT", "")

STANDARD_ROLES = [
    {"id": 1, "name": "Админ"},
    {"id": 2, "name": "Пользователь"},
    {"id": 3, "name": "Гость"}
]

STANDARD_ROLES_IDS = [role["id"] for role in STANDARD_ROLES]