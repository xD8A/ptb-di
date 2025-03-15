from dishka import FromDishka
from telegram import Update
from telegram.ext import ContextTypes
from app.di import inject


@inject
async def start(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        value: FromDishka[int]
) -> None:
    await update.message.reply_text(f"Hello, {value}!")
