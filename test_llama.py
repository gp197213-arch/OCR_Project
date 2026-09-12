import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests

url = "http://localhost:8080/v1/chat/completions"

test_text = """Прuвет! Это тестовый текст с ошuбками OCR.
Некоторые буквы заменены на латuницу, есть лuшние пробелы и склеенныеслова.
Также встpечаются цифpы вместо букв: Здpaвствуйте, товapищи!"""

payload = {
    "messages": [
        {"role": "system", "content": (
            "Ты корректор текста после OCR. Исправь ошибки распознавания: "
            "замени латинские буквы на кириллические, убери лишние пробелы, "
            "раздели склеенные слова. Сохрани смысл и пунктуацию. "
            "Верни ТОЛЬКО исправленный текст, без пояснений."
        )},
        {"role": "user", "content": test_text}
    ],
    "temperature": 0.1
}

r = requests.post(url, json=payload, timeout=120)
r.raise_for_status()
print("=== ДО ===")
print(test_text)
print("\n=== ПОСЛЕ ===")
print(r.json()["choices"][0]["message"]["content"])