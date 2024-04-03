from aiogram import types, Router
from aiogram.filters.command import CommandStart

from bot.apps.users import UserAPI
from .api_calls import ServiceAPI
from .keyboards import main_kb, back_to_menu_kb

service_api = ServiceAPI()
user_api = UserAPI()
main_router = Router()


@main_router.message(CommandStart())
async def cmd_start(message: types.Message):
    ping_res = await service_api.ping_backend()
    if ping_res:
        is_user_exists = await user_api.user_exists(user_id=message.from_user.id)
        if not is_user_exists:
            await user_api.create_user(
                user_id=message.from_user.id,
                user_username=message.from_user.username,
                user_firstname=message.from_user.first_name,
                user_lastname=message.from_user.last_name
            )
        await message.answer(f"Чем могу помочь, {message.from_user.first_name}?", reply_markup=main_kb)
    else:
        await message.answer(f"Не удается соединиться с сервером.\nПопробуйте позже", reply_markup=back_to_menu_kb)
