from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from .keyboards import kb_builder
from bot.apps.main.keyboards import back_to_menu_kb
from .api_calls import TestingsAPI


testings_api = TestingsAPI()
testings_callback_router = Router()


class TestingState(StatesGroup):
    question_number = State()
    testings = State()
    score = State()
    r_answer_score = State()


@testings_callback_router.callback_query(F.data == "start_test")
async def start_test_callback(callback: types.CallbackQuery, state: FSMContext):

    new_testing = await testings_api.get_new_testing()
    await callback.answer("Тестирование")

    r_answer_score = 100 / len(new_testing)

    await state.set_state(TestingState.question_number)
    await state.update_data(question_number=1)
    await state.update_data(testings=new_testing)
    await state.update_data(score=0)
    await state.update_data(r_answer_score=r_answer_score)

    kb = kb_builder(new_testing[0]["answers"])

    await callback.message.edit_text(
        f"Вопрос 1 из {len(new_testing)}:\n\n{new_testing[0]['question']}\n\nВыберете верный ответ",
        reply_markup=kb
    )


@testings_callback_router.callback_query(F.data == "r_answer")
@testings_callback_router.callback_query(F.data == "f_answer")
async def to_do_callback(callback: types.CallbackQuery, state: FSMContext):

    state_data = await state.get_data()
    cur_q_num = state_data["question_number"] + 1
    await state.update_data(question_number=cur_q_num)

    testings = state_data["testings"]

    cur_score = state_data["score"]

    if callback.data == "r_answer":
        r_answer_score = state_data["r_answer_score"]
        cur_score += r_answer_score
        await state.update_data(score=cur_score)
        await callback.answer("Верно")
    else:
        await callback.answer("Не верно")

    if state_data["question_number"] < len(testings):
        kb = kb_builder(testings[cur_q_num-1]["answers"])

        await callback.message.edit_text(
            f"Вопрос {cur_q_num} из {len(testings)}:\n\n{testings[cur_q_num-1]['question']}\n\nВыберете верный ответ",
            reply_markup=kb
        )
    else:
        await callback.message.edit_text(
            f"Вы ответили на все {len(testings)} вопросов\n\nВаш результат:\n {int(cur_score)} из 100 баллов",
            reply_markup=back_to_menu_kb
        )
