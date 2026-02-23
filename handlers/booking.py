ADMIN_ID = 1071317313

async def send_tariff_request(update, context, tariff_name):
    query = update.callback_query
    await query.answer()

    user = query.from_user

    print("Заявка вызвана")

    await query.message.reply_text(
        f"✨ Вы выбрали: {tariff_name}\n\n"
        "Я скоро свяжусь с вами 💫"
    )
    
    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"🔥 Новая заявка\n\n"
                f"Тариф: {tariff_name}\n"
                f"Имя: {user.first_name}\n"
                f"Username: @{user.username}\n"
                f"ID: {user.id}"
            )
        )
        print("Сообщение админу отправлено")

    except Exception as e:
        print("Ошибка отправки админу:", e)