from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def build_keyboard(buttons):
    keyboard = [
        [InlineKeyboardButton(btn["title"], callback_data=btn["action"])]
        for btn in buttons
    ]

    return InlineKeyboardMarkup(keyboard)

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔮 Мини-разбор", callback_data="mini_start")],
        [InlineKeyboardButton("📊 Тарифы БАНУАСТРО", callback_data="tariffs")],
        [InlineKeyboardButton("💬 Консультация", callback_data="consultation")]
    ])

def tariffs_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("1️⃣ Ясность", callback_data="tariff_basic")],
        [InlineKeyboardButton("2️⃣ Опора", callback_data="tariff_pro")],
        [InlineKeyboardButton("3️⃣ Расширение", callback_data="tariff_vip")],
        [InlineKeyboardButton("💫 Один вопрос — 1000₽", callback_data="tariff_question")],
        [InlineKeyboardButton("⬅️ Главное меню", callback_data="main_menu")]
    ])
  
