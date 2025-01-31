import cohere
import os
import aiohttp
import asyncio
import json


class NLPProcessor:
    def __init__(self):
        self.api_key = os.getenv("COHERE_API_KEY")
        self.co = cohere.Client(self.api_key)
        self.keywords = self._load_keywords()
        self.examples = self._load_examples()

    def _load_keywords(self):
        """Завантажує ключові слова з файлу keywords.txt"""
        with open("config/keywords.txt", "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip()]

    def _load_examples(self):
        """Завантажує приклади для Cohere з файлу examples.json"""
        with open("services/examples.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def check_keywords(self, text: str) -> bool:
        """Перевіряє, чи містить текст ключові слова"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.keywords)

    async def is_interesting(self, text: str) -> bool:
        # Спочатку перевіряємо ключові слова
        if not self.check_keywords(text):
            return False

        # Якщо ключові слова є, запитуємо Cohere
        url = "https://api.cohere.ai/v1/classify"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "small",
            "inputs": [text],
            "examples": self.examples,
            "outputIndicator": "Связаны ли это сообщение с атакой дронов? Ответ 'Yes', или 'No",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        prediction = result["classifications"][0]["prediction"].lower()
                        confidence = result["classifications"][0]["confidence"]

                        # Перевіряємо відповідь та впевненість моделі
                        return prediction == "интересно" and confidence >= 0.7
                    else:
                        print(f"Cohere помилка: {response.status}")
                        return False
        except Exception as e:
            print(f"Помилка: {str(e)}")
            return False
