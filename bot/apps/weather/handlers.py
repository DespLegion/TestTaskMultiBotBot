from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from .callbacks import WeatherStates
from .api_calls import WeatherAPI
from .keyboards import weather_kb


weather_router = Router()
weather_api = WeatherAPI()


@weather_router.message(WeatherStates.location)
async def update_location(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if message.location:
        location = message.location
        new_city = await weather_api.update_user_last_loc(
            user_id=user_id,
            latitude=message.location.latitude,
            longitude=message.location.longitude
        )
    else:
        location = message.text
        new_city = await weather_api.update_user_last_loc(
            user_id=user_id,
            city_name=message.text
        )
    await state.update_data(location=location)
    data = await state.get_data()
    if "start_message" in data:
        await data["start_message"].edit_text(
            f"Вы успешно обновили ваше местоположение.\nНовое местоположение: {new_city}",
            reply_markup=weather_kb
        )
    if "message" in data:
        await data["message"].delete()
    await state.clear()
    await message.delete()
