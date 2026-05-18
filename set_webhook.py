import requests
import sys

BOT_TOKEN = "8681996510:AAEoGKm_UJYcm4qCeHOOcxVse88pdOQyTGQ"

if len(sys.argv) < 2:
    print("Использование: python set_webhook.py <ваш_vercel_url>")
    print("Пример: python set_webhook.py https://your-app.vercel.app")
    sys.exit(1)

WEBHOOK_URL = sys.argv[1].rstrip('/') + '/'

# Устанавливаем webhook
response = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
    json={"url": WEBHOOK_URL}
)

print(f"Статус: {response.status_code}")
print(f"Ответ: {response.json()}")

# Проверяем webhook
info = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo")
print(f"\nИнформация о webhook:")
print(info.json())
