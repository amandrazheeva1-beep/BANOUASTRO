from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters
)

from config import TOKEN
from handlers.menu_handlers import show_screen
from handlers.mini_analysis import *
from handlers.booking import book


async def start(update, context):
    await show_screen(update.effective_chat.id, context, "main_menu")


async def buttons(update, context):
    action = update.callback_query.data

    if action == "mini_analysis":
        return await start_mini(update, context)

    if action == "book_consultation":
        await book(update, context)
        return

    await show_screen(update.effective_chat.id, context, action)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_mini, pattern="mini_analysis")],
        states={
            NAME: [MessageHandler(filters.TEXT, get_name)],
            DATE: [MessageHandler(filters.TEXT, get_date)],
            REQUEST: [MessageHandler(filters.TEXT, get_request)],
        },
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(buttons))

    app.run_polling()


if __name__ == "__main__":
    main()
  
