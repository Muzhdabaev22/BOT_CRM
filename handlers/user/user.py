from data.logging import logger
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from data.config import dp, bot, db
from filters.is_user import IsUser
from keyboards.keyboards import check_reg, agree_admin_reg, teacher_panel


class FSMTeacherReg(StatesGroup):
    name_from_teacher = State()
    id_tg = State()
    name_teacher = State()
    language_code = State()


@dp.message_handler(IsUser(), commands=["start"])
async def start(message: types.Message):
    """Хендлер для начала работы бота"""

    logger.info(f'Вызвана функция {start.__name__} как юзер. ID того, кто вызвал: {message.chat.id}')
    await message.answer(f"Привет я бот Юнга и помогу тебе! \nХотите зарегистрировать как учитель?",
                         reply_markup=check_reg)


@dp.callback_query_handler(state=None)
async def callback_register_teacher(callback_query: types.CallbackQuery):
    """Callback для подтверждения регистрации учителя"""

    try:
        if callback_query.data == "reg_yes":

            await bot.edit_message_reply_markup(
                chat_id=callback_query.from_user.id,
                message_id=callback_query.message.message_id,
                reply_markup=None)
            await FSMTeacherReg.name_from_teacher.set()
            await bot.send_message(chat_id=callback_query.from_user.id, text="Введите ваше ФИО")

        elif callback_query.data == "reg_no":

            await bot.edit_message_reply_markup(
                chat_id=callback_query.from_user.id,
                message_id=callback_query.message.message_id,
                reply_markup=None)
            await bot.send_message(chat_id=callback_query.from_user.id, text="Похоже вы не учитель(")
    except Exception as error:
        logger.error(f"Ошибка с кнопками регистрации учителя: {error}")
        await bot.send_message(1371636236, f"Ошибка с кнопками в регистрации юзера: {error}")


@dp.message_handler(state=FSMTeacherReg.name_from_teacher)
async def load_name_from_user(message: types.Message, state: FSMContext):
    """Функция для отправки админу подтверждения на регистрацию"""

    try:
        async with state.proxy() as data:
            data["name_from_teacher"] = message.text
            data["id_tg"] = message.from_user.id

            await bot.send_message(chat_id=1656621614, text="Пришел запрос на регистрацию учителя. Отправитель: "
                                                            f"{data['name_from_teacher']}",
                                                            reply_markup=agree_admin_reg)
        await FSMTeacherReg.next()
        await message.answer("Всё прошло успешно! Ждите сообщение, когда вас зарегистрирует админ")

    except Exception as error:
        logger.error(f"Ошибка с FSM в load_name_from_user: {error}")
        await message.answer("Что-то пошло не так. Попробуйте снова ввести ФИО, вызвав команду /start")


@dp.callback_query_handler(text="confirm_admin_reg", state=FSMTeacherReg)
async def callback_register_teacher_admin(callback_query: types.CallbackQuery):
    """Callback для регистрации учителя админом"""

    await bot.delete_message(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id)
    await FSMTeacherReg.next()
    await bot.send_message(chat_id=callback_query.from_user.id, text="Введите фамилию и имя учителя через пробел")


@dp.callback_query_handler(text="delete_admin_reg", state=FSMTeacherReg)
async def callback_delete_message(callback_query: types.CallbackQuery, state: FSMContext):
    """Callback для отмены регистрации учителя админом"""

    await bot.delete_message(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id)
    await state.finish()


@dp.message_handler(state=FSMTeacherReg.name_teacher)
async def load_name_from_teacher(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name_teacher"] = message.text

    await FSMTeacherReg.next()
    await message.answer("Теперь введите код языка, например: 0 английский")


@dp.message_handler(state=FSMTeacherReg.language_code)
async def load_name_from_teacher(message: types.Message, state: FSMContext):
    """Функция для записи нового учителя в БД"""

    try:

        async with state.proxy() as data:
            data["language_code"] = message.text
            db.query("INSERT INTO teachers (fullname, codeLanguage, tg_id) VALUES (%s, %s, %s)",
                     (data["name_teacher"], data["language_code"], data["id_tg"]))

        await bot.send_message(data["id_tg"], "Вас зарегистрировали. Добро пожаловать!", reply_markup=teacher_panel)
        await message.answer("Всё прошло успешно")
        await state.finish()

    except Exception as error:
        logger.error(f"Ошибка с FSM или загрузкой данных об учителе в БД: {error}")
        await message.answer("Что-то пошло не так. Сообщение разработчику уже выслано")
        await bot.send_message(1371636236, f"Ошибка с загрузкой данных в БД об учителе: {error}")
