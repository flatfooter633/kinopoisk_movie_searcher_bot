import os
from dotenv import load_dotenv, find_dotenv

LOW_BUDGET = "100-50000"
HIGH_BUDGET = "9000000-9999999999"

HI_ARRAY = {'hi', 'hello', 'good', 'привет', 'здоров', 'здравствуй', 'здравствуйте', 'menu', 'start', 'меню', 'старт'}

HOW_ARE_YOU_ANSWER = [
    "Чем дальше, тем страшнее.",
    "Спасибо, дела регулярно.",
    "Бьет ключом, да всё по голове.",
    "Как на марсе. Почему? – Никакой жизни.",
    "Не знаю…",
    "Как на бахче. Арбуз растет, а кончик сохнет.",
    "Еще не родила…",
    "Вы обознались… это не я.",
    "Дела идут хорошо, но мимо.",
    "Как у зебры: белая полоска, черная полоска.",
    "Не знаю, прокурор заболел",
    "А тебе зачем? =)",
    "Мой психиатр посоветовал мне не обсуждать это с малознакомыми людьми.",
    "Если есть в кармане пачка сигарет, значит все не так уж плохо на сегодняшний день.",
    "Дела как у тебя, только значительно лучше.",
    "Херошо!",
    "Еще не завели, но в нашем государстве все может быть.",
    "Если было бы еще лучше, то это было бы незаконно.",
]

# Загрузка переменных окружения из файла.env
# Если файла.env нет, то окружение не загружается и приложение завершается с сообщением об ошибке.
if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

# Токен API кинопоиска
API_KEY = os.getenv("API_KEY")
# Токен бота можно получить через @BotFather в Telegram
TOKEN = os.getenv("TOKEN")


# Настройки REDIS
REDIS_HOST = os.getenv("REDIS_HOST", "redis")  # Используем имя сервиса из docker-compose
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# ['announced', 'completed', 'filming', 'post-production', 'pre-production']
# ['animated-series', 'anime', 'cartoon', 'movie', 'tv-series']


# Список стикеров
STICKERS = {
    "search": "CAACAgIAAxkBAAEHUMhmqOKVqjDJvavilI7sqxYEv0LYoQAC2RgAAnUWUEmUQAHVSkl_pzUE",
    "selection": "CAACAgIAAxkBAAEHUflmqQXECFTmYlOfAzeGry7KTJaFEAAC7hQAAuNVUEk4S4qtAhNhvDUE",
    "start": "CAACAgIAAxkBAAEHUd9mqQNOmo_aKPi1L52HbA-wdA7bKwAChxUAAj0PUEnem2b91sejvzUE",
    "error": "CAACAgIAAxkBAAEHYexmq-NPtIxB3COd6MNqjSZ-qUNsiQACyxQAAt2wUUlMYGw0MqQdYTUE",
    "why": "CAACAgIAAxkBAAEHYf9mq-SRYC-9CPpAOlh9pBGdYjKbZQAC6BgAAoCaGElH6JHLA5DZuTUE",
    "go": "CAACAgIAAxkBAAEHY71mrHOgBsgHiJTw5H0wMONhYLR4xgACfQADQbVWDMI7otqy4CWANQQ",
    "wow": "CAACAgIAAxkBAAEHY7tmrHObSNWJeYy4Ohp-ftnA_5Ch_QACawADQbVWDPrzm0b7fXuVNQQ",
    "boom": "CAACAgIAAxkBAAEHY7lmrHOSkKMKQBVibnqfY-kccJmWvgACagADQbVWDKyZ8RxfRvjjNQQ",
    "hello": "CAACAgIAAxkBAAEHY7dmrHOQHKwqkOfB52nJ7HDWbXx1XQACbgADQbVWDNClhHLm3FqINQQ",
    "ok": "CAACAgIAAxkBAAEHY7VmrHOCeovwmvyG9is1iQS3dMRHIgACcQADQbVWDFigEETauxe_NQQ",
    "oops": "CAACAgIAAxkBAAEHY79mrHO3hfdWj31Q8XgXG3AZ21rpOAACcgADQbVWDBovm1aDtrOwNQQ",
    "ouch": "CAACAgIAAxkBAAEHY8FmrHPBsRLIsjXlZ9ONRleFj3bhqQACeAADQbVWDNm6y3pBU7OPNQQ",
    "not_found": "CAACAgIAAxkBAAEHYhFmq-lGpy-1TY35mzeKW3RfzWrKygACYhgAAjx6UEnKFDnPOcbwvzUE",
    "done": "CAACAgIAAxkBAAEHYg1mq-gTcmNmnf5UqU56BowsNqBBCwAC_RkAAmzaUUlkoYIx4TqiCjUE",
    "stop": "CAACAgIAAxkBAAEHYfBmq-OsOkNojsClk9oEF0Ddb_8BPgACChUAAl_zwUl2NIzsRPf4fzUE",
    "help": "CAACAgIAAxkBAAEHUeFmqQRvZTB8vv7jYCFzZxcIdrXOxQACwxMAAm3oEEqGY8B94dy6NDUE",
}
# Список стран
COUNTRIES_LIST = [
    "Австралия",
    "Австрия",
    "Аргентина",
    "Бельгия",
    "Бразилия",
    "Великобритания",
    "Германия",
    "Германия (ГДР)",
    "Германия (ФРГ)",
    "Греция",
    "Грузия",
    "Дания",
    "Джибути",
    "Израиль",
    "Индия",
    "Ирландия",
    "Исландия",
    "Испания",
    "Италия",
    "Казахстан",
    "Канада",
    "Китай",
    "Корея",
    "Корея Северная",
    "Корея Южная",
    "Куба",
    "Латвия",
    "Литва",
    "Мексика",
    "Нидерланды",
    "Новая Зеландия",
    "Новая Каледония",
    "Норвегия",
    "Польша",
    "Португалия",
    "Российская империя",
    "Россия",
    "Румыния",
    "СССР",
    "США",
    "Сербия",
    "Сербия и Черногория",
    "Словакия",
    "Словения",
    "Турция",
    "Украина",
    "Финляндия",
    "Франция",
    "Чехия",
    "Чехословакия",
    "Чили",
    "Швейцария",
    "Швеция",
    "ЮАР",
    "Япония",
]
# Список жанров
GENRE_LIST = [
    "аниме",
    "биография",
    "боевик",
    "вестерн",
    "военный",
    "детектив",
    "детский",
    "для взрослых",
    "документальный",
    "драма",
    "игра",
    "история",
    "комедия",
    "концерт",
    "короткометражка",
    "криминал",
    "мелодрама",
    "музыка",
    "мультфильм",
    "мюзикл",
    "новости",
    "приключения",
    "реальное ТВ",
    "семейный",
    "спорт",
    "ток-шоу",
    "триллер",
    "ужасы",
    "фантастика",
    "фильм-нуар",
    "фэнтези",
    "церемония",
]

# Базовый Запрос поиска по названию фильма
SEARCH_BY_NAME_QUERY = {
    "url": "https://api.kinopoisk.dev/v1.4/movie/search",
    "query_params": {
        "page": 1,
        "limit": 10,
    },
    "headers": {
        "accept": "application/json",
        "X-API-KEY": API_KEY,
    },
}


# Базовый Запрос поиска по жанру и стране
BASE_SEARCH_QUERY = {
    "url": "https://api.kinopoisk.dev/v1.4/movie",
    "query_params": {
        "page": 1,
        "limit": 15,
        "sortField": "votes.imdb",
        "sortType": -1,
        "selectFields": [
            "id",
            "name",
            "alternativeName",
            "budget",
            # "fees",
            "description",
            "rating",
            "year",
            "type",
            # "facts",
            "genres",
            "ageRating",
            "countries",
            "poster",
            # "similarMovies",
            # "sequelsAndPrequels",
            # "persons",
        ],
        "notNullFields": [
            "id",
            "name",
            "alternativeName",
            "description",
            "year",
            "rating.kp",
            "ageRating",
            "budget.value",
            "budget.currency",
            "genres.name",
            "countries.name",
            "poster.url",
            # "persons.id",
            # "persons.name",
            # "persons.description",
            # "persons.profession",
            # "facts.type",
            # "facts.value",
            # "facts.spoiler",
            # "similarMovies.id",
            # "similarMovies.name",
            # "similarMovies.alternativeName",
            # "similarMovies.year",
            # "sequelsAndPrequels.id",
            # "sequelsAndPrequels.name",
        ],
        "type": ["animated-series", "anime", "cartoon", "movie", "tv-series"],
        # "budget.value": "1000 - 9000000",
    },
    "headers": {
        "accept": "application/json",
        "X-API-KEY": API_KEY,
    },
}
# Текст помощи бота
HELP_TEXT = (
    f"Справка по основным командам и функциям поиска фильмов.\n"
    f"\nКоманды:\n"
    f"  ☑️/start - основное меню\n"
    f"  📖/history - история запросов\n"
    f"\nПоиск фильма/сериала:\n"
    f"  🎥/movie_search - по названию\n"
    f"  🎬/movie_by_param - по параметрам\n"
    f"  💩/low_budget_movie - с низким бюджетом\n"
    f"  💰/high_budget_movie - с высоким бюджетом\n"
)

START_TEXT = (
    f"\n☑️Нажав на кнопку\n<b>👉🏼[Подобрать по параметрам]👈🏼</b>\nможешь задать "
    f"мне ключевые параметры:\n🎭жанр,\n🍿год,\n🌟рейтинг\nи я подберу подходящие фильмы.\n"
    f"\n☑️Нажав на кнопку\n<b>👉🏼[Поиск по названию]👈🏼</b>\nвведи название фильма и я его найду.\n"
    f"\n🫵🏼Нажми нужную кнопку: "
)
GREETING_VARIANTS = [
    "Я помогу тебе найти любимые фильмы!",
    "Добро пожаловать в мир кино! Я помогу тебе выбрать интересный фильм.",
    "Я помогу тебе подобрать интересный 🎞фильм для просмотра.",
    "Я здесь, чтобы помочь тебе найти лучшие фильмы.",
    "Я рад помочь тебе с выбором фильма!",
    "Я с удовольствием помогу тебе найти твои любимые фильмы!",
    "Я с радостью помогу тебе найти твои любимые фильмы!",
]


# 📆📅🪣⚔️⛓🏺⚰️🛒🎁⏰⏱🕰⏳🧭🎛📺☎️💡🕯🧯⚖️🪓🎃🫵🏼👈🏼👉🏼🫷🏼🫸🏼 🤡💩👻🤖👽🤠🤡💩👻🤖👽🥷🏻🧛🏻‍♂️🧜🏼‍♀️🧞‍♂️🧞🧚🏻‍♂️🌍🌟🍿🍭🍼🎭🎬🎥📽🎞💰🛠⚙️💳💣📖💤🔚🔙🔛🔝🔜✔️☑️🔘©️®️™️🎵🎶➕➖🟰✖️➗🇺🇸🇷🇺
def return_film_info(input_card) -> str:
    try:
        budget = input_card.get("budget").get("value")
        currency = input_card.get("budget").get("currency")
    except AttributeError:
        budget_string = ""
    else:
        budget_string = f"\n💳Бюджет: <b>{budget:,} {currency}</b>"

    try:
        search_date = input_card.search_date
    except AttributeError:
        text = (
            f'\n🎥Название:\n<b><a href="{input_card.get("poster").get("url")}">{input_card.get("name")}</a></b>\n'
            f'\n🎬Оригинальное название:\n<u>{input_card.get("alternativeName")}</u>\n'
            f'\n🍿Год: <b>{input_card.get("year")}</b>'
            f"{budget_string}"
            f'\n🍼Возрастной рейтинг: <b>{input_card.get("ageRating")}+</b>'
            f'\n🌟Рейтинг Кинопоиска: <b>{round(input_card.get("rating").get("kp"), 1)}</b>'
            f'\n🎭Жанры: <b>{", ".join(genre.get("name") for genre in input_card.get("genres"))}</b>'
            f'\n🌍Страны: <b>{", ".join(country.get("name") for country in input_card.get("countries"))}</b>\n'
            f'\n📖Описание:\n<i>{input_card.get("description")}</i>'
        )
    else:
        text = (
            f"📆Дата и время поиска: <b>{search_date:%d.%m.%Y %H:%M}</b>\n"
            f'\n🎥Название:\n<b><a href="{input_card.poster_url}">{input_card.movie_name}</a></b>\n'
            f"\n🍿Год: <b>{input_card.year}</b>"
            f"\n🍼Возрастной рейтинг: <b>{input_card.age_rating}+</b>"
            f"\n🌟Рейтинг Кинопоиска: <b>{input_card.rating}</b>"
            f"\n🎭Жанры: <b>{input_card.genre}</b>"
            f"\n📖Описание:\n<i>{input_card.movie_description}</i>"
        )

    return text
