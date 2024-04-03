from aiogram.types import InlineKeyboardMarkup as InlineKM
from aiogram.types import InlineKeyboardButton as InlineKB


cancel_button = InlineKB(text="Отмена", callback_data="cancel")

start_p_e_kb = InlineKM(
    inline_keyboard=[
        [
            InlineKB(text="Фото", callback_data="edit_photo"),
            InlineKB(text="Водяной знак", callback_data="update_watermark")
        ],
        [cancel_button],
    ]
)
