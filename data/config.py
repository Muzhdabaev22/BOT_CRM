import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv, find_dotenv
from data.database import DatabaseManagerSQL
from aiogram.contrib.fsm_storage.memory import MemoryStorage

if not find_dotenv():
    exit('Переменные окружения не загружены')
else:
    load_dotenv()

TOKEN = os.getenv("TOKEN_BOT")
host = os.getenv("HOST")
user = os.getenv("USER")
port = 3306
password = os.getenv("PASSWORD")
db_name = os.getenv("DB_NAME")


storage = MemoryStorage()

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)

admins = ["admin_id"]

db = DatabaseManagerSQL(host=host, port=port, user=user, password=password, db_name=db_name)
