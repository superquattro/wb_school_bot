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

menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(KeyboardButton("🚀 Начать обучение"), KeyboardButton("📘 О курсе"))
menu.add(KeyboardButton("🎁 Пробный урок"), KeyboardButton("💳 Купить часть 1 (3990 ₽)"))
menu.add(KeyboardButton("💼 Купить весь курс (7990 ₽)"), KeyboardButton("🛠 Поддержка"))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Ты сейчас на самом крутом курсе, который научит тебя GPT-чату. Ты работаешь с искусственным интеллектом.", reply_markup=menu)

@dp.message_handler(lambda msg: msg.text == "📘 О курсе")
async def course_info(message: types.Message):
    await message.answer("""🧠 Привет! Это не просто курс. Это твой вход в эпоху ChatGPT.
❓Ты слышал про ChatGPT, но не до конца понимаешь, как его использовать?
... (весь текст как выше)
❗️Ты можешь подождать ещё год.
А можешь через 7 дней сказать:
“Я теперь понимаю, как использовать ИИ в жизни и в работе. И умею это делать.”""", parse_mode="Markdown")

@dp.message_handler(lambda msg: msg.text == "🎁 Пробный урок")
async def trial(message: types.Message):
    await message.answer("🎁 Пробный урок скоро появится!")

@dp.message_handler(lambda msg: msg.text == "🚀 Начать обучение")
async def start_course(message: types.Message):
    await message.answer("🧠 Обучение скоро будет доступно!")

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
