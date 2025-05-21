# bot.py — обновлённый код с учётом новой структуры
from aiogram import Bot, Dispatcher, types, executor
import logging, os

API_TOKEN = os.getenv('API_TOKEN')
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    text = (
        'Привет! Это твой вход в курс по ChatGPT.\n\n'
        '🚀 Начни с бесплатного урока\n'
        '📘 /lesson — Бесплатный урок\n'
        '💳 /buy — Оплатить курс\n'
        '🧠 /info — О курсе\n'
        '📎 /download — Скачать материалы'
    )
    await message.answer(text)

@dp.message_handler(commands=['lesson'])
async def lesson(message: types.Message):
    await message.answer("Урок 1: Как работает ChatGPT.\n... [подробности] ...")

@dp.message_handler(commands=['buy'])
async def buy(message: types.Message):
    await message.answer("Оплата: 3990 ₽ за базу, 7990 ₽ за PRO. Ссылка: https://pay.example.com")

@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    await message.answer("В этом курсе ты научишься использовать ChatGPT профессионально: от промтов до создания агентов")

@dp.message_handler(commands=['download'])
async def download(message: types.Message):
    await message.answer("📥 Скачать материалы: https://yourlink.com/materials.zip")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
