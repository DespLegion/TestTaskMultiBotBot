from aiogram.types import InlineKeyboardMarkup as InlineKM
from aiogram.types import InlineKeyboardButton as InlineKB


cancel_button = InlineKB(text="Отмена", callback_data="cancel")

main_to_do_kb = InlineKM(
    inline_keyboard=[
        [
            InlineKB(text="Добавить задачу", callback_data="add_task"),
            InlineKB(text="Список задач", callback_data="tasks_list")
        ],
        [cancel_button],
    ]
)

main_no_tasks_kb = InlineKM(
    inline_keyboard=[
        [
            InlineKB(text="Добавить задачу", callback_data="add_task"),
        ],
        [cancel_button],
    ]
)

cancel_to_do_kb = InlineKM(
    inline_keyboard=[
        [cancel_button],
    ]
)

save_task_kb = InlineKM(
    inline_keyboard=[
        [InlineKB(text="Сохранить", callback_data="save_task")],
        [cancel_button],
    ]
)

save_task_update_kb = InlineKM(
    inline_keyboard=[
        [InlineKB(text="Сохранить", callback_data="save_task_update")],
        [cancel_button],
    ]
)

skip_title_update_kb = InlineKM(
    inline_keyboard=[
        [InlineKB(text="Далее", callback_data="skip_title_task_update")],
        [cancel_button],
    ]
)

skip_text_update_kb = InlineKM(
    inline_keyboard=[
        [InlineKB(text="Далее", callback_data="skip_text_task_update")],
        [cancel_button],
    ]
)

edit_task_kb = InlineKM(
    inline_keyboard=[
        [
            InlineKB(text="Редактировать", callback_data="edit_task"),
            InlineKB(text="Удалить", callback_data="delete_task")
        ],
        [cancel_button],
    ]
)

