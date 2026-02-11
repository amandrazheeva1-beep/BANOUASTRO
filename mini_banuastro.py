from datetime import datetime


# ===== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =====

def calculate_core_number(day, month, year):
    return (day + month + year) % 9


def calculate_purpose_number(day, month):
    return (day * month) % 9


def calculate_year_energy(birth_day, birth_month, current_year):
    return (birth_day + birth_month + current_year) % 9


# ===== СПРАВОЧНИК ЭНЕРГИЙ =====

ENERGY_MEANINGS = {
    0: "Мощная трансформационная энергия",
    1: "Лидер, инициатор, человек действия",
    2: "Партнёрство, чувствительность, дипломатия",
    3: "Творчество, харизма, самовыражение",
    4: "Стабильность, система, ответственность",
    5: "Свобода, перемены, движение",
    6: "Любовь, семья, забота",
    7: "Духовность, анализ, поиск смысла",
    8: "Деньги, власть, реализация"
}


# ===== МИНИ РАЗБОР ЛИЧНОСТИ =====

def personality_analysis(date_str):
    try:
        date = datetime.strptime(date_str, "%d.%m.%Y")

        core = calculate_core_number(date.day, date.month, date.year)

        return f"""
✨ Мини-разбор личности БАНУАСТРО

Дата рождения: {date_str}

🌟 Базовая энергия личности:
{ENERGY_MEANINGS[core]}

Вы проявляете себя через эту энергию в жизни, отношениях и работе.
"""

    except:
        return "Введите дату в формате ДД.ММ.ГГГГ"


# ===== МИНИ РАЗБОР ПРЕДНАЗНАЧЕНИЯ =====

def purpose_analysis(date_str):
    try:
        date = datetime.strptime(date_str, "%d.%m.%Y")

        purpose = calculate_purpose_number(date.day, date.month)

        return f"""
💫 Мини-разбор предназначения

Ваш вектор предназначения:
{ENERGY_MEANINGS[purpose]}

Через эту энергию раскрывается ваш потенциал и миссия.
"""

    except:
        return "Введите дату в формате ДД.ММ.ГГГГ"


# ===== ЭНЕРГИЯ ГОДА =====

def year_energy_analysis(date_str):
    try:
        date = datetime.strptime(date_str, "%d.%m.%Y")

        current_year = datetime.now().year

        energy = calculate_year_energy(
            date.day,
            date.month,
            current_year
        )

        return f"""
📅 Энергия вашего {current_year} года

Главная тема года:
{ENERGY_MEANINGS[energy]}

Этот год будет раскрывать именно эту сферу жизни.
"""

    except:
        return "Введите дату в формате ДД.ММ.ГГГГ"


# ===== ПОЛНЫЙ МИНИ-РАЗБОР =====

def full_mini_reading(date_str):

    p1 = personality_analysis(date_str)
    p2 = purpose_analysis(date_str)
    p3 = year_energy_analysis(date_str)

    return f"""
{p1}

{p2}

{p3}

🔮 Это краткий разбор.
Для полного анализа напишите "Консультация"
"""
  
