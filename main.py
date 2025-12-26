import os
import random
import requests
import json

# Конфигурация из переменных окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID") # ID канала (начинается с -100) или @username
MESSAGE_ID = os.environ.get("MESSAGE_ID") # ID сообщения, которое нужно менять
IMAGE_DIR = "images"

def update_telegram_photo():
    if not all([BOT_TOKEN, CHANNEL_ID, MESSAGE_ID]):
        print("Error: Не заданы переменные окружения (BOT_TOKEN, CHANNEL_ID, MESSAGE_ID)")
        return

    # Получаем список картинок
    try:
        files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    except FileNotFoundError:
        print(f"Error: Директория {IMAGE_DIR} не найдена")
        return

    if not files:
        print("Error: В папке нет картинок")
        return

    # Выбираем случайную картинку (или можно придумать логику по времени)
    selected_image = random.choice(files)
    image_path = os.path.join(IMAGE_DIR, selected_image)
    
    print(f"Выбрана картинка: {selected_image}")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageMedia"

    # Формируем запрос
    # media должен быть JSON-строкой, где media="attach://<ключ_файла>"
    media_payload = {
        "type": "photo",
        "media": "attach://image_upload",
    }

    with open(image_path, "rb") as img_file:
        files_data = {
            "image_upload": img_file
        }
        data = {
            "chat_id": CHANNEL_ID,
            "message_id": MESSAGE_ID,
            "media": json.dumps(media_payload)
        }
        
        response = requests.post(url, data=data, files=files_data)

    if response.status_code == 200:
        print("Успешно обновлено!")
    else:
        print(f"Ошибка API: {response.text}")

if __name__ == "__main__":
    update_telegram_photo()
