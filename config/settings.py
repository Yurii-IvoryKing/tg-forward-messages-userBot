import os
from dotenv import load_dotenv
from decouple import config

load_dotenv()


def parse_entities(env_var: str) -> list:
    """Парсить список ID/username з .env, автоматично видаляючи лапки та пробіли."""
    raw_value = config(env_var, default="")

    entities = []
    for entity in raw_value.split(","):
        entity = entity.strip().strip("'\"")
        if not entity:
            print(f"⚠️ Увага: Порожнє значення у {env_var}")
            continue
        # Спроба конвертувати в int (для числових ID)
        try:
            entity = int(entity)
        except ValueError:
            pass

        entities.append(entity)

    return entities


# Налаштування з .env
API_ID = config("API_ID", cast=int)
API_HASH = config("API_HASH")
SOURCE_CHANNEL_IDS = parse_entities("SOURCE_CHANNEL_IDS")
TARGET_USER_IDS = parse_entities("TARGET_USER_IDS")
PHONE_NUMBER = config("PHONE_NUMBER")
COHERE_API_KEY = config("COHERE_API_KEY", default="")

KEYWORDS_FILE = "config/keywords.txt"
