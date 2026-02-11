from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def build_keyboard(buttons):
    keyboard = [
        [InlineKeyboardButton(btn["title"], callback_data=btn["action"])]
        for btn in buttons
    ]

    return InlineKeyboardMarkup(keyboard)
  
