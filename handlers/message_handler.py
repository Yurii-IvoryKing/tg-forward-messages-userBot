from telethon import events
from services.nlp_processor import NLPProcessor
from config.settings import SOURCE_CHANNEL_IDS, TARGET_USER_IDS
import os
import asyncio

nlp_processor = NLPProcessor()


async def setup_handlers(client):
    try:

        source_channels = []
        for entity in SOURCE_CHANNEL_IDS:
            try:
                channel = await client.get_entity(entity)
                source_channels.append(channel)
                print(
                    f"✅ Канал додано: {channel.title if hasattr(channel, 'title') else channel.id}"
                )
            except Exception as e:
                print(f"❌ Помилка отримання каналу {entity}: {str(e)}")

        target_users = []
        for entity in TARGET_USER_IDS:
            try:
                user = await client.get_entity(entity)
                target_users.append(user)
                print(f"✅ Цільовий користувач/канал додано: {user.id}")
            except Exception as e:
                print(
                    f"❌ Помилка отримання цільового користувача/каналу {entity}: {str(e)}"
                )

        # Якщо немає каналів або цільових користувачів, зупиняємо бота
        if not source_channels or not target_users:
            print("❌ Немає каналів-джерел або цільових користувачів. Бот зупинено.")
            return

        # Обробка звичайних повідомлень (без альбомів)
        @client.on(
            events.NewMessage(
                chats=source_channels, func=lambda e: not e.message.grouped_id
            )
        )
        async def single_message_handler(event):
            try:
                text = event.raw_text
                has_keywords = nlp_processor.check_keywords(text)

                if not has_keywords:
                    return

                is_interesting = await nlp_processor.is_interesting(text)
                if not is_interesting:
                    return

                # Пересилання всім цільовим користувачам/каналам
                for target_user in target_users:
                    await event.forward_to(target_user)

            except Exception as e:
                print(f"❌ Помилка: {str(e)}")

        # Обробка альбомів (групових повідомлень)
        @client.on(events.Album(chats=source_channels))
        async def album_handler(event):
            try:
                # Отримуємо текст з першого повідомлення альбому
                text = event.messages[0].raw_text if event.messages else ""
                if not text:
                    return

                has_keywords = nlp_processor.check_keywords(text)
                if not has_keywords:
                    return

                is_interesting = await nlp_processor.is_interesting(text)
                if not is_interesting:
                    return

                # Пересилання всім цільовим користувачам
                for target_user in target_users:
                    await client.forward_messages(
                        target_user,
                        event.messages,
                        from_peer=event.chat_id,
                        as_album=True,
                    )
                    print(f"✅ Альбом переслано до {target_user.id}!")

            except Exception as e:
                print(f"❌ Помилка: {str(e)}")

    except Exception as e:
        print(f"❌ Помилка ініціалізації: {str(e)}")
