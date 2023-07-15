from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from data.logging import logger
from data.config import dp, bot, db
from filters.is_admin import IsAdmin
from keyboards.keyboards import admin_panel, count_lessons


class FSMcreateStudent(StatesGroup):
    name = State()
    code = State()
    language = State()
    city = State()
    age = State()
    level = State()
    telephone = State()
    link = State()
    goal = State()
    form = State()
    dateArrival = State()
    comment = State()
    status = State()
    teacher = State()


class FSMEditStudent(StatesGroup):
    code = State()
    question = State()
    data = State()


class FSMcheckStudent(StatesGroup):
    code = State()


class FSMcheckTicket(StatesGroup):
    code = State()


class FSMcreateTicket(StatesGroup):
    code = State()
    count = State()
    date = State()


class FSMAccountingLessons(StatesGroup):
    code = State()
    lesson = State()


class FSMDeleteStudent(StatesGroup):
    code = State()
    confirm = State()


class FSMDeleteTeacher(StatesGroup):
    name = State()
    confirm = State()


@dp.message_handler(IsAdmin(), commands=["start"])
async def start(message: types.Message):

    """Хендлер для начала работы бота"""
    await bot.send_message(message.chat.id, "Добро пожаловать, Елизавета!", reply_markup=admin_panel)


@dp.message_handler(IsAdmin(), text=["/Создать студента"])
async def create_student(message: types.Message):

    """Хендлер для создания ученика"""

    await message.answer("Введите фамилию и имя ученика")
    await FSMcreateStudent.name.set()


@dp.message_handler(IsAdmin(), state="*", commands="отмена")
@dp.message_handler(Text(equals="отмена", ignore_case=True), state="*")
async def cancelFSM_handler(message: types.Message, state: FSMContext):

    """Хендлер для отмены функций, где есть FSM"""

    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Отменил")


@dp.message_handler(state=FSMcreateStudent.name)
async def nameFSM_createStudent(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text

    await FSMcreateStudent.next()
    await message.answer("Введите код ученика")


@dp.message_handler(state=FSMcreateStudent.code)
async def codeFSM_createStudent(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["code"] = message.text

    query_db = db.fetchone("SELECT * FROM students WHERE code=(%s)", (data["code"],))

    if query_db is None:
        await FSMcreateStudent.next()
        await message.answer("Введите язык ученика")
    else:
        await message.answer("Ученик с таким id уже есть")
        await state.finish()


@dp.message_handler(state=FSMcreateStudent.language)
async def languageFSM_createStudent(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["language"] = message.text

    await FSMcreateStudent.next()
    await message.answer("Введите город ученика")


@dp.message_handler(state=FSMcreateStudent.city)
async def cityFSM_createStudent(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["city"] = message.text

    await FSMcreateStudent.next()
    await message.answer("Введите возраст ученика")


@dp.message_handler(state=FSMcreateStudent.age)
async def ageFSM_createStudent(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["age"] = message.text

    await FSMcreateStudent.next()
    await message.answer("Введите уровень ученика")


@dp.message_handler(state=FSMcreateStudent.level)
async def levelFSM_createStudent(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["level"] = message.text

    await FSMcreateStudent.next()
    await message.answer("Введите телефон ученика")


@dp.message_handler(state=FSMcreateStudent.telephone)
async def telephoneFSM_createStudent(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["telephone"] = message.text

    await FSMcreateStudent.next()
    await message.answer("Введите цель ученика")


@dp.message_handler(state=FSMcreateStudent.link)
async def linkFSM_createStudent(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["link"] = message.text

    await FSMcreateStudent.next()
    await message.answer("Введите соц. сеть ученика")


@dp.message_handler(state=FSMcreateStudent.goal)
async def goalFSM_createStudent(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["goal"] = message.text

    await FSMcreateStudent.next()
    await message.answer("Введите форму обучения ученика")


@dp.message_handler(state=FSMcreateStudent.form)
async def formFSM_createStudent(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["form"] = message.text

    await FSMcreateStudent.next()
    await message.answer("Введите дату прихода ученика")


@dp.message_handler(state=FSMcreateStudent.dateArrival)
async def dateFSM_createStudent(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["dateArrival"] = message.text

    await FSMcreateStudent.next()
    await message.answer("Введите комментарий")


@dp.message_handler(state=FSMcreateStudent.comment)
async def commentFSM_createStudent(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["comment"] = message.text

    await FSMcreateStudent.next()
    await message.answer("Введите статус ученика")


@dp.message_handler(state=FSMcreateStudent.status)
async def statusFSM_createStudent(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["status"] = message.text

    await FSMcreateStudent.next()
    await message.answer("Введите учителя ученика")


@dp.message_handler(state=FSMcreateStudent.teacher)
async def teacherFSM_createStudent(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["teacher"] = message.text

            db.query("INSERT INTO students (name, code, language, city, age, level, telephone, link, goal, form, "
                     "dateArrival, comment, status, teacher) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                     "%s, %s)",
                     (data["name"], data["code"], data["language"], data["city"], data["age"], data["level"],
                      data["telephone"], data["goal"], data["link"], data["form"], data["dateArrival"],
                      data["comment"], data["status"], data["teacher"]))

        await message.answer("Готово! Ученик создан")
    except Exception as error:
        logger.error(f"Ошибка с FSMcreateStudent: {error}")
        await message.answer("Что-то пошло не так. Сообщение разработчику уже выслано")
        await bot.send_message(1371636236, f"Ошибка с созданием ученика: {error}")
    finally:
        await state.finish()


@dp.message_handler(IsAdmin(), text=["/Изменение студента"])
async def edit_student(message: types.Message):
    await message.answer("Введите код ученика")
    await FSMEditStudent.code.set()


@dp.message_handler(state=FSMEditStudent.code)
async def codeFSMEdit_student(message: types.Message, state: FSMContext):

    """Функция для изменения информации об ученике"""

    async with state.proxy() as data:
        data["code"] = message.text

    data_db = db.fetchone("SELECT * FROM students WHERE code=(%s)", (data["code"],))

    if data_db is None:
        await message.answer("Ученика с таким кодом нет.")
        await state.finish()
    else:
        await FSMEditStudent.next()
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
                             f"\nУчитель: {data_db['teacher']}"
                             f"\n"
                             f"\nЧто хотите изменить?")


@dp.message_handler(state=FSMEditStudent.question)
async def questionFSMEdit_student(message: types.Message, state: FSMContext):
    """Функция для изменения информации об ученике"""

    async with state.proxy() as data:
        data["question"] = message.text.lower()

    await FSMEditStudent.next()
    await message.answer("Введите данные")


@dp.message_handler(state=FSMEditStudent.data)
async def dataFSMEdit_student(message: types.Message, state: FSMContext):

    """Функция для записи обновленной информации об ученике"""

    async with state.proxy() as data:
        data["data"] = message.text

    if data["question"] == "имя":
        db.query("UPDATE students SET name=(%s)", (data["data"],))
        await message.answer("Готово!")
    elif data["question"] == "код ученика":
        db.query("UPDATE students SET code=(%s)", (data["data"],))
        await message.answer("Готово!")
    elif data["question"] == "язык":
        db.query("UPDATE students SET language=(%s)", (data["data"],))
        await message.answer("Готово!")
    elif data["question"] == "город":
        db.query("UPDATE students SET city=(%s)", (data["data"],))
        await message.answer("Готово!")
    elif data["question"] == "возраст":
        db.query("UPDATE students SET age=(%s)", (data["data"],))
        await message.answer("Готово!")
    elif data["question"] == "уровень":
        db.query("UPDATE students SET level=(%s)", (data["data"],))
        await message.answer("Готово!")
    elif data["question"] == "телефон":
        db.query("UPDATE students SET telephone=(%s)", (data["data"],))
        await message.answer("Готово!")
    elif data["question"] == "ссылка на соцсети":
        db.query("UPDATE students SET link=(%s)", (data["data"],))
        await message.answer("Готово!")
    elif data["question"] == "цель":
        db.query("UPDATE students SET goal=(%s)", (data["data"],))
        await message.answer("Готово!")
    elif data["question"] == "форма обучения":
        db.query("UPDATE students SET form=(%s)", (data["data"],))
        await message.answer("Готово!")
    elif data["question"] == "дата прихода":
        db.query("UPDATE students SET dateArrival=(%s)", (data["data"],))
        await message.answer("Готово!")
    elif data["question"] == "комментарий":
        db.query("UPDATE students SET comment=(%s)", (data["data"],))
        await message.answer("Готово!")
    elif data["question"] == "статус":
        db.query("UPDATE students SET status=(%s)", (data["data"],))
        await message.answer("Готово!")
    elif data["question"] == "учитель":
        db.query("UPDATE students SET teacher=(%s)", (data["data"],))
        await message.answer("Готово!")
    else:
        await message.answer("Неверный запрос")

    await state.finish()


@dp.message_handler(IsAdmin(), text=["/Посмотреть студента"])
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


@dp.message_handler(IsAdmin(), text=["/Новый абонемент"])
async def FSMcreate_ticket(message: types.Message):

    """Хендлер для создания нового абонемента для ученика"""

    await FSMcreateTicket.code.set()
    await message.answer("Введите код ученика")


@dp.message_handler(state=FSMcreateTicket.code)
async def FSMcode_create_ticket(message: types.Message, state: FSMContext):

    """Функция для продолжения создания нового абонемента для ученика"""

    async with state.proxy() as data:
        data["code"] = message.text

    data_db = db.fetchone("SELECT * FROM students WHERE code=(%s)", (data["code"],))

    if data_db is None:
        await message.answer("Ученика с таким кодом нет")
        await state.finish()
    else:
        await FSMcreateTicket.next()
        await message.answer("Введите количество уроков", reply_markup=count_lessons)


@dp.callback_query_handler(text="lessons_4", state=FSMcreateTicket)
async def FSMCallback_create_ticket(call: types.CallbackQuery, state: FSMContext):

    """Хендлер для установления в новый абонемент кол-ва уроков"""

    async with state.proxy() as data:
        data["count"] = 4

    await FSMcreateTicket.next()
    await bot.delete_message(
        chat_id=call.from_user.id,
        message_id=call.message.message_id)
    await call.message.answer("Введите дату покупки абонемента")


@dp.callback_query_handler(text="lessons_8", state=FSMcreateTicket)
async def FSMCallback_create_ticket(call: types.CallbackQuery, state: FSMContext):

    """Хендлер для установления в новый абонемент кол-ва уроков"""

    async with state.proxy() as data:
        data["count"] = 8

    await FSMcreateTicket.next()
    await bot.delete_message(
        chat_id=call.from_user.id,
        message_id=call.message.message_id)
    await call.message.answer("Введите дату покупки абонемента")


@dp.callback_query_handler(text="lessons_12", state=FSMcreateTicket)
async def FSMCallback_create_ticket(call: types.CallbackQuery, state: FSMContext):

    """Хендлер для установления в новый абонемент кол-ва уроков"""

    async with state.proxy() as data:
        data["count"] = 12

    await FSMcreateTicket.next()
    await bot.delete_message(
        chat_id=call.from_user.id,
        message_id=call.message.message_id)
    await call.message.answer("Введите дату покупки абонемента")


@dp.message_handler(state=FSMcreateTicket.date)
async def dateFSMcreate_ticket(message: types.Message, state: FSMContext):

    """Функция для добавления созданного абонемента в БД"""

    async with state.proxy() as data:
        data["date"] = message.text

    query = db.fetchone("SELECT * FROM seasonTickets WHERE code=(%s)", (data["code"]))

    try:
        if query is None:
            db.query("INSERT INTO seasonTickets (code, countLessons, dateBuy) VALUES (%s, %s, %s)",
                     (data["code"], data["count"], data["date"]))
        else:
            db.query("UPDATE seasonTickets SET code=%s, countLessons=%s, dateBuy=%s, classesHeld=NULL WHERE code=(%s)",
                     (data["code"], data["count"], data["date"], data["code"]))
    except Exception as error:
        logger.error(f"Ошибка с созданием абонемента: {error}")
        await message.answer("Не удалось создать абонемент. Сообщение разработчику уже выслано")
        await bot.send_message(1371636236, f"Ошибка с созданием абонемента: {error}")

    name_teacher = db.fetchone("SELECT teacher FROM students WHERE code=(%s)", (data["code"],))

    if name_teacher is None:
        await message.answer("У этого ученика нет учителя в базе данных")
    else:
        id_teacher = db.fetchone("SELECT tg_id FROM teachers WHERE fullname=(%s)", (name_teacher['teacher'],))

        if id_teacher is None:
            await message.answer("Абонемент создан")
            await message.answer("Сообщение учителю о добавлении абонемента ученика не было отправлено, т.к указанное "
                                 "имя учителя у ученика в базе данных не соответствует с учителями в базе данных ")
            await state.finish()
            return

        try:
            name_student = db.fetchone("SELECT name FROM students WHERE code=%s", (data["code"],))
            await bot.send_message(id_teacher['tg_id'], text=f"{name_student['name']} с кодом: {data['code']} купил("
                                                             f"а) абонемент ")

            await message.answer("Абонемент создан")

        except Exception as error:

            logger.error(f"Ошибка с отправкой информации о покупке абонемента: {error}")
            await message.answer("Что-то пошло не так c отправкой сообщения учителю. "
                                 "Сообщение разработчику уже выслано")
            await bot.send_message(1371636236, f"Ошибка с отправкой абонемента учителю: {error}")

    await state.finish()


@dp.message_handler(IsAdmin(), text=["/Посмотреть абонемент"])
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


@dp.message_handler(IsAdmin(), text=["/Удалить студента"])
async def delete_student(message: types.Message):
    await FSMDeleteStudent.code.set()
    await message.answer("Введите код ученика: ")


@dp.message_handler(state=FSMDeleteStudent.code)
async def delete_student_code(message: types.Message, state: FSMContext):

    """Функция для удаления ученика из БД"""

    async with state.proxy() as data:
        data["code"] = message.text

    result = db.fetchone("SELECT * FROM students WHERE code=(%s)", (data["code"],))

    if result is None:
        await message.answer("Ученика с таким кодом нет")
        await state.finish()
    else:
        await message.answer("Чтобы подтвердить удаление введите: 'Удаляй'")
        await FSMDeleteStudent.next()


@dp.message_handler(state=FSMDeleteStudent.confirm)
async def delete_student_confirm(message: types.Message, state: FSMContext):

    """Функция для подтверждения удаления ученика из БД"""

    async with state.proxy() as data:
        data["confirm"] = message.text

    if data["confirm"] == "Удаляй":
        db.query("DELETE FROM students WHERE code=(%s)", (data["code"],))
        db.query("DELETE FROM seasonTickets WHERE code=(%s)", (data["code"],))
        await message.answer("Удалил")
        await state.finish()
    else:
        await message.reply("Отменяю удаление")
        await state.finish()


@dp.message_handler(IsAdmin(), text=["/Удалить учителя"])
async def delete_teacher(message: types.Message):
    await FSMDeleteTeacher.name.set()
    await message.answer("Введите имя учителя: ")


@dp.message_handler(state=FSMDeleteTeacher.name)
async def delete_teacher_code(message: types.Message, state: FSMContext):

    """Функция для удаления учителя из БД"""

    async with state.proxy() as data:
        data["name"] = message.text

    result = db.fetchone("SELECT * FROM teachers WHERE fullname=(%s)", (data["name"],))

    if result is None:
        await message.answer("Учителя с таким именем нет")
        await state.finish()
    else:
        await message.answer("Чтобы подтвердить удаление введите: 'Удаляй'")
        await FSMDeleteTeacher.next()


@dp.message_handler(state=FSMDeleteTeacher.confirm)
async def delete_teacher_confirm(message: types.Message, state: FSMContext):

    """Функция для подтверждения удаления учителя из БД"""

    async with state.proxy() as data:
        data["confirm"] = message.text

    if data["confirm"] == "Удаляй":
        db.query("DELETE FROM teachers WHERE fullname=(%s)", (data["name"],))
        await message.answer("Удалил")
        await state.finish()
    else:
        await message.reply("Отменяю удаление")
        await state.finish()

