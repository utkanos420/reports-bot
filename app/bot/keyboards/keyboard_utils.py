from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_report_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Оставить заявку", callback_data="create_report")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()

def cancel_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Отменить", callback_data="cancel_report")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()

def skip_report_description():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Пропустить шаг", callback_data="skip_report_description")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def floors_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="1", callback_data="floor_1")
    keyboard_builder.button(text="2", callback_data="floor_2")
    keyboard_builder.button(text="3", callback_data="floor_3")
    keyboard_builder.button(text="4", callback_data="floor_4")
    keyboard_builder.adjust(3)
    return keyboard_builder.as_markup()


def floor_1_cabs():
    cabs = sorted([
        "1.08", "1.09", "1.10", "1.11", "1.12", "1.14",
        "1.16", "1.18", "1.19", "1.26", "1.27", "1.28",
        "1.29", "1.30", "1.31", "1.32", "1.40", "1.43"
    ], key=lambda x: [int(n) for n in x.split('.')])
    keyboard_builder = InlineKeyboardBuilder()
    for cab in cabs:
        keyboard_builder.button(text=cab, callback_data=f"cabinet_{cab}")
    keyboard_builder.adjust(4)
    return keyboard_builder.as_markup()


def floor_2_cabs():
    cabs = sorted([
        "2.1", "2.4", "2.8", "2.12", "2.13", "2.16", "2.17", "2.18", "2.20",
        "2.27", "2.28", "2.29", "2.30", "2.31", "2.32", "2.34", "2.35", "2.36",
        "2.37", "2.40", "2.41", "2.45", "2.46", "2.47", "2.48", "2.49", "2.50", "2.51", "2.52"
    ], key=lambda x: [int(n) for n in x.split('.')])
    keyboard_builder = InlineKeyboardBuilder()
    for cab in cabs:
        keyboard_builder.button(text=cab, callback_data=f"cabinet_{cab}")
    keyboard_builder.adjust(4)
    return keyboard_builder.as_markup()


def floor_3_cabs():
    cabs = sorted([
        "3.14", "3.16", "3.22", "3.29", "3.31", "3.32", "3.33", "3.34", "3.35",
        "3.36", "3.37", "3.38", "3.39", "3.40", "3.44", "3.50", "3.51", "3.53", "3.54"
    ], key=lambda x: [int(n) for n in x.split('.')])
    keyboard_builder = InlineKeyboardBuilder()
    for cab in cabs:
        keyboard_builder.button(text=cab, callback_data=f"cabinet_{cab}")
    keyboard_builder.adjust(4)
    return keyboard_builder.as_markup()


def floor_4_cabs():
    cabs = sorted([
        "4.2", "4.3", "4.5", "4.6", "4.8", "4.9", "4.12"
    ], key=lambda x: [int(n) for n in x.split('.')])
    keyboard_builder = InlineKeyboardBuilder()
    for cab in cabs:
        keyboard_builder.button(text=cab, callback_data=f"audience_{cab}")
    keyboard_builder.adjust(4)
    return keyboard_builder.as_markup()


def reason_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Карточки", callback_data="card")
    keyboard_builder.button(text="Оборудование", callback_data="devices")
    keyboard_builder.button(text="Настройка оборудования", callback_data="devices_soft")
    keyboard_builder.button(text="Другое", callback_data="other")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()
