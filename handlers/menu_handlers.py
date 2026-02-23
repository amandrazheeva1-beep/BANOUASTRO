import json
from keyboards.builder import build_keyboard
import config
from keyboards.builder import tariffs_keyboard
from handlers.booking import send_tariff_request

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

async def handle_menu_action(update, context):
    query = update.callback_query
    await query.answer()

    action = query.data

    if action in config.menu_data:
        section = config.menu_data[action]

        await query.message.reply_text(
            section["text"],
            reply_markup=build_keyboard(section.get("buttons", []))
        )
                                    
def tariffs_text():
        return """
        🌟 Тарифы БАНУАСТРО

        1️⃣ Базовый — «Ясность»
        Цена: 5 000₽

        Что входит:
        • Индивидуальный разбор по выбранной системе  
        • Анализ сильных и слабых сторон  
        • Рекомендации по развитию    

        Подходит тем, кто хочет получить первую ясную карту себя.

        ---

        2️⃣ Продвинутый — «Опора»
        Цена: 15 000₽

        Что входит:
        • Полный разбор системы БАНУАСТРО  
        • Анализ жизненных сценариев  
        • Практические рекомендации    
        • Письменный отчёт  
        • Поддержка 7 дней  

        Подходит для глубокого понимания себя.

        ---

        3️⃣ Флагманский — «Расширение»
        Цена: 35 000₽

        Что входит:
        • Полный разбор всех систем БАНУАСТРО  
        • Прогноз на год  
        • План личной стратегии    
        • Письменный отчёт  
        • Поддержка месяц  
        • Мини-разбор ситуаций  

        Подходит для максимальной глубины.

        ---

        💫 Разбор одного вопроса — 1000 ₽
        """

async def show_tariffs(update, context):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
    tariffs_text(),
    reply_markup=tariffs_keyboard()
    )

async def tariff_basic(update, context):
    await send_tariff_request(update, context, "Базовый — Ясность")


async def tariff_pro(update, context):
    await send_tariff_request(update, context, "Продвинутый — Опора")


async def tariff_vip(update, context):
    await send_tariff_request(update, context, "Флагманский — Расширение")


async def tariff_question(update, context):
    await send_tariff_request(update, context, "Разбор одного вопроса — 1000₽")