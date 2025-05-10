# Стартовый код Telegram-бота "WB Школа" с обучающим модулем

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InputFile
import logging
import os

API_TOKEN = os.getenv('API_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Главное меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("📘 Обучение"), KeyboardButton("💳 Оплатить доступ"))
main_menu.add(KeyboardButton("🛠 Поддержка"))

# Хранилище шагов пользователей
user_steps = {}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Привет! Добро пожаловать в WB Школу.\n\nЗдесь ты пройдёшь пошаговое обучение по торговле на Wildberries.", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "📘 Обучение")
async def course_access(message: types.Message):
    user_steps[message.from_user.id] = 1
    await send_lesson(message)

async def send_lesson(message):
    step = user_steps.get(message.from_user.id, 1)
    if step == 1:
        photo = InputFile("modul1.png")
        await message.answer_photo(photo, caption="Модуль 1: Регистрация ИП через Т-Банк.\n\nЗайдите на сайт https://www.tinkoff.ru/business/ и заполните анкету.\n\nПосле этого курьер приедет к вам в любой регион РФ.")
        await message.answer("Напишите 'Далее', чтобы перейти к следующему шагу.")
    elif step == 2:
        photo = InputFile("modul2.png")
        await message.answer_photo(photo, caption="Модуль 2: Подключение к Личному кабинету Wildberries.\n\nПерейдите на seller.wildberries.ru и создайте учётную запись с ИП.")
        await message.answer("Обучение завершено. Следующие модули скоро будут добавлены!")

@dp.message_handler(lambda message: message.text.lower() == "далее")
async def next_step(message: types.Message):
    user_id = message.from_user.id
    user_steps[user_id] = user_steps.get(user_id, 1) + 1
    await send_lesson(message)

@dp.message_handler(lambda message: message.text == "💳 Оплатить доступ")
async def buy_access(message: types.Message):
    await message.answer("Скоро здесь появится кнопка оплаты 💳\n(сейчас работает тестовый режим)")

@dp.message_handler(lambda message: message.text == "🛠 Поддержка")
async def support_info(message: types.Message):
    await message.answer("Если возникли вопросы, пиши сюда: @your_support")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
