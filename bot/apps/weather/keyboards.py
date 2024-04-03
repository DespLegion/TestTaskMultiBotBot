from aiogram.types import ReplyKeyboardMarkup as ReplyKM, KeyboardButton

from aiogram.types import InlineKeyboardMarkup as InlineKM
from aiogram.types import InlineKeyboardButton as InlineKB


weather_kb = InlineKM(
    inline_keyboard=[
        [InlineKB(text="Показать прогноз", callback_data="show_weather")],
        [InlineKB(text="Отмена", callback_data="cancel")],
    ]
)

location_kb = ReplyKM(
    keyboard=[
        [
            KeyboardButton(
                text="Обновить местоположение",
                request_location=True,
            )
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
