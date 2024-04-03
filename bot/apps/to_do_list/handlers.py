from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from .callbacks import AddTaskState, TasksListState, UpdateTaskState
from .keyboards import cancel_to_do_kb, save_task_kb, edit_task_kb, save_task_update_kb, skip_text_update_kb
from bot.apps.main.keyboards import back_to_menu_kb


to_do_list_router = Router()


@to_do_list_router.message(AddTaskState.task_title)
async def set_task_title(message: types.Message, state: FSMContext):
    await state.update_data(task_title=message.text)
    await message.delete()
    state_data = await state.get_data()
    start_message = state_data["start_message"]
    await start_message.edit_text(
        f"Введите текст задачи",
        reply_markup=cancel_to_do_kb
    )
    await state.set_state(AddTaskState.task_text)


@to_do_list_router.message(AddTaskState.task_text)
async def set_task_text(message: types.Message, state: FSMContext):
    await state.update_data(task_text=message.text)
    await message.delete()
    state_data = await state.get_data()
    start_message = state_data["start_message"]
    await start_message.edit_text(
        f"Новая задача:\n{state_data['task_title']}\n\n{state_data['task_text']}",
        reply_markup=save_task_kb
    )


@to_do_list_router.message(TasksListState.task_id)
async def full_task_info(message: types.Message, state: FSMContext):
    m_text = message.text
    await message.delete()
    state_data = await state.get_data()
    start_message = state_data["start_message"]
    try:
        task_number = int(message.text) - 1
        needed_task = state_data["tasks_list"][task_number]
        await state.update_data(needed_task=needed_task)
        await state.update_data(task_id=needed_task["task_id"])
        await start_message.edit_text(
            f"Задача:\n\n{needed_task['task_title']}\n\n{needed_task['task_text']}",
            reply_markup=edit_task_kb
        )
    except (IndexError, ValueError):
        await start_message.edit_text(
            f"{start_message.text}\n\nВы ввели неверный номер задачи - {m_text}. Попробуйте еще раз",
            reply_markup=edit_task_kb
        )


@to_do_list_router.message(UpdateTaskState.task_title)
@to_do_list_router.callback_query(F.data == "skip_title_task_update")
async def edit_task_title(data: types.Message | types.CallbackQuery, state: FSMContext):
    if isinstance(data, types.Message):
        new_title = data.text
        await data.delete()
    else:
        new_title = ""

    await state.update_data(task_title=new_title)
    state_data = await state.get_data()
    start_message = state_data["start_message"]
    await start_message.edit_text(
        f"Введите новый текст задачи\nЕсли не хотите его менять, нажмите 'Далее'",
        reply_markup=skip_text_update_kb
    )
    await state.set_state(UpdateTaskState.task_text)


@to_do_list_router.message(UpdateTaskState.task_text)
@to_do_list_router.callback_query(F.data == "skip_text_task_update")
async def edit_task_text(data: types.Message | types.CallbackQuery, state: FSMContext):
    if isinstance(data, types.Message):
        new_text = data.text
        await data.delete()
    else:
        new_text = ""

    await state.update_data(task_text=new_text)
    await state.set_state(state=None)
    state_data = await state.get_data()
    start_message = state_data["start_message"]
    needed_task = state_data["needed_task"]
    if state_data['task_title'] == "" and state_data['task_text'] == "":
        await start_message.edit_text(
            f"Вы не внесли ни каких изменений.\nЗадача обновлена не будет",
            reply_markup=back_to_menu_kb
        )
    else:
        await start_message.edit_text(
            f"Обновленная задача:\n\nЗаголовок:\n"
            f"{needed_task['task_title'] if state_data['task_title'] == '' else state_data['task_title']}\n"
            f"\nТекст:\n"
            f"{needed_task['task_text'] if state_data['task_text'] == '' else state_data['task_text']}",
            reply_markup=save_task_update_kb
        )
