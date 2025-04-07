from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramNetworkError
from logging import getLogger
from database.models import async_main
from config import TOKEN
from handlers.handlers import router  # Import the router module


async def main() -> None:
    """
    Инициализация экземпляра бота с использованием стандартных свойств и запуск диспетчера событий
    """
    # Все обработчики должны быть присоединены к диспетчеру (или роутеру)
    dp = Dispatcher(bot_token=TOKEN)

    # Получение логгера
    logger = getLogger("loader")

    # Экземпляр бота с использованием стандартных свойств и запуск диспетчера событий
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    try:
        await async_main()  # Initialize database connection
        dp.include_router(router)  # Include the router module
        await dp.start_polling(bot)  # Start polling
    except TelegramNetworkError as e:
        logger.error(f"Ошибка соединения с Telegram: [{e}]")
