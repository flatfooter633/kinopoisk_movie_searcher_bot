from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подобрать по параметрам", callback_data="movie_by_param")],
        [InlineKeyboardButton(text="Поиск по названию", callback_data="movie_search")],
        [InlineKeyboardButton(text="💰Высоко бюджетные", callback_data="high_budget_movie"),
         InlineKeyboardButton(text="🎃Низко бюджетные", callback_data="low_budget_movie")],
        [InlineKeyboardButton(text="🌟Избранное", callback_data="favorites"),
         InlineKeyboardButton(text="🎥Просмотренные", callback_data="viewed")],
        [InlineKeyboardButton(text="⏳История", callback_data="history"),
         InlineKeyboardButton(text="💡Помощь", callback_data="help")],
    ]
)


class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int


# ◀️▶️▶️🔼⏩⏪⏮️️⏭️🔽⏬⏏️➡️⬅️⬆️⬇️🔄️🔙🔜🔝🔚☑️
def pag_func(page: int = 0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅️", callback_data=Pagination(action="prev", page=page).pack()),
        InlineKeyboardButton(text="⬆️", callback_data=Pagination(action="up", page=page).pack()),
        InlineKeyboardButton(text="➡️", callback_data=Pagination(action="next", page=page).pack()),
        width=3
    )
    builder.row(
        InlineKeyboardButton(text="🌟в избранное", callback_data="add_to_favorite"),
        InlineKeyboardButton(text="просмотрен🎥", callback_data="add_to_viewed"),
        width=2
    )
    builder.row(InlineKeyboardButton(text="⏏️главное меню⏏️", callback_data="main_menu"))
    return builder.as_markup()


async def from_dict_keyboard(
        input_dict: dict,
        callback_prefix: str,
        columns: int,
        reverse: bool = False) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard markup from a dictionary of items.

    Parameters:
        - input_dict (dict): A dictionary where keys are English names and values are Russian names.
        - callback_prefix (str): The prefix for the callback data.
        - columns (int): The number of columns for the keyboard layout.
        - reverse (bool): If True, the English names will be displayed instead of the Russian names.

    Returns:
        - InlineKeyboardMarkup: The inline keyboard markup with buttons created from the dictionary.
    """
    # Initialize InlineKeyboardBuilder
    key = InlineKeyboardBuilder()

    # Iterate through the dictionary
    for eng, rus in input_dict.items():
        if reverse:
            # Add a button with the English name to the keyboard
            key.add(InlineKeyboardButton(text=eng, callback_data=f'{callback_prefix}{rus}'))
        else:
            # Add a button with the Russian name to the keyboard
            key.add(InlineKeyboardButton(text=rus, callback_data=f'{callback_prefix}{eng}'))

    # Adjust the organization of the keyboard to columns and return the InlineKeyboardMarkup object
    return key.adjust(columns).as_markup()


async def from_list_keyboard(input_list: list, callback_prefix: str, columns: int) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard markup from a list of items.

    Parameters:
        - input_list (list): A list of items.
        - callback_prefix (str): The prefix for the callback data.
        - columns (int): The number of columns for the keyboard layout.

    Returns:
        - InlineKeyboardMarkup: The inline keyboard markup with buttons created from the list.
    """
    # Initialize InlineKeyboardBuilder
    key = InlineKeyboardBuilder()

    # Iterate through the list
    for item in input_list:
        # Add a button to the keyboard
        key.add(InlineKeyboardButton(text=str(item), callback_data=f'{callback_prefix}{item}'))

    # Adjust the organization of the keyboard to columns and return the InlineKeyboardMarkup object
    return key.adjust(columns).as_markup()
