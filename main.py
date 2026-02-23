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
from handlers.booking import send_tariff_request
from handlers.menu_handlers import (
    show_tariffs,
    tariff_basic,
    tariff_pro,
    tariff_vip,
    tariff_question
)
from handlers.mini_analysis import (
    start_consultation,
    get_cons_name,
    get_cons_date,
    finish_consultation,
    CONS_NAME,
    CONS_DATE,
    CONS_REQUEST
)

async def start(update, context):
    await show_screen(update.effective_chat.id, context, "main_menu")

async def buttons(update, context):
    query = update.callback_query
    await query.answer()

    action = query.data

    if action == "mini_analysis":
        return await start_mini(update, context)
    
    if action in [
        "tariff_basic",
        "tariff_pro",
        "tariff_vip",
        "tariff_question",
        "tariffs"
    ]:
        return

    await show_screen(update.effective_chat.id, context, action)

def main():
    print("Бот запущен и ждёт сообщений")

    app = ApplicationBuilder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_mini, pattern="mini_analysis")],
        states={

            NAME: [
                MessageHandler(filters.TEXT, get_name),
                CallbackQueryHandler(cancel_mini, pattern="cancel_mini")
            ],

            DATE: [
                MessageHandler(filters.TEXT, get_date),
                CallbackQueryHandler(retry_date, pattern="retry_date"),
                CallbackQueryHandler(cancel_mini, pattern="cancel_mini")
            ],

            REQUEST: [
                MessageHandler(filters.TEXT, get_request),
                CallbackQueryHandler(cancel_mini, pattern="cancel_mini")
            ],

            "TOPIC": [
                CallbackQueryHandler(topic_selected, pattern="topic_")
            ],                                   
        },
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)

    consult_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_consultation, pattern="^consultation$")
        ],
        states={
            CONS_NAME: [MessageHandler(filters.TEXT, get_cons_name)],
            CONS_DATE: [MessageHandler(filters.TEXT, get_cons_date)],
            CONS_REQUEST: [MessageHandler(filters.TEXT, finish_consultation)],
        },
        fallbacks=[]
    )

    app.add_handler(consult_conv)
    app.add_handler(CallbackQueryHandler(show_tariffs, pattern="tariffs"))
    app.add_handler(CallbackQueryHandler(tariff_basic, pattern="tariff_basic"))
    app.add_handler(CallbackQueryHandler(tariff_pro, pattern="tariff_pro"))
    app.add_handler(CallbackQueryHandler(tariff_vip, pattern="tariff_vip"))
    app.add_handler(CallbackQueryHandler(tariff_question, pattern="tariff_question"))
    app.add_handler(CallbackQueryHandler(start_consultation, pattern="^consultation$"))
    app.add_handler(CallbackQueryHandler(buttons))

    app.run_polling()


if __name__ == "__main__":
    main()
  
