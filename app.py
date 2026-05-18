from telegram import Update
from king_clan_bot import application
import json

# Для Vercel нужна синхронная функция-обработчик
async def telegram_webhook(request_body):
    """Обрабатывает входящие webhook от Telegram"""
    update = Update.de_json(json.loads(request_body), application.bot)
    await application.initialize()
    await application.process_update(update)
    return {"statusCode": 200, "body": "ok"}

# Экспортируем для Vercel
def handler(event, context):
    """Serverless функция для Vercel"""
    import asyncio
    
    # Получаем тело запроса
    body = event.get("body", "{}")
    
    # Запускаем async обработчик
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(telegram_webhook(body))
    loop.close()
    
    return {
        "statusCode": 200,
        "body": "OK"
    }

# Альтернативный экспорт
app = handler
