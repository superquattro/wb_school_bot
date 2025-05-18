from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.executor import start_webhook
import logging
import os
import aiohttp
import asyncio

API_TOKEN = os.getenv("API_TOKEN")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{RENDER_EXTERNAL_URL}{WEBHOOK_PATH}"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(KeyboardButton("📘 О курсе"), KeyboardButton("🎁 Попробовать бесплатно"))
menu.add(KeyboardButton("💳 Купить часть 1 (3990 ₽)"), KeyboardButton("💳 Купить весь курс (7990 ₽)"))
menu.add(KeyboardButton("🛠 Поддержка"))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    text = "Добро пожаловать в бот-курс Аркадия по ChatGPT!\n\n🔹 Обучение для новичков и продвинутых пользователей\n🔹 GPT-агенты, промты, автоматизация\n\nВыберите, с чего начать 👇"
    await message.answer(text, reply_markup=menu)

@dp.message_handler(lambda msg: msg.text == "📘 О курсе")
async def course_info(message: types.Message):
    text = ("💡 Курс состоит из 2 частей:\n\n"
            "1️⃣ *Базовая* — основы ChatGPT, грамотная работа с промтами\n"
            "2️⃣ *Продвинутая* — создание GPT-агентов, интеграции, API\n\n"
            "Вы можете купить любую часть отдельно или получить полный доступ.")
    await message.answer(text, parse_mode='Markdown')

@dp.message_handler(lambda msg: msg.text == "🎁 Попробовать бесплатно")
async def trial(message: types.Message):
    await message.answer("🎁 Бесплатный пробный урок скоро будет доступен!\nСледите за обновлениями.")

@dp.message_handler(lambda msg: "Купить" in msg.text)
async def buy(message: types.Message):
    await message.answer("💳 Оплата временно недоступна.\nСкоро здесь появится возможность купить курс прямо в боте.")

@dp.message_handler(lambda msg: msg.text == "🛠 Поддержка")
async def support(message: types.Message):
    await message.answer("📩 Напишите нам: @your_support")

async def ping_self():
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(RENDER_EXTERNAL_URL) as resp:
                    logging.info(f"Ping status: {resp.status}")
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
