from aiogram.types import InlineKeyboardButton as InlineKB
from aiogram.utils.keyboard import InlineKeyboardBuilder


def kb_builder(answers: dict):
    kb = InlineKeyboardBuilder()
    for answer in answers:
        if not answer == "r_answer":
            cb_data = "f_answer"
        else:
            cb_data = "r_answer"
        kb.button(text=str(answers[answer]), callback_data=cb_data)
    kb.adjust(2)
    kb.row(
        InlineKB(text="Отмена", callback_data="cancel"),
        width=1
    )
    return kb.as_markup()
