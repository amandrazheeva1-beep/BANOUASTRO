from telegram.ext import ConversationHandler
from datetime import datetime
import random
from database.models import save_user
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from handlers.booking import ADMIN_ID



# ===== СТЕЙТЫ ДИАЛОГА =====
NAME, DATE, REQUEST = range(3)

def control_keyboard():
    return InlineKeyboardMarkup([
    [InlineKeyboardButton("⬅️ Главное меню", callback_data="main_menu")],
    [InlineKeyboardButton("❌ Отменить разбор", callback_data="cancel_mini")]
    ])

REQUEST_TOPICS = {
    "money": "💰 Деньги",
    "love": "❤️ Отношения",
    "career": "🚀 Реализация",
    "purpose": "🌟 Предназначение"
}

ENERGY_DATA = {
    1: {
        "name": "Энергия лидера",
        "strength": "способность запускать процессы и вести людей",
        "risk": "перегруз ответственностью и давление на себя"
    },
    2: {
        "name": "Энергия партнёрства",
        "strength": "тонкое чувствование людей и дипломатия",
        "risk": "зависимость от мнения окружающих"
    },
    3: {
        "name": "Энергия творчества",
        "strength": "харизма и способность вдохновлять",
        "risk": "распыление энергии"
    },
    4: {
        "name": "Энергия стабильности",
        "strength": "умение строить систему и доводить до результата",
        "risk": "жёсткость и страх перемен"
    },
    5: {
        "name": "Энергия свободы",
        "strength": "гибкость и умение быстро адаптироваться",
        "risk": "потеря фокуса"
    },
    6: {
        "name": "Энергия любви",
        "strength": "способность создавать гармоничные отношения",
        "risk": "жертвенность"
    },
    7: {
        "name": "Энергия мудрости",
        "strength": "глубокий анализ и духовный поиск",
        "risk": "закрытость и уход в себя"
    },
    8: {
        "name": "Энергия реализации",
        "strength": "управление ресурсами и материальный успех",
        "risk": "контроль и эмоциональная жёсткость"
    }
}


SCENARIOS = [
    "В жизни могут повторяться ситуации, где нужно научиться выбирать себя.",
    "Часто судьба будет ставить перед выбором между стабильностью и ростом.",
    "Жизнь может подталкивать к раскрытию таланта через испытания."
]
                
def extended_banuastro_reading(name, birthdate, request):

    try:
        date = datetime.strptime(birthdate, "%d.%m.%Y")
        energy = (date.day + date.month + date.year) % 8 + 1

        data = ENERGY_DATA[energy]
        scenario = random.choice(SCENARIOS)

        return f"""
{name}, я посмотрела вашу карту по методике БАНУАСТРО 🔮

🌟 Ваша базовая энергия — {data['name']}

Это говорит о том, что у вас заложен сильный потенциал через:
👉 {data['strength']}

Но также карта показывает возможную зону напряжения:
⚠️ {data['risk']}

💫 Внутренний сценарий карты:
{scenario}

Ваш запрос:
«{request}»

Он напрямую связан с задачами вашей энергии.  
Часто именно через такие темы раскрывается предназначение человека.

✨ Сейчас это только мини-анализ карты.
В полном разборе я смотрю глубинные сценарии, отношения, предназначение и точки роста.
"""
    except:
        return "Ошибка чтения даты. Используйте формат ДД.ММ.ГГГГ"


def consultation_offer():
    return """
Если чувствуете отклик — вы можете записаться на полный персональный разбор.

На консультации я подробно разбираю:
✨ жизненные сценарии
✨ предназначение
✨ отношения и повторяющиеся ситуации
✨ сильные стороны и точки роста

Напишите «Консультация», чтобы узнать детали.
"""

async def start_mini(update, context):

    await update.callback_query.message.reply_text(
        "🔮 Мини-разбор БАНУАСТРО\n\n"
        "Шаг 1 из 3\n"
        "Введите имя",
        reply_markup=control_keyboard()
    )
    return NAME


async def cancel_mini(update, context):

    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "Разбор остановлен. Вы можете начать заново через меню."
    )

    context.user_data.clear()

    return ConversationHandler.END


async def get_name(update, context):

    context.user_data["name"] = update.message.text

    await update.message.reply_text(
        "Шаг 2 из 3\nВведите дату рождения (ДД.ММ.ГГГГ)",
        reply_markup=control_keyboard()
    )

    return DATE


async def get_date(update, context):

    birthdate = update.message.text

    try:
        datetime.strptime(birthdate, "%d.%m.%Y")
    except:
        await update.message.reply_text(
            "❌ Неверный формат даты\nВведите ДД.ММ.ГГГГ",
            reply_markup=control_keyboard()
        )
        return DATE

    context.user_data["birthdate"] = birthdate

    await update.message.reply_text(
        "Шаг 3 из 3\nВведите ваш запрос",
        reply_markup=control_keyboard()
    )

    return REQUEST
        

async def retry_date(update, context):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
    "Введите дату рождения в формате ДД.ММ.ГГГГ"
    )

    return DATE
      
async def get_request(update, context):

    tg_id = update.effective_user.id
    name = context.user_data["name"]
    birthdate = context.user_data["birthdate"]
    request = update.message.text

    save_user(tg_id, name, birthdate, request)

async def get_request(update, context):

    context.user_data["request"] = update.message.text

    keyboard = [
        [InlineKeyboardButton("💰 Деньги", callback_data="topic_money")],
        [InlineKeyboardButton("❤️ Отношения", callback_data="topic_love")],
        [InlineKeyboardButton("🚀 Реализация", callback_data="topic_career")],
        [InlineKeyboardButton("🌟 Предназначение", callback_data="topic_purpose")]
    ]

    await update.message.reply_text(
        "Выберите основную тему вашего запроса:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return "TOPIC"

def topic_analysis(topic):

    if topic == "money":
        return """
💰 Тема денег показывает, как человек взаимодействует с ресурсами.

В карте часто деньги связаны не только с работой,
а с внутренним ощущением ценности себя.

Если в энергии есть напряжение — человек может:
• занижать стоимость своего труда
• бояться больших доходов
• входить в нестабильные проекты

Когда энергия раскрывается — деньги приходят через сильные стороны личности.
"""

    if topic == "love":
        return """
❤️ Тема отношений показывает сценарии взаимодействия с партнёрами.

Карта может показывать:
• повторяющиеся типажи партнёров
• страх близости
• склонность к жертвенности

Отношения часто становятся зеркалом личного роста.
"""

    if topic == "career":
        return """
🚀 Тема реализации показывает, через какую деятельность человек раскрывается.

Карта может указывать:
• формат работы
• тип среды
• стиль лидерства
• формат заработка
"""

    if topic == "purpose":
        return """
🌟 Предназначение показывает направление развития личности.

Это не профессия, а способ проявления энергии через жизнь.
"""

async def topic_selected(update, context):

    query = update.callback_query
    await query.answer()

    topic = query.data.replace("topic_", "")

    name = context.user_data["name"]
    birthdate = context.user_data["birthdate"]
    request = context.user_data["request"]

    base_reading = extended_banuastro_reading(name, birthdate, request)
    topic_text = topic_analysis(topic)

    await query.message.reply_text(base_reading)
    await query.message.reply_text(topic_text)
    await query.message.reply_text(consultation_offer())

    return ConversationHandler.END

CONS_NAME, CONS_DATE, CONS_REQUEST = range(100, 103)

async def start_consultation(update, context):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text("Введите ваше имя:")
    return CONS_NAME

async def get_cons_name(update, context):
    context.user_data["cons_name"] = update.message.text
    await update.message.reply_text("Введите дату рождения (ДД.ММ.ГГГГ):")
    return CONS_DATE


async def get_cons_date(update, context):
    context.user_data["cons_date"] = update.message.text
    await update.message.reply_text("Опишите ваш запрос:")
    return CONS_REQUEST

async def finish_consultation(update, context):
    print("FINISH CONSULTATION ВЫЗВАН")

    user = update.message.from_user

    context.user_data["cons_request"] = update.message.text

    name = context.user_data.get("cons_name")
    date = context.user_data.get("cons_date")
    request = context.user_data.get("cons_request")

    print("Данные:", name, date, request)

    await update.message.reply_text(
        "✨ Заявка отправляется..."
    )

    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                "🔥 Новая запись на консультацию\n\n"
                f"Имя: {name}\n"
                f"Дата: {date}\n"
                f"Запрос: {request}\n"
                f"Username: @{user.username}\n"
                f"ID: {user.id}"
            )
        )
        print("Сообщение админу отправлено")

    except Exception as e:
        print("ОШИБКА:", e)

    await update.message.reply_text(
        "✅ Заявка отправлена!"
    )

    context.user_data.clear()

    return ConversationHandler.END