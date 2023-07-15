from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

check_reg = InlineKeyboardMarkup(row_width=2)
check_reg.add(InlineKeyboardButton(text="Да", callback_data="reg_yes"),
              InlineKeyboardButton(text="Нет", callback_data="reg_no"))

agree_admin_reg = InlineKeyboardMarkup(row_width=1)
agree_admin_reg.add(InlineKeyboardButton(text="Регистрировать учителя", callback_data="confirm_admin_reg"),
                    InlineKeyboardButton(text="Удалить сообщение", callback_data="delete_admin_reg"))

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add("/Новый абонемент").add("/Учёт уроков").add("/Создать студента").add("/Изменение студента").add(
    "/Удалить студента").add("/Удалить учителя").add("/Посмотреть студента").add("/Посмотреть абонемент").add(
    "/Мои ученики")

count_lessons = InlineKeyboardMarkup(row_width=3)
count_lessons.add(InlineKeyboardButton(text="4", callback_data="lessons_4"),
                  InlineKeyboardButton(text="8", callback_data="lessons_8"),
                  InlineKeyboardButton(text="12", callback_data="lessons_12"))

confirm_ticket = InlineKeyboardMarkup(row_width=2)
confirm_ticket.add(InlineKeyboardButton(text="Да", callback_data="confirm_ticket"),
                   InlineKeyboardButton(text="Нет", callback_data="not_confirm_ticket"))

teacher_panel = ReplyKeyboardMarkup(resize_keyboard=True)
teacher_panel.add("/Учёт уроков").add("/Посмотреть студента").add("/Посмотреть абонемент").add(
    "/Мои ученики")