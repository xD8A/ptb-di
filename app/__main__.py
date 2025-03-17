from os import getenv
from dishka import make_async_container
from telegram import Update
from telegram.ext import Application, CommandHandler
from app.di import setup_dishka
from app.handlers import start
from app.providers import MyProvider


def main() -> None:
    container = make_async_container(MyProvider())

    token = getenv("BOT_TOKEN")

    app_builder = Application.builder().token(token)
    setup_dishka(container, app_builder)

    application = app_builder.build()
    application.add_handler(CommandHandler("start", start, block=False))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
