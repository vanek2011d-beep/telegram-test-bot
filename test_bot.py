
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🔍 Проверить сервер", callback_data="check")

    await message.answer(
        "✅ Тестовый бот работает!",
        reply_markup=keyboard.as_markup()
    )


@dp.callback_query(F.data == "check")
async def check(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("✅ Кнопки работают!")


async def handle_webhook(request):
    data = await request.json()
    from aiogram.types import Update
    update = Update.model_validate(data, context={"bot": bot})
    await dp.feed_update(bot, update)
    return web.Response(text="OK")


async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)


async def on_cleanup(app):
    await bot.session.close()


app = web.Application()
app.router.add_post("/webhook", handle_webhook)
app.router.add_get("/", lambda request: web.Response(text="Bot is running"))
app.on_startup.append(on_startup)
app.on_cleanup.append(on_cleanup)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    web.run_app(app, host="0.0.0.0", port=port)
