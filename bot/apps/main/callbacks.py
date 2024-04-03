from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from .keyboards import main_kb, back_to_menu_kb
from .api_calls import ServiceAPI


service_api = ServiceAPI()
main_callback_router = Router()


@main_callback_router.callback_query(F.data == "cancel")
async def cancel_callback(callback: types.CallbackQuery, state: FSMContext = None):
    if state:
        data = await state.get_data()
        if "message" in data:
            await data["message"].delete()
        await state.clear()

    await callback.answer("Отмена")
    await callback.message.edit_reply_markup()

    ping_res = await service_api.ping_backend()
    if ping_res:
        await callback.message.answer(
            f"Чем могу помочь, {callback.from_user.first_name}?", reply_markup=main_kb
        )
    else:
        await callback.message.answer(
            f"Не удается соединиться с сервером.\nПопробуйте позже",
            reply_markup=back_to_menu_kb
        )

    await callback.message.delete()
