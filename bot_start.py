import asyncio
from aiogram import Bot, Dispatcher, types

import logging

import config

from bot.apps.main import main_router, main_callback_router
from bot.apps.users import user_callback_router
from bot.apps.weather import weather_router, weather_callback_router
from bot.apps.to_do_list import to_do_list_callback_router, to_do_list_router
from bot.apps.testings import testings_callback_router
from bot.apps.photo_editing import photo_e_callback_router, photo_e_router


bot = Bot(token=config.B_TOKEN)

dp = Dispatcher()


async def main():
    dp.include_routers(
        main_router,
        main_callback_router,
        user_callback_router,
        weather_router,
        weather_callback_router,
        to_do_list_router,
        to_do_list_callback_router,
        testings_callback_router,
        photo_e_router,
        photo_e_callback_router
    )
    await bot.set_my_commands(
        commands=[
            types.BotCommand(
                command="start",
                description="Main menu"
            )
        ]
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    asyncio.run(main())
