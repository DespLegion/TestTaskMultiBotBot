from io import BytesIO

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.apps.main.keyboards import back_to_menu_kb
from .keyboards import start_p_e_kb
from .api_calls import PhotoEAPI

photo_e_callback_router = Router()
photo_api = PhotoEAPI()


class PhotoEditState(StatesGroup):
    photo = State()
    start_message = State()


class WatermarkUpdateState(StatesGroup):
    watermark = State()
    start_message = State()


@photo_e_callback_router.callback_query(F.data == "photo_edit_start")
async def start_photo_edit_callback(callback: types.CallbackQuery):

    await callback.answer("Редактирование фото")

    await callback.message.edit_text(
        f"Для добавления водяного знака на фото нажмите 'Фото'\n\n"
        f"Для установки или обновления водяного знака по умолчанию нажмите 'Водяной знак'",
        reply_markup=start_p_e_kb
    )


@photo_e_callback_router.callback_query(F.data == "edit_photo")
async def photo_edit_callback(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer("Добавить водяной знак на фото")

    await state.set_state(PhotoEditState.photo)

    await state.update_data(start_message=callback.message)

    await callback.message.edit_text(
        f"Отправьте фотографию, на которую желаете нанести водяной знак",
        reply_markup=back_to_menu_kb
    )


@photo_e_callback_router.callback_query(F.data == "update_watermark")
async def watermark_update_callback(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state(WatermarkUpdateState.watermark)

    temp_watermark_img = await photo_api.get_watermark(callback.from_user.id)
    watermark_bytes = BytesIO(temp_watermark_img)

    await callback.answer("Обновить водяной знак")

    msg = await callback.message.answer_photo(
        photo=types.BufferedInputFile(watermark_bytes.getvalue(), filename=""),
        caption="Ваш водяной знак.\n\n"
                "Если хотите его изменить - Отправьте изображение, которое вы хотите использовать",
        reply_markup=back_to_menu_kb
    )

    await state.update_data(start_message=msg)
    await callback.message.delete()
