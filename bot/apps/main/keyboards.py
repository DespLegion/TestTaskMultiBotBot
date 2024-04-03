from aiogram.types import InlineKeyboardMarkup as InlineKM
from aiogram.types import InlineKeyboardButton as InlineKB


main_kb = InlineKM(
    inline_keyboard=[
        [InlineKB(text="О пользователе", callback_data="user_info")],
        [
            InlineKB(text="Прогноз погоды", callback_data="weather_info"),
            InlineKB(text="Обработка изображения", callback_data="photo_edit_start")
        ],
        [
            InlineKB(text="Пройти тест", callback_data="start_test"),
            InlineKB(text="TO-DO List", callback_data="to_do_list")
        ],
        [InlineKB(text="О боте", url="https://github.com/DespLegion/TestTaskMultiBotBackend")],
    ]
)

back_to_menu_kb = InlineKM(
    inline_keyboard=[
        [InlineKB(text="В меню", callback_data="cancel")],
    ]
)
