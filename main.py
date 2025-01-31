import os
from telethon import TelegramClient
from config import settings
from handlers.message_handler import setup_handlers

client = TelegramClient('userbot_session', settings.API_ID, settings.API_HASH)

async def main():
    await client.start(settings.PHONE_NUMBER)
    print("🟢 Бот запущений!")
    await setup_handlers(client)
    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())