from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from .keyboards import main_to_do_kb, cancel_to_do_kb, skip_title_update_kb, main_no_tasks_kb
from bot.apps.main.keyboards import back_to_menu_kb
from .api_calls import ToDoAPI


to_do_api = ToDoAPI()
to_do_list_callback_router = Router()


class AddTaskState(StatesGroup):
    task_title = State()
    task_text = State()
    start_message = State()


class TasksListState(StatesGroup):
    task_id = State()
    tasks_list = State()
    needed_task = State()
    start_message = State()


class UpdateTaskState(StatesGroup):
    task_id = State()
    task_title = State()
    task_text = State()
    needed_task = State()
    start_message = State()


@to_do_list_callback_router.callback_query(F.data == "to_do_list")
async def to_do_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    total_tasks_q = await to_do_api.get_all_user_tasks(user_id=user_id)
    if total_tasks_q["status"] == "success":
        total_tasks = len(total_tasks_q["user_tasks"])
    else:
        total_tasks = 0
    await callback.answer("Список задач")
    if total_tasks <= 0:
        await callback.message.edit_text(
            f"Ваш список задач пуст.\nДля добавления новой задачи - нажмите кнопку",
            reply_markup=main_no_tasks_kb
        )
    else:
        await callback.message.edit_text(
            f"Что вы хотите сделать с вашим Списком Задач?\nКоличество ваших задач: {total_tasks}",
            reply_markup=main_to_do_kb
        )


@to_do_list_callback_router.callback_query(F.data == "add_task")
async def add_task_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Добавить задачу")
    await state.set_state(AddTaskState.task_title)
    await callback.message.edit_text(
        f"Введите название (Заголовок) задачи",
        reply_markup=cancel_to_do_kb
    )
    await state.update_data(start_message=callback.message)


@to_do_list_callback_router.callback_query(F.data == "save_task")
async def save_task_callback(callback: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    await callback.answer("Сохранить задачу")
    user_id = callback.from_user.id
    save_task_res = await to_do_api.create_user_task(
        user_id=user_id,
        task_title=state_data['task_title'],
        task_text=state_data['task_text']
    )
    if save_task_res["status"] == "success":
        start_message = state_data["start_message"]
        total_tasks_q = await to_do_api.get_all_user_tasks(user_id=user_id)
        if total_tasks_q["status"] == "success":
            total_tasks = len(total_tasks_q["user_tasks"])
        else:
            total_tasks = "Unknown"
        await start_message.edit_text(
            f"Задача успешно сохранена.\nКоличество ваших задач: {total_tasks}",
            reply_markup=back_to_menu_kb
        )
    else:
        await callback.message.edit_text(
            f"Ошибка при сохранении задачи. Вернитесь в меню и попробуйте еще раз",
            reply_markup=back_to_menu_kb
        )

    await state.clear()


@to_do_list_callback_router.callback_query(F.data == "tasks_list")
async def show_tasks_callback(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    tasks_list = await to_do_api.get_all_user_tasks(user_id=user_id)

    await callback.answer("Список задач")
    if tasks_list["status"] == "success":
        c = 1
        tasks_str = ""
        for task in tasks_list["user_tasks"]:
            tasks_str += f"{c}) {task['task_title']}\n"
            c += 1
        tasks_str += "\nДля подробного просмотра задачи - введите ее номер"

        await state.set_state(TasksListState.task_id)

        await state.update_data(tasks_list=tasks_list["user_tasks"])

        mess = await callback.message.edit_text(
            f"Список ваших задач:\n\n{tasks_str}",
            reply_markup=back_to_menu_kb
        )
        await state.update_data(start_message=mess)
    else:
        await state.clear()
        await callback.message.edit_text(
            f"Ошибка при получении списка задач. Вернитесь в меню и попробуйте еще раз",
            reply_markup=back_to_menu_kb
        )


@to_do_list_callback_router.callback_query(F.data == "edit_task")
async def edit_task_callback(callback: types.CallbackQuery, state: FSMContext):

    task_list_state_data = await state.get_data()
    task_id = task_list_state_data["task_id"]

    needed_task = task_list_state_data["needed_task"]

    await state.clear()

    await state.set_state(UpdateTaskState.task_title)
    await state.update_data(needed_task=needed_task)
    await state.update_data(task_id=task_id)
    await state.update_data(start_message=callback.message)

    await callback.answer("Редактировать задачу")

    await callback.message.edit_text(
        f"Введите новый заголовок задачи\nЕсли не хотите его менять, нажмите 'Далее'",
        reply_markup=skip_title_update_kb
    )


@to_do_list_callback_router.callback_query(F.data == "delete_task")
async def delete_task_callback(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    state_data = await state.get_data()

    delete_status = await to_do_api.delete_user_task(user_id=user_id, task_id=state_data['task_id'])

    await callback.answer("Удалить задачу")
    if delete_status["status"] == "success":
        await state.clear()
        await callback.message.edit_text(
            f"Задача успешно удалена",
            reply_markup=back_to_menu_kb
        )
    else:
        await state.clear()
        await callback.message.edit_text(
            f"Ошибка при удалении задачи. Вернитесь в меню и попробуйте еще раз",
            reply_markup=back_to_menu_kb
        )


@to_do_list_callback_router.callback_query(F.data == "save_task_update")
async def save_task_update_callback(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    state_data = await state.get_data()

    if "task_id" in state_data:
        task_id = int(state_data["task_id"])
    else:
        task_id = None

    if "task_title" in state_data:
        task_title = state_data["task_title"]
    else:
        task_title = ""

    if "task_text" in state_data:
        task_text = state_data["task_text"]
    else:
        task_text = ""

    update_status = await to_do_api.update_user_task(
        user_id=user_id,
        task_id=task_id,
        task_title=task_title,
        task_text=task_text
    )
    await callback.answer("Сохранить изменения")
    start_message = state_data["start_message"]
    if update_status["status"] == "success":
        await start_message.edit_text(
            f"Задача успешно обновлена",
            reply_markup=back_to_menu_kb
        )
    else:
        await start_message.edit_text(
            f"Ошибка при обновлении задачи.\nВернитесь в меню и попробуйте снова",
            reply_markup=back_to_menu_kb
        )
    await state.clear()
