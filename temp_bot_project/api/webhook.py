from http.server import BaseHTTPRequestHandler
import json
import os
import requests

# Этот класс будет обрабатывать входящие запросы от Telegram
class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        # Получаем токен бота из переменных окружения Vercel
        BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
        TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        try:
            # Читаем тело запроса
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            update = json.loads(post_data.decode('utf-8'))

            # Извлекаем id чата и текст сообщения
            chat_id = update['message']['chat']['id']
            message_text = update['message']['text']
            
            # --- Логика Бота ---
            # Если пользователь отправил /start
            if message_text == '/start':
                welcome_text = """Добро пожаловать в Oxide Legacy! 🔥

Это кликер-игра, доступная прямо в Telegram.

Нажми на кнопку 'Меню' внизу, чтобы начать игру!"""
                
                # Готовим данные для отправки сообщения обратно пользователю
                payload = {
                    'chat_id': chat_id,
                    'text': welcome_text
                }
                
                # Отправляем сообщение через API Telegram
                requests.post(TELEGRAM_API_URL, json=payload)

        except Exception as e:
            # В случае ошибки, можно записать ее в лог Vercel
            print(f"Error: {e}")

        # Отправляем Telegram ответ 200 OK, чтобы показать, что мы получили обновление
        self.send_response(200)
        self.end_headers()
        return
