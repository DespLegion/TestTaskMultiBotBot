from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.apps.main.keyboards import back_to_menu_kb

from .api_calls import UserAPI


user_api = UserAPI()
user_callback_router = Router()


@user_callback_router.callback_query(F.data == "user_info")
async def user_info_callback(callback: CallbackQuery):
    user_info = await user_api.get_user(callback.from_user.id)
    if user_info["status"]:
        await callback.message.edit_text(
            f"Имя пользователя: {user_info['user']['user_firstname']}\n"
            f"ID пользователя: {user_info['user']['user_id']}\n"
            f"Дата регистрации: {user_info['user']['user_add_date']} (UTC)",
            reply_markup=back_to_menu_kb
        )
    await callback.answer("Информация о пользователе")
