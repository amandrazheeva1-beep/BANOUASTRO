import json
from keyboards.builder import build_keyboard

with open("menu.json", "r", encoding="utf-8") as f:
    MENU = json.load(f)


async def show_screen(chat_id, context, screen_name):

    if screen_name == "main_menu":
        screen = MENU["main_menu"]

    elif screen_name in MENU:
        screen = MENU[screen_name]

    elif "faq" in MENU and screen_name in MENU["faq"]:
        screen = MENU["faq"][screen_name]

    else:
        return

    await context.bot.send_message(
        chat_id=chat_id,
        text=screen["text"],
        reply_markup=build_keyboard(screen.get("buttons", []))
    )
  
