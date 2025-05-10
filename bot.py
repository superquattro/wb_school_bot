from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InputFile
from aiogram.utils.executor import start_webhook
import logging
import os
import aiohttp

API_TOKEN = os.getenv("API_TOKEN")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{RENDER_EXTERNAL_URL}{WEBHOOK_PATH}"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("📘 Обучение"), KeyboardButton("💳 Оплатить доступ"))
main_menu.add(KeyboardButton("🛠 Поддержка"))

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

async def on_startup(dp):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.telegram.org/bot{API_TOKEN}/getWebhookInfo") as resp:
            data = await resp.json()
            if not data['result']['url']:
                await bot.set_webhook(WEBHOOK_URL)
                print("Webhook установлен автоматически")

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
