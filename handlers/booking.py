from config import ADMIN_ID

async def book(update, context):

    user = update.effective_user

    await context.bot.send_message(
        ADMIN_ID,
        f"Новая заявка от @{user.username}"
    )

    await update.callback_query.message.reply_text(
        "Заявка отправлена консультанту"
    )
  
