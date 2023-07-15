from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from data.logging import logger
from data.config import dp, bot, db
from filters.is_teacher import IsTeacher
from keyboards.keyboards import confirm_ticket, teacher_panel
import re
from datetime import datetime


class FSMSeasonTicket(StatesGroup):
    code = State()
    lesson = State()
    confirm = State()


class FSMcheckTicket(StatesGroup):
    code = State()


class FSMcheckStudent(StatesGroup):
    code = State()


@dp.message_handler(IsTeacher(), commands=["start"])
async def start(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, привет!", reply_markup=teacher_panel)


@dp.message_handler(IsTeacher(), state="*", commands="отмена")
@dp.message_handler(Text(equals="отмена", ignore_case=True), state="*")
async def cancelFSM_handler(message: types.Message, state: FSMContext):

    """Хендлер для отмены функций, где есть FSM"""

    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Отменил")


@dp.message_handler(IsTeacher(), text=["/Учёт уроков"])
async def FSMcode_accounting_lesson(message: types.Message):
    await FSMSeasonTicket.code.set()
    await message.answer("Введите код ученика")


@dp.message_handler(state=FSMSeasonTicket.code)
async def FSMload_code_seasonTickets(message: types.Message, state: FSMContext):

    """Функция для вывода информации о проведенных уроках и записи проведенного урока в бд"""

    async with state.proxy() as data:
        data["code"] = message.text

    get_from_students = db.fetchone("SELECT * FROM students WHERE code=(%s)", (data["code"],))

    if get_from_students is None:
        await message.answer("Ученика с таким кодом нет")
        await state.finish()
    else:
        get_ticket = db.fetchone("SELECT * FROM seasonTickets WHERE code=(%s)", (data["code"],))

        if get_ticket is None:
            await message.answer("У этого ученика нет абонемента")
            await state.finish()
        else:
            if get_ticket["classesHeld"] is None:
                await message.answer(f"{get_from_students['code']} {get_from_students['name']}"
                                     f"\nКуплено уроков: {get_ticket['countLessons']}"
                                     f"\nДата покупки абонемента: {get_ticket['dateBuy']}"
                                     f"\nПроведенных уроков ещё не было"
                                     f"\n"
                                     f"\nВведите проведённый урок")
                await FSMSeasonTicket.next()
            else:
                classesHeld = get_ticket['classesHeld'].split(", ")
                for ind, value in enumerate(classesHeld):
                    classesHeld[ind] = value + "\n"

                await message.answer(f"{get_from_students['code']} {get_from_students['name']}"
                                     f"\nКуплено уроков: {get_ticket['countLessons']}"
                                     f"\nДата покупки абонемента: {get_ticket['dateBuy']}"
                                     f"\nПроведенные уроки: \n{''.join(classesHeld)}"
                                     f"\n"
                                     f"Введите проведённый урок")

                await FSMSeasonTicket.next()


@dp.message_handler(state=FSMSeasonTicket.lesson)
async def FSMload_lesson_seasonTickets(message: types.Message, state: FSMContext):

    """Функция для подтверждения записи проведенного урок"""

    async with state.proxy() as data:
        data["lesson"] = message.text

    pattern = r"У\d{1,2}/\d{1,2}.\d{1,2}.\w+"
    result = re.search(pattern, data["lesson"])
    count_lesson = db.fetchone("SELECT countLessons FROM seasonTickets WHERE code=(%s)", (data["code"],))

    pattern2 = r"(?<=У)\d{1,2}(?=/)"
    check_len = re.search(pattern2, data['lesson'])
    if result and int(check_len.group()) <= int(count_lesson['countLessons']):
        await message.answer("Подтвердить отправку?", reply_markup=confirm_ticket)
        await FSMSeasonTicket.next()
    else:
        await message.answer("Неправильно введен урок. Пример: У1/8 6 апреля")
        await state.finish()


@dp.callback_query_handler(text="confirm_ticket", state=FSMSeasonTicket)
async def callback_register_teacher_admin(call: types.CallbackQuery, state: FSMContext):

    """Callback для записи в бд проведенного урока"""

    try:
        async with state.proxy() as data:
            await bot.delete_message(
                chat_id=call.from_user.id,
                message_id=call.message.message_id)

            value = db.fetchone("SELECT classesHeld FROM seasonTickets WHERE code=(%s);", (data["code"],))

            if value['classesHeld'] is None:

                db.query("UPDATE seasonTickets SET classesHeld=(%s) WHERE code=(%s);", (data["lesson"], data["code"]))
                await call.message.answer("Урок сохранён")

                student_info = db.fetchone("SELECT language FROM students WHERE code=(%s)", (data["code"],))

                date = datetime.today().strftime('%d.%m.%Y')
                db.query("INSERT INTO lessonsHistory (code, date, lesson_code) VALUES "
                         "(%s, %s, %s)", (data["code"], date, student_info['language']))
            else:

                result_value = f"{value['classesHeld']}, {data['lesson']}"

                db.query("UPDATE seasonTickets SET classesHeld=(%s) WHERE code=(%s);",
                         (f"{result_value}", data["code"]))

                count_lesson = db.fetchone("SELECT countLessons FROM seasonTickets WHERE code=(%s)", (data["code"],))
                student_info = db.fetchone("SELECT name, teacher, language FROM students WHERE code=(%s)",
                                           (data["code"],))
                teacher_info = db.fetchone("SELECT fullname, codeLanguage FROM teachers WHERE fullname=(%s)",
                                           (student_info['teacher'],))

                date = datetime.today().strftime('%d.%m.%Y')
                db.query("INSERT INTO lessonsHistory (code, date, lesson_code) VALUES "
                         "(%s, %s, %s)", (data["code"], date, student_info['language']))

                pattern = r"(?<=У)\d{1,2}(?=/)"
                check_len = re.search(pattern, data["lesson"])

                if int(check_len.group()) in (4, 8, 12):
                    await bot.send_message(1656621614, f"Код ученика: {data['code']}, имя: {student_info['name']}"
                                                       f"\nКод учителя: {teacher_info['codeLanguage']}, "
                                                       f"имя: {teacher_info['fullname']}"
                                                       f"\nЛиза, оплати четыре урока.")
                    await call.message.answer("Четыре урока состоялось, ожидайте оплаты.")

                if int(check_len.group()) == count_lesson['countLessons']:
                    db.query("DELETE FROM seasonTickets WHERE code=(%s)", (data["code"],))
                    await bot.send_message(1656621614, f"Абонемент закончился у ученика с кодом: {data['code']} "
                                                       f"{student_info['name']}")
                    await call.message.answer("Последний урок сохранён, абонемент закончился.")
                else:
                    await call.message.answer("Урок сохранён")

    except Exception as error:
        logger.error(f"Произошла ошибка с учётом урока: {error}")
        await call.message.answer("Что-то пошло не так. Сообщение разработчику уже выслано. Просьба передать "
                                  "проведенный урок в сообщения Елизавете")
        await bot.send_message(1371636236, f"Ошибка с учётом уроков: {error}")
    finally:
        await state.finish()


@dp.callback_query_handler(text="not_confirm_ticket", state=FSMSeasonTicket)
async def callback_register_teacher_admin(callback_query: types.CallbackQuery, state: FSMContext):

    """Callback для отмены записи проведенного урока"""

    await bot.delete_message(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id)
    await callback_query.message.answer("Отменил")
    await state.finish()


@dp.message_handler(IsTeacher(), text=["/Посмотреть абонемент"])
async def check_ticket(message: types.Message):
    await FSMcheckTicket.code.set()
    await message.answer("Введите код ученика")


@dp.message_handler(state=FSMcheckTicket.code)
async def FSMcheck_ticket_load(message: types.Message, state: FSMContext):

    """Функция для просмотра абонемента ученика"""

    async with state.proxy() as data:
        data["code"] = message.text

    data_db = db.fetchone("SELECT * FROM students WHERE code=(%s)", (data["code"],))

    if data_db is None:
        await message.answer("Ученика с таким кодом нет")
        await state.finish()
    else:
        query = db.fetchone("SELECT * FROM seasonTickets WHERE code=(%s)", (data["code"],))

        if query is None:
            await message.answer("У этого ученика закончился абонемент или его вовсе нет")
            await state.finish()
        else:
            if query['classesHeld'] is None:
                await message.answer(f"\nКуплено уроков: {query['countLessons']}"
                                     f"\nДата покупки абонемента: {query['dateBuy']}"
                                     f"\nПроведенных уроков ещё не было")
            else:
                classesHeld = query['classesHeld'].split(", ")
                for ind, value in enumerate(classesHeld):
                    classesHeld[ind] = value + "\n"

                await message.answer(f"\nКуплено уроков: {query['countLessons']}"
                                     f"\nДата покупки абонемента: {query['dateBuy']}"
                                     f"\nПроведенные уроки: \n{''.join(classesHeld)}")

            await state.finish()


@dp.message_handler(IsTeacher(), text=["/Посмотреть студента"])
async def edit_student(message: types.Message):
    await FSMcheckStudent.code.set()
    await message.answer("Введите код ученика")


@dp.message_handler(state=FSMcheckStudent.code)
async def FSMcheck_student(message: types.Message, state: FSMContext):

    """Функция для просмотра информации об ученике"""

    async with state.proxy() as data:
        data["code"] = message.text

    data_db = db.fetchone("SELECT * FROM students WHERE code=(%s)", (data["code"],))

    if data_db is None:
        await message.answer("Ученика с таким кодом нет")
        await state.finish()
    else:
        await message.answer(f"Данные ученика: \n"
                             f"\nИмя: {data_db['name']}"
                             f"\nКод ученика: {data_db['code']}"
                             f"\nЯзык: {data_db['language']}"
                             f"\nГород: {data_db['city']}"
                             f"\nВозраст: {data_db['age']}"
                             f"\nУровень: {data_db['level']}"
                             f"\nТелефон: {data_db['telephone']}"
                             f"\nСсылка на соцсети: {data_db['link']}"
                             f"\nЦель: {data_db['goal']}"
                             f"\nФорма обучения: {data_db['form']}"
                             f"\nДата прихода: {data_db['dateArrival']}"
                             f"\nКомментарий: {data_db['comment']}"
                             f"\nСтатус: {data_db['status']}"
                             f"\nУчитель: {data_db['teacher']}")

        await state.finish()


@dp.message_handler(IsTeacher(), text=["/Мои ученики"])
async def my_students(message: types.Message):

    """Хендлер для просмотра своих учеников"""

    info_teacher = db.fetchone("SELECT * FROM teachers WHERE tg_id=(%s)", (message.from_user.id,))
    students = db.fetchall("SELECT name, code FROM students WHERE teacher=(%s)", (info_teacher['fullname'],))

    if len(students) == 0:
        await message.answer("У вас нет учеников")
    else:
        result = ""
        for i in students:
            result = f"{result}{i['name']}, код: {i['code']}\n"

        await message.answer(f"Ваши ученики: \n{result}")
