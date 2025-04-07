from aiogram import html, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from contextlib import suppress
from random import choice

from datetime import datetime
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, get_user_locale
from states.states import QueryFormer
from keyboards import keyboards as kb
from keyboards import keyboards_pattern as kb_pattern
from database import requests as db
from api.kinopoisk_from_cash import http_session_start
from utils.validate_funcs import validate_year, validate_rating, check_card, check_named_card
from config import return_film_info
from config import (
    LOW_BUDGET,
    HIGH_BUDGET,
    HELP_TEXT,
    HOW_ARE_YOU_ANSWER,
    STICKERS,
    START_TEXT,
    GREETING_VARIANTS,
    HI_ARRAY,
    GENRE_LIST,
    COUNTRIES_LIST,
    BASE_SEARCH_QUERY,
    SEARCH_BY_NAME_QUERY
)
from locale import Error as LocaleError
from logging import getLogger

# Получение логгера
logger = getLogger("custom_handlers")

router = Router()  # router
films = dict()  # global basket for film cards
current_page = 0  # current page of film cards

# ---------------------------------------------------------
# region Start and Help
# ---------------------------------------------------------
@router.message(F.text.lower().in_(HI_ARRAY))
@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_exist = await db.set_user(
        tg_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
    logger.info(f"User {message.from_user.id} started the bot. Existing user: {user_exist}")
    await message.reply_sticker(STICKERS.get("hello"))
    await message.reply(
        f"Привет, "
        f"{html.bold(message.from_user.first_name)}! "
        f"<b>{'С возвращением!' if user_exist else 'Рад знакомству!👻'}</b>\n"
        f"{choice(GREETING_VARIANTS)}\n{START_TEXT}",
        reply_markup=kb.start_keyboard,
    )

    await message.delete()

@router.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    logger.info(f"User {message.from_user.id} requested help")
    await message.answer(HELP_TEXT)

@router.callback_query(F.data == "help")
async def search_film(callback: CallbackQuery) -> None:
    logger.info(f"User {callback.from_user.id} requested help via callback")
    await callback.answer("Вывожу справочную информацию...")
    await callback.message.edit_text(HELP_TEXT)
    await callback.message.answer_sticker(STICKERS.get("help"))
    # await callback.message.delete()
# endregion
# ---------------------------------------------------------


# ---------------------------------------------------------
# region Main Menu Handler
# ---------------------------------------------------------
@router.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery) -> None:
    logger.info(f"User {callback.from_user.id} returned to main menu")
    await callback.answer("Вывожу главное меню...")
    await callback.message.edit_text("Главное меню", reply_markup=kb.start_keyboard)
# endregion
# ---------------------------------------------------------


# ---------------------------------------------------------
# region Conversation Handlers
# ---------------------------------------------------------
@router.message(
    F.text.lower().contains('как жизнь') |
    F.text.lower().contains('как дела') |
    F.text.lower().contains('что делаешь') |
    F.text.lower().contains('чем занимаешься')
)
async def casual_conversation(message: Message) -> None:
    logger.info(f"User {message.from_user.id} initiated casual conversation")
    await message.reply_sticker(STICKERS.get("ok"))
    await message.reply(f"{choice(HOW_ARE_YOU_ANSWER)}")
# endregion
# ---------------------------------------------------------

# ---------------------------------------------------------
# region Movie Search Handlers
# ---------------------------------------------------------
@router.message(Command("movie_search"))
async def movie_search_command(message: Message, state: FSMContext) -> None:
    logger.info(f"User {message.from_user.id} initiated movie search via command")
    await state.set_state(QueryFormer.name)
    await message.answer("Введите название фильма:")

@router.callback_query(F.data == "movie_search")
async def movie_search_callback(callback: CallbackQuery, state: FSMContext) -> None:
    logger.info(f"User {callback.from_user.id} initiated movie search via callback")
    await callback.answer("Формируем запрос кинопоиску...")
    await callback.message.answer_sticker(STICKERS.get("search"))
    await state.set_state(QueryFormer.name)
    await callback.message.answer(
        "Введите название фильма \n[Например 'Бетховен' или 'Титаник']:"
    )

@router.message(QueryFormer.name)
async def name_catcher(message: Message, state: FSMContext) -> None:
    name = message.text.strip()
    logger.info(f"User {message.from_user.id} searching for movie: {name}")
    await search_by_cmd(message, name=name)
    await state.clear()
# endregion
# ---------------------------------------------------------

# ---------------------------------------------------------
# region Movie Search by Parameters
# ---------------------------------------------------------
@router.message(Command("movie_by_param"))
async def film_selection(message: Message, state: FSMContext) -> None:
    await state.set_state(QueryFormer.genre)
    await message.answer("Введите жанр фильма\n[Например 'аниме' или 'мюзикл']:")

@router.message(QueryFormer.genre)
async def genre_selection(message: Message, state: FSMContext) -> None:
    genre = message.text.lower().strip()
    if genre in GENRE_LIST:
        await state.update_data(genre=genre)
        await state.set_state(QueryFormer.years)
        await message.answer(
            "Введите годы релиза фильма \n[Например '2003' или '1990-2024']:"
        )
    else:
        await message.reply_sticker(STICKERS.get("error"))
        await message.answer("Жанр указан не верно!")


@router.message(QueryFormer.years)
async def years_selection(message: Message, state: FSMContext) -> None:
    years = validate_year(message.text)
    if years:
        await state.update_data(years=years)
        await state.set_state(QueryFormer.countries)
        await message.answer(
            "Введите страну релиза фильма \n[Например 'Россия' или 'США, Канада']:"
        )
    else:
        await message.reply_sticker(STICKERS.get("error"))
        await message.answer("Год указан не верно!")


@router.message(QueryFormer.countries)
async def countries_selection(message: Message, state: FSMContext) -> None:
    countries = message.text.strip()
    if countries in COUNTRIES_LIST:
        await state.update_data(countries=message.text)
        await state.set_state(QueryFormer.ratings)
        await message.answer(
            "Введите рейтинг фильма от 1 до 10 \n[Например '8' или '7-10']:"
        )
    else:
        await message.reply_sticker(STICKERS.get("error"))
        await message.answer("Страна указана не верно!")


@router.message(QueryFormer.ratings)
async def ratings_selection(message: Message, state: FSMContext) -> None:
    ratings = validate_rating(message.text.strip(), 0, 10)
    if ratings:
        await state.update_data(ratings=ratings)
        await state.set_state(QueryFormer.age_ratings)
        await message.answer(
            "Введите возрастное ограничение фильма от 6 до 18 \n[Например '12-18']:"
        )
    else:
        await message.reply_sticker(STICKERS.get("error"))
        await message.answer("Рейтинг указан не верно!")


@router.message(QueryFormer.age_ratings)
async def age_ratings_selection(message: Message, state: FSMContext) -> None:
    age_ratings = validate_rating(message.text.strip(), 6, 18)
    if age_ratings:
        await state.update_data(age_ratings=age_ratings)
        await state.set_state(QueryFormer.limit)
        await message.answer("Введите лимит выдачи фильмов \n[Например '5' или '15']:")
    else:
        await message.reply_sticker(STICKERS.get("error"))
        await message.answer("Возрастное ограничение указано не верно!")


@router.message(QueryFormer.limit)
async def limit_selection(message: Message, state: FSMContext) -> None:
    limit = message.text.strip()
    if limit.isdigit():
        await state.update_data(limit=limit)
        films_query = await state.get_data()
        await search_by_cmd(message, films_query)
        await state.clear()
    else:
        await message.reply_sticker(STICKERS.get("error"))
        await message.answer("Лимит выдачи указан не верно!")

# endregion
# ---------------------------------------------------------

# ---------------------------------------------------------
# region Movie Search by Parameters Handlers
# ---------------------------------------------------------
@router.callback_query(F.data == "movie_by_param")
async def movie_by_param(callback: CallbackQuery) -> None:
    logger.info(f"User {callback.from_user.id} initiated movie search by parameters")
    await callback.answer("Формируем запрос кинопоиску...")
    await callback.message.edit_text(
        "Выберите жанр фильма:",
        reply_markup=await kb.from_dict_keyboard(
            kb_pattern.genres,
            'genres_',
            3
        )
    )


@router.callback_query(F.data.startswith('genres_'))
async def category(callback: CallbackQuery, state: FSMContext):
    genre = callback.data.split("_")[-1]
    await state.set_state(QueryFormer.genre)
    await state.update_data(
        genre=GENRE_LIST
        if genre == 'all-genres'
        else kb_pattern.genres.get(genre)
    )
    await state.set_state(QueryFormer.countries)
    await callback.answer(f'Вы выбрали жанр {genre}')
    await callback.message.edit_text(
        'Выберите страну релиза фильма',
        reply_markup=await kb.from_dict_keyboard(
            kb_pattern.countries,
            'countries_',
            3
        )
    )


@router.callback_query(F.data.startswith('countries_'))
async def category(callback: CallbackQuery, state: FSMContext):
    country = callback.data.split("_")[-1]
    await state.update_data(
        countries=COUNTRIES_LIST
        if country == 'all-countries'
        else kb_pattern.countries.get(country)
    )
    await state.set_state(QueryFormer.years)
    await callback.answer(f'Вы выбрали страну {country}')
    await callback.message.edit_text(
        'Выберите годы релиза фильма',
        reply_markup=await kb.from_list_keyboard(
            kb_pattern.years,
            'years_',
            3
        )
    )


@router.callback_query(F.data.startswith('years_'))
async def category(callback: CallbackQuery, state: FSMContext):
    years = callback.data.split("_")[-1]
    await state.update_data(years=years)
    await state.set_state(QueryFormer.ratings)
    await callback.answer(f'Вы выбрали годы {years}')
    await callback.message.edit_text(
        'Выберите рейтинг фильма',
        reply_markup=await kb.from_list_keyboard(
            kb_pattern.rating,
            'rating_',
            3
        )
    )


@router.callback_query(F.data.startswith('rating_'))
async def category(callback: CallbackQuery, state: FSMContext):
    rating = callback.data.split("_")[-1]
    await state.update_data(ratings=rating)
    await state.set_state(QueryFormer.age_ratings)
    await callback.answer(f'Вы выбрали рейтинг {rating}')
    await callback.message.edit_text(
        'Выберите возрастной рейтинг фильма',
        reply_markup=await kb.from_dict_keyboard(
            kb_pattern.agerating,
            'agerating_',
            4,
            True
        )
    )


@router.callback_query(F.data.startswith('agerating_'))
async def category(callback: CallbackQuery, state: FSMContext):
    age_rating = callback.data.split("_")[-1]
    await state.update_data(age_ratings=age_rating)
    await state.set_state(QueryFormer.limit)
    await callback.answer(f'Вы выбрали возрастной рейтинг {age_rating}')
    await callback.message.edit_text(
        'Выберите кол-во фильмов в выдаче',
        reply_markup=await kb.from_list_keyboard(
            list(range(5, 31, 5)),
            'limit_',
            3
        )
    )


@router.callback_query(F.data.startswith('limit_'))
async def category(callback: CallbackQuery, state: FSMContext):
    limit = callback.data.split("_")[-1]
    await state.update_data(limit=limit)
    await callback.answer(f'Вы выбрали {limit} фильмов в выдаче')
    films_query = await state.get_data()
    # await callback.message.answer(f'Вы выбрали {films_query}')
    await search_by_callback(callback, films_query)
    await state.clear()
# endregion
# ---------------------------------------------------------


# ---------------------------------------------------------
# region History and Favorites Handlers
# ---------------------------------------------------------
@router.message(Command("history"))
async def command_history_handler(message: Message) -> None:
    logger.info(f"User {message.from_user.id} requested search history")
    await message.answer(
        "Выберите дату поиска: ",
        reply_markup=await SimpleCalendar(locale=await get_user_locale(message.from_user)).start_calendar()
    )

@router.callback_query(SimpleCalendarCallback.filter())
async def request_date(callback_query: CallbackQuery, callback_data: CallbackData):
    logger.info(f"User {callback_query.from_user.id} selecting date for history")
    try:
        calendar = SimpleCalendar(
            locale=await get_user_locale(callback_query.from_user), show_alerts=True
        )
    except LocaleError:
        logger.warning('TG did not fix the locales')
        calendar = SimpleCalendar(locale='ru_RU.utf8', show_alerts=True)

    current_date = datetime.now()
    calendar.set_dates_range(datetime(2025, 1, 1), current_date)
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        date = date.strftime("%Y-%m-%d")
        await callback_query.message.edit_text(f'Вы выбрали {date}')
        logger.info(f'User {callback_query.from_user.id} selected date: {date}')
        tg_id = callback_query.from_user.id
        history = await db.get_user_history(tg_id, date)
        global films
        films[tg_id] = list()
        films[tg_id] = [item for item in history]
        if len(films[tg_id]) > 0:
            await callback_query.message.answer(return_film_info(films.get(tg_id)[0]), reply_markup=kb.pag_func())
        else:
            logger.info(f'No history found for user {tg_id} on date {date}')
            await callback_query.message.edit_text("История запросов пуста.", reply_markup=kb.start_keyboard,)
            await callback_query.message.answer_sticker(STICKERS.get("not_found"))

@router.callback_query(F.data.in_(db.functions.keys()))
async def history_favorites_viewed_handler(callback: CallbackQuery) -> None:
    tg_id = callback.from_user.id
    logger.info(f"User {tg_id} requested {callback.data}")
    db_function = db.functions[callback.data]
    if callback.data == "history":
        await callback.answer("Вы выбрали историю запросов")
        try:
            calendar = await SimpleCalendar(locale=await get_user_locale(callback.from_user)).start_calendar()
        except LocaleError:
            logger.warning('TG did not fix the locales')
            calendar = await SimpleCalendar(locale='ru_RU.utf8').start_calendar()

        await callback.message.answer(
            "Выберите дату поиска: ",
            reply_markup=calendar
        )
    else:
        items = await db_function(tg_id)
        global films
        films[tg_id] = list()
        await callback.answer(f"{callback.data.capitalize()}:")
        films[tg_id] = [item for item in items]
        if len(films[tg_id]) > 0:
            await callback.message.answer(return_film_info(films.get(tg_id)[0]), reply_markup=kb.pag_func())
        else:
            logger.info(f'No {callback.data} found for user {tg_id}')
            await callback.message.answer_sticker(STICKERS.get("not_found"))
            await callback.message.answer(f"Список {callback.data} фильмов пуст.", reply_markup=kb.start_keyboard, )

# endregion
# ---------------------------------------------------------


# ---------------------------------------------------------
# region Pagination Handler
# ---------------------------------------------------------
@router.callback_query(kb.Pagination.filter(F.action.in_(["prev", "next", "up"])))
async def pagination_handler(callback: CallbackQuery, callback_data: kb.Pagination) -> None:
    page_number = int(callback_data.page)
    tg_id = callback.from_user.id
    global films
    movies = films.get(tg_id)
    if callback_data.action == "prev":
        page = page_number - 1 if page_number > 0 else 0
    elif callback_data.action == "next":
        page = page_number + 1 if page_number < len(movies) - 1 else page_number
    else:
        page = 0
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            return_film_info(movies[page]),
            reply_markup=kb.pag_func(page=page)
        )
    global current_page
    current_page = page
    await callback.answer("Изменяем страницу...")
# endregion
# ---------------------------------------------------------


# ---------------------------------------------------------
# region Add to List Handler
# ---------------------------------------------------------
@router.callback_query(F.data.startswith("add_to_"))
async def add_to_list(callback: CallbackQuery) -> None:
    tg_id = callback.from_user.id
    global films
    list_type = callback.data.split("_")[-1]
    try:
        film_id = films.get(tg_id)[current_page].get("id")
    except AttributeError:
        film_id = films.get(tg_id)[current_page].movie_id
    await db.modify_request_parameter(film_id, callback.from_user.id, f"movie_{list_type}", True)
    logger.info(f"User {tg_id} added film {film_id} to {list_type}")
    await callback.answer(f"Фильм добавлен в {list_type}")
# endregion
# ---------------------------------------------------------


# ---------------------------------------------------------
# region High and Low Budget Movie Handlers
# ---------------------------------------------------------
@router.message(Command("high_budget_movie"))
async def high_budget_movie_command(message: Message) -> None:
    logger.info(f"User {message.from_user.id} requested high budget movies")
    await search_by_cmd(message, budget=HIGH_BUDGET)

@router.message(Command("low_budget_movie"))
async def low_budget_movie_command(message: Message) -> None:
    logger.info(f"User {message.from_user.id} requested low budget movies")
    await search_by_cmd(message, budget=LOW_BUDGET)

@router.callback_query(F.data == "high_budget_movie")
async def high_budget_movie_callback(callback: CallbackQuery) -> None:
    logger.info(f"User {callback.from_user.id} requested high budget movies via callback")
    await search_by_callback(callback, budget=HIGH_BUDGET)

@router.callback_query(F.data == "low_budget_movie")
async def low_budget_movie_callback(callback: CallbackQuery) -> None:
    logger.info(f"User {callback.from_user.id} requested low budget movies via callback")
    await search_by_callback(callback, budget=LOW_BUDGET)
# endregion
# ---------------------------------------------------------



# ---------------------------------------------------------
# region Search Functions
# ---------------------------------------------------------
async def search_by_callback(callback: CallbackQuery, films_query: dict = None, budget: str = None) -> None:
    if budget:
        await callback.answer("Формируем запрос кинопоиску...")
        movies_cards = await http_session_start(query=BASE_SEARCH_QUERY, budget=budget)
    else:
        movies_cards = await http_session_start(BASE_SEARCH_QUERY, films_query)
    if isinstance(movies_cards, list):
        tg_id = callback.from_user.id
        global films
        films[tg_id] = list()
        films[tg_id] = [movie for movie in movies_cards if check_card(movie)]
        await callback.message.edit_text(return_film_info(films.get(tg_id)[0]), reply_markup=kb.pag_func())
        for movie in movies_cards:
            if check_card(movie):
                await db.add_record(movie, tg_id)
    else:
        await callback.message.reply_sticker(STICKERS.get("why"))
        await callback.message.answer(
            "Не удалось найти фильмы по указанным критериям.",
            reply_markup=kb.start_keyboard,)


async def search_by_cmd(
        message: Message,
        films_query: dict = None,
        budget: str = None,
        name: str = None) -> None:
    if budget:
        await message.answer("Формируем запрос кинопоиску...")
        movies_cards = await http_session_start(query=BASE_SEARCH_QUERY, budget=budget)
    elif name:
        print(name)
        movies_cards = await http_session_start(query=SEARCH_BY_NAME_QUERY, query_name=name)
    else:
        movies_cards = await http_session_start(query=BASE_SEARCH_QUERY, add_to_query=films_query)
    if isinstance(movies_cards, list):
        tg_id = message.from_user.id
        global films
        films[tg_id] = list()
        films[tg_id] = [movie for movie in movies_cards if check_named_card(movie)]
        try:
            first_film = films.get(tg_id)[0]
        except IndexError:
            await message.answer("Фильмы не найдены.")
            return
        else:
            await message.answer(return_film_info(first_film), reply_markup=kb.pag_func())
            for movie in movies_cards:
                if movie and check_named_card(movie):
                    await db.add_record(movie, tg_id)
    else:
        await message.reply_sticker(STICKERS.get("why"))
        await message.answer("Не удалось найти фильмы по указанным критериям.", reply_markup=kb.start_keyboard,)

# endregion
# ---------------------------------------------------------
