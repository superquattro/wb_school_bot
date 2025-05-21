from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.executor import start_webhook
import logging
import os
import aiohttp
import asyncio
from datetime import datetime

API_TOKEN = os.getenv("API_TOKEN")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = RENDER_EXTERNAL_URL + WEBHOOK_PATH

logging.basicConfig(level=logging.INFO, filename="bot.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Меню начального этапа
menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(KeyboardButton("📘 О курсе — часть 1"))
menu.add(KeyboardButton("📘 О курсе — часть 2"))
menu.add(KeyboardButton("📘 О курсе — часть 3"))

# Меню с полным доступом
full_menu = ReplyKeyboardMarkup(resize_keyboard=True)
full_menu.add(KeyboardButton("📘 О курсе — часть 1"), KeyboardButton("📘 О курсе — часть 2"))
full_menu.add(KeyboardButton("📘 О курсе — часть 3"))
full_menu.add(KeyboardButton("🚀 Начать обучение"), KeyboardButton("🎁 Пробный урок"))
full_menu.add(KeyboardButton("💳 Купить часть 1 (3990 ₽)"), KeyboardButton("💼 Купить весь курс (7990 ₽)"))
full_menu.add(KeyboardButton("🛠 Поддержка"))

# Прогресс пользователя
user_progress = {}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Ты сейчас на самом крутом курсе, который научит тебя GPT-чату. Ты работаешь с искусственным интеллектом.", reply_markup=menu)


@dp.message_handler(lambda msg: msg.text == "📘 О курсе — часть 1")
async def part_1(message: types.Message):
    user_id = message.from_user.id
    read = user_progress.get(user_id, set())
    read.add("📘 О курсе — часть 1")
    user_progress[user_id] = read
    await message.answer("""Часть 1 текста от Екатерины...""", parse_mode='Markdown')
    if read.issuperset({'📘 О курсе — часть 2', '📘 О курсе — часть 3', '📘 О курсе — часть 1'}):
        await message.answer("✅ Все части прочитаны! Новые кнопки разблокированы.", reply_markup=full_menu)

@dp.message_handler(lambda msg: msg.text == "📘 О курсе — часть 2")
async def part_2(message: types.Message):
    user_id = message.from_user.id
    read = user_progress.get(user_id, set())
    read.add("📘 О курсе — часть 2")
    user_progress[user_id] = read
    await message.answer("""Часть 2 текста от Екатерины...""", parse_mode='Markdown')
    if read.issuperset({'📘 О курсе — часть 2', '📘 О курсе — часть 3', '📘 О курсе — часть 1'}):
        await message.answer("✅ Все части прочитаны! Новые кнопки разблокированы.", reply_markup=full_menu)

@dp.message_handler(lambda msg: msg.text == "📘 О курсе — часть 3")
async def part_3(message: types.Message):
    user_id = message.from_user.id
    read = user_progress.get(user_id, set())
    read.add("📘 О курсе — часть 3")
    user_progress[user_id] = read
    await message.answer("""Часть 3 текста от Екатерины...""", parse_mode='Markdown')
    if read.issuperset({'📘 О курсе — часть 2', '📘 О курсе — часть 3', '📘 О курсе — часть 1'}):
        await message.answer("✅ Все части прочитаны! Новые кнопки разблокированы.", reply_markup=full_menu)


@dp.message_handler(lambda msg: msg.text == "🚀 Начать обучение")
async def start_course(message: types.Message):
    await message.answer("🧠 Обучение скоро будет доступно!")

@dp.message_handler(lambda msg: msg.text == "🎁 Пробный урок")
async def trial(message: types.Message):
    await message.answer("🎁 Пробный урок скоро появится!")

@dp.message_handler(lambda msg: "Купить" in msg.text)
async def buy(message: types.Message):
    await message.answer("💳 Оплата появится в ближайшее время.")

@dp.message_handler(lambda msg: msg.text == "🛠 Поддержка")
async def support(message: types.Message):
    await message.answer("📩 Поддержка: @your_support")

async def ping_self():
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(RENDER_EXTERNAL_URL) as resp:
                    logging.info(f"Ping status: {resp.status} at {datetime.now()}")
            except Exception as e:
                logging.warning(f"Ping error: {e}")
            await asyncio.sleep(300)

async def on_startup(dp):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.telegram.org/bot{API_TOKEN}/getWebhookInfo") as resp:
            data = await resp.json()
            if not data['result']['url']:
                await bot.set_webhook(WEBHOOK_URL)
                logging.info("Webhook установлен автоматически")
    asyncio.create_task(ping_self())

async def on_shutdown(dp):
    await bot.delete_webhook()
    logging.info("Webhook отключён.")

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
    )
