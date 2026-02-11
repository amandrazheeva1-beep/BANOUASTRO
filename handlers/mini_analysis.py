from telegram.ext import ConversationHandler, MessageHandler, filters
from database.models import save_user

NAME, DATE, REQUEST = range(3)


async def start_mini(update, context):
    await update.callback_query.message.reply_text("Введите имя")
    return NAME


async def get_name(update, context):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Введите дату рождения")
    return DATE


async def get_date(update, context):
    context.user_data["birthdate"] = update.message.text
    await update.message.reply_text("Введите запрос")
    return REQUEST


async def get_request(update, context):
    tg_id = update.effective_user.id

    save_user(
        tg_id,
        context.user_data["name"],
        context.user_data["birthdate"],
        update.message.text
    )

    await update.message.reply_text(
        "По вашей карте видно повторяющийся сценарий..."
    )

    return ConversationHandler.END
  
