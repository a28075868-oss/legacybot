import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

# ==========================================
#   НАСТРОЙКИ
# ==========================================
BOT_TOKEN = "8681996510:AAEoGKm_UJYcm4qCeHOOcxVse88pdOQyTGQ"
ADMIN_CHAT_ID = 7394719247
# ==========================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

NAME, AGE, EXPERIENCE, ROLE = range(4)

ROLES = [
    "мейн",
    "фармила",
    "ночной охранник",
    "коллер cpt",
    "cpt игрок ",
    "sai помощник клана",
    "Любая роль",
]

EXPERIENCE_OPTIONS = [
    ("✅ Да, есть опыт в кланах", "yes"),
    ("❌ Нет, первый раз", "no"),
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    welcome_text = (
        "*Добро пожаловать в набор клана KING* 👑\n\n"
        "Я задам тебе несколько вопросов, и твоя заявка уйдёт на рассмотрение сотрудников Sai.\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "❓ *Как тебя зовут?* (имя или ник)"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    name = update.message.text.strip()
    if len(name) < 2 or len(name) > 32:
        await update.message.reply_text("⚠️ Введи корректное имя (от 2 до 32 символов).")
        return NAME
    context.user_data["name"] = name
    await update.message.reply_text(
        f"Отлично, *{name}*! 👋\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "❓ *Сколько тебе лет?*",
        parse_mode="Markdown"
    )
    return AGE


async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    if not text.isdigit() or not (10 <= int(text) <= 60):
        await update.message.reply_text("⚠️ Введи корректный возраст (от 10 до 60 лет).")
        return AGE
    context.user_data["age"] = text
    keyboard = [
        [InlineKeyboardButton(label, callback_data=val)]
        for label, val in EXPERIENCE_OPTIONS
    ]
    await update.message.reply_text(
        "━━━━━━━━━━━━━━━━━━━━\n"
        "❓ *Был ли у тебя опыт игры в кланах?*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return EXPERIENCE


async def get_experience(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    exp_map = {"yes": "✅ Да, есть опыт", "no": "❌ Нет, первый раз"}
    context.user_data["experience"] = exp_map.get(query.data, query.data)
    keyboard = [
        [InlineKeyboardButton(role, callback_data=role)]
        for role in ROLES
    ]
    await query.edit_message_text(
        "━━━━━━━━━━━━━━━━━━━━\n"
        "❓ *На какую должность хочешь вступить в клан?*\n\n"
        "Выбери из списка:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return ROLE


async def get_role(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    role = query.data
    context.user_data["role"] = role
    user = query.from_user
    data = context.user_data

    confirm_text = (
        "✅ *Заявка отправлена!*\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📋 *Твоя заявка:*\n\n"
        f"👤 Имя: *{data['name']}*\n"
        f"🎂 Возраст: *{data['age']} лет*\n"
        f"🎮 Опыт в кланах: *{data['experience']}*\n"
        f"🏷️ Желаемая роль: *{role}*\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "⏳ Ожидай ответа от руководства клана *KING*.\n"
        "Мы свяжемся с тобой в ближайшее время! 👑"
    )
    await query.edit_message_text(confirm_text, parse_mode="Markdown")

    mention = f"[{user.full_name}](tg://user?id={user.id})"
    admin_text = (
        "🔔 *НОВАЯ ЗАЯВКА В КЛАН KING* 🔔\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 *Имя:* {data['name']}\n"
        f"🎂 *Возраст:* {data['age']} лет\n"
        f"🎮 *Опыт в кланах:* {data['experience']}\n"
        f"🏷️ *Желаемая роль:* {role}\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"📲 *Telegram:* {mention}\n"
        f"🆔 *ID:* `{user.id}`\n"
        f"🔗 *Username:* @{user.username if user.username else '—'}"
    )
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=admin_text,
        parse_mode="Markdown"
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "❌ Заявка отменена. Если передумаешь — напиши /start",
        parse_mode="Markdown"
    )
    return ConversationHandler.END


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Напиши /start чтобы подать заявку в клан KING 👑"
    )


# Создаём приложение на верхнем уровне для деплоя
application = Application.builder().token(BOT_TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        NAME:       [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        AGE:        [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
        EXPERIENCE: [CallbackQueryHandler(get_experience)],
        ROLE:       [CallbackQueryHandler(get_role)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    per_message=False,
)

application.add_handler(conv_handler)
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))


async def main():
    logger.info("Бот KING запущен...")
    await application.initialize()
    await application.start()
    await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
