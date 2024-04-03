from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from .keyboards import location_kb, weather_kb
from bot.apps.main.keyboards import back_to_menu_kb

from .api_calls import WeatherAPI


weather_callback_router = Router()
weather_api = WeatherAPI()


class WeatherStates(StatesGroup):
    location = State()
    message = State()
    start_message = State()


@weather_callback_router.callback_query(F.data == "weather_info")
async def weather_info_callback(callback: types.CallbackQuery, state: FSMContext):
    last_location = await weather_api.get_user_last_loc_name(callback.from_user.id)
    if last_location == "Unknown":
        await callback.message.edit_text(
            f"Ваше местоположение неизвестно.\nВам необходимо обновить ваше местоположение",
            reply_markup=back_to_menu_kb
        )
    else:
        await callback.message.edit_text(
            f"Ваше местоположение: {last_location}, верно?",
            reply_markup=weather_kb
        )

    await state.set_state(WeatherStates.location)
    await callback.answer("Информация о погоде")
    answer_msg = await callback.message.answer(
        f"Для обновления местоположения нажмите кнопку ниже или введите город",
        reply_markup=location_kb
    )
    await state.update_data(message=answer_msg)
    await state.update_data(start_message=callback.message)


@weather_callback_router.callback_query(F.data == "show_weather")
async def show_weather_callback(callback: types.CallbackQuery, state: FSMContext):
    weather = await weather_api.get_weather(callback.from_user.id)
    if weather == "Unknown place":
        await callback.message.edit_text(
            f"Не удалось обновить погоду по вашему местоположению\n\n"
            f"Убедитесь что ваше местоположение (Город) указано корректно\n"
            f"В противном случае - обновите ваше местоположение",
            reply_markup=back_to_menu_kb
        )
    else:
        await callback.message.edit_text(
            f"Погода в городе: {weather['city']}\n"
            f"Температура {weather['cur_temp']}°C\n"
            f"Ощущается как {weather['temp_feels_like']}°C\n"
            f"Облачность {weather['cloud']}%\n"
            f"Скорость ветра {weather['wind_speed']} м\с",
            reply_markup=back_to_menu_kb
        )

    data = await state.get_data()
    if "message" in data:
        await data["message"].delete()
    await state.clear()
