from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from io import BytesIO

from .callbacks import WatermarkUpdateState, PhotoEditState
from bot.apps.main.keyboards import back_to_menu_kb
from bot.utils.add_watermark import add_wm
from .api_calls import PhotoEAPI


photo_e_router = Router()
photo_api = PhotoEAPI()


@photo_e_router.message(PhotoEditState.photo)
async def photo_with_watermark(message: types.Message, state: FSMContext):

    bytes_photo = BytesIO()
    await message.bot.download(file=message.photo[-1].file_id, destination=bytes_photo)

    temp_watermark_img = await photo_api.get_watermark(message.from_user.id)
    watermark_bytes = BytesIO(temp_watermark_img)

    res_img = await add_wm(img=bytes_photo, watermark_buffer=watermark_bytes)

    bytes_photo_to_send = BytesIO()

    res_img.save(bytes_photo_to_send, format="jpeg")
    bytes_photo_to_send.seek(0)

    state_data = await state.get_data()
    start_message = state_data["start_message"]

    await start_message.delete()

    await message.answer_photo(
        photo=types.BufferedInputFile(bytes_photo_to_send.getvalue(), filename=""),
        caption="Ваше изображение с наложенным водяным знаком",
        reply_markup=back_to_menu_kb
    )

    await message.delete()


@photo_e_router.message(WatermarkUpdateState.watermark)
async def upload_watermark(message: types.Message, state: FSMContext):

    bytes_watermark = BytesIO()
    await message.bot.download(file=message.photo[-1].file_id, destination=bytes_watermark)

    state_data = await state.get_data()
    start_message = state_data["start_message"]

    q_res = await photo_api.update_watermark(user_id=message.from_user.id, watermark_img=bytes_watermark)

    await start_message.delete()

    if q_res["status"] == "success":
        await message.answer_photo(
            photo=message.photo[-1].file_id,
            caption="Ваш новый водяной знак\n\nТеперь вы используете его, при наложении на фото",
            reply_markup=back_to_menu_kb
        )
    else:
        await message.answer(
            "Обновить водяной знак не удалось.\nВернитесь в меню и попробуйте снова",
            reply_markup=back_to_menu_kb
        )

    await message.delete()
