import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

if __name__ == '__main__':
    # Получить токен из .env
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN не найден в .env файле!")

# Загружаем меню
with open("menu.json", "r", encoding="utf-8") as f:
    MENU = json.load(f)


# ---------- Функция создания кнопок ----------
def build_keyboard(buttons):
    keyboard = []

    for btn in buttons:
        keyboard.append([
            InlineKeyboardButton(btn["title"], callback_data=btn["action"])
        ])

    return InlineKeyboardMarkup(keyboard)


# ---------- Показ экрана ----------
async def show_screen(chat_id, context, screen_name):

    if screen_name == "main_menu":
        screen = MENU["main_menu"]

    elif screen_name in MENU:
        screen = MENU[screen_name]

    elif "faq" in MENU and screen_name in MENU["faq"]:
        screen = MENU["faq"][screen_name]

    else:
        return

    text = screen["text"]
    buttons = screen.get("buttons")

    reply_markup = build_keyboard(buttons) if buttons else None

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup
    )


# ---------- Команда /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_screen(update.effective_chat.id, context, "main_menu")


# ---------- Обработка кнопок ----------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    action = query.data

    await show_screen(query.message.chat.id, context, action)


# ---------- Запуск ----------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен")
    app.run_polling()


if __name__ == "__main__":
    main()

from telegram.ext import MessageHandler, filters

async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    await update.message.reply_text(
        MENU["mini_analysis"]["action_after_data"]["text"],
        reply_markup=build_keyboard(
            MENU["mini_analysis"]["action_after_data"]["buttons"]
        )
    )

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, user_message))
