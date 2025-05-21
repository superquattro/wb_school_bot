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
    await message.answer("""🧠 Привет! Это не просто курс. Это твой вход в эпоху ChatGPT. ❓Ты слышал про ChatGPT, но не до конца понимаешь, как его использовать? Или уже пробовал, но быстро “застрял” на этапе «напиши сказку про дракона»?  Добро пожаловать. Здесь ты научишься не просто разговаривать с ChatGPT, а использовать его как инструмент заработка, творчества, управления и автоматизации.  ⚡️ Почему этот курс нужен тебе именно сейчас ChatGPT уже изменил рынок труда, бизнес, обучение. 🛠 Его используют маркетологи, юристы, преподаватели, предприниматели, SMM-специалисты, дизайнеры, проект-менеджеры.  Но 95% людей используют его неправильно. Вводят глупые вопросы, получают глупые ответы и думают: “Он тупой”.  Нет. Он не тупой. Он точно повторяет твои команды. Если ты даёшь слабую команду — получаешь слабый результат.  А теперь внимание:  💡 ChatGPT — это инструмент, которому нужна инструкция. И мы её тебе дадим.  📚 Что тебя ждёт внутри курса Как работает ChatGPT и как думает ИИ  Что такое промт-инжиниринг и как писать такие запросы, от которых у модели “взрывается интеллект”  Как решать конкретные задачи: от написания текстов до создания ботов, лендингов, бизнес-идей, книг, презентаций и даже Excel-формул  Как зарабатывать с помощью ChatGPT  Как создавать своих GPT-агентов: персональные ассистенты, консультанты, продавцы, методисты  Всё это — пошагово, с примерами, скриншотами, заданиями и шаблонами.  🔍 А если ты новичок? 🟢 Отлично. Этот курс создан для тебя. Мы не нагружаем терминами. Мы говорим простым языком:  Вот как это работает  Вот как это использовать  Вот как сделать результат  Ты получаешь:  Понятную структуру  Поддержку  Логику, которую можно повторить  🔧 Что ты научишься делать на практике: ✅ Писать такие промты, которые дают качественный, предсказуемый результат ✅ Создавать своих помощников — в продажах, в контенте, в обучении ✅ Работать в любых сферах: HR, финансы, маркетинг, дизайн, образование ✅ Зарабатывать: делать ChatGPT-продукты, услуги, автоматизацию ✅ Использовать нейросети не как “игрушку”, а как рабочий инструмент  👨‍🏫 Курс создал Аркадий — эксперт по ChatGPT У Аркадия 10+ лет в образовании, 2 года в ИИ. Он делает не “ещё один курс”, а систему обучения, в которой ChatGPT становится частью твоего рабочего процесса.  💥 Что будет, если ты пройдёшь этот курс? Ты перестанешь быть “наблюдателем” технологической революции  Ты станешь тем, кто умеет использовать ИИ — реально, на практике  У тебя будет собственный ИИ-помощник, настроенный под тебя  У тебя будет навык, который уже сейчас покупают на фрилансе и в компаниях  🎁 Попробуй бесплатно Первый урок — бесплатный. Просто чтобы ты понял: это не “вода”, это инструмент.  Если зайдёт — проходишь дальше, оплачиваешь доступ и идёшь к результату.  💳 Сколько стоит? 📦 Базовая часть: 3990 ₽ — основы ChatGPT, практика, навыки  🔓 Продвинутая часть: 7990 ₽ — создание агентов, монетизация, интеграции  🎯 Цель — не просто обучение, а результат: у тебя будет реальный навык и готовый ИИ-продукт  🔘 Что делать прямо сейчас? Нажми кнопку — и начни с бесплатного урока  Прочувствуй стиль  Убедись в ценности  Пройди — и оплати, если действительно хочешь использовать ИИ как профессионал  ❗️Ты можешь подождать ещё год. А можешь через 7 дней сказать: “Я теперь понимаю, как использовать ИИ в жизни и в работе. И умею это делать.”""")
    await message.answer("👇 Выбери действие ниже:", reply_markup=menu)

@dp.message_handler(lambda msg: msg.text == "🛠 Поддержка")
async def support(message: types.Message):
    await message.answer("📩 Напиши нам: @your_support")

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
    logging.info("Webhook отключён и бот завершил работу.")

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
