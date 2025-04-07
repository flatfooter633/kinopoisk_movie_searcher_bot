from database.models import async_session
from database.models import User, Request
from sqlalchemy import select
from datetime import datetime
from logging import getLogger

# Getting logger
logger = getLogger("db_logger")


async def set_user(tg_id: int, first_name: str, last_name: str) -> bool:
    """
    This function sets user information in the database.
    Parameters:
        tg_id (int): The Telegram ID of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
    Returns:
        bool: Returns False if the user information was successfully written to the database,
              True if the user information already exists in the database.
    """
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, first_name=first_name, last_name=last_name))
            logger.info(f"Information about user {tg_id} written to the database")
            await session.commit()
            return False
        else:
            logger.info(f"User information {tg_id} already exists in the database")
            return True


async def add_record(query: dict, tg_id: int) -> None:
    """
    This function adds a movie record to the database based on the provided query and Telegram ID.
    Parameters:
        - query (dict): A dictionary containing movie information such as id, name, 
            description, rating, year, genres, ageRating, and poster.
        - tg_id (int): The Telegram ID of the user.
    Returns:
        - None: The function does not return any value.
    The function checks if the movie record already exists in the database based on the tg_id and movie_id.
    If the record does not exist, it creates a new Request object 
    with the provided information and adds it to the database.
    It logs an information message indicating that the movie information has been loaded into the database.
    If the record already exists, it logs an information message indicating 
    that the movie information already exists in the database.
    """
    async with async_session() as session:
        availability = await session.scalar(
            select(Request).where(Request.tg_id == tg_id, Request.movie_id == query.get("id"))
        )
        if not availability:
            request = Request(
                search_date=datetime.now(),
                movie_id=query.get("id"),
                movie_name=query.get("name"),
                movie_description=query.get("description"),
                rating=round(query.get("rating").get("kp"), 1),
                year=query.get("year"),
                genre=", ".join(genre.get("name") for genre in query.get("genres")),
                age_rating=query.get("ageRating"),
                poster_url=query.get("poster").get("url"),
                tg_id=tg_id,
            )

            session.add(request)
            logger.info(f"Movie information {query.get("id")} loaded into the database")
            await session.commit()
        else:
            logger.info(f"Movie information {query.get("id")} already exists in the database")


async def modify_request_parameter(movie_id: int, user_id: int, parameter_name: str, new_value: bool) -> None:
    """
    This function modifies a specific parameter of a movie request in the database.
    Parameters:
        - movie_id (int): The unique identifier of the movie.
        - user_id (int): The Telegram ID of the user.
        - parameter_name (str): The name of the parameter to be modified.
        - new_value (bool): The new value to be assigned to the specified parameter.
    Returns:
        - None: The function does not return any value.
    The function first attempts to find a movie request in the database that matches the provided movie_id and user_id.
    If a matching request is found, the function uses Python's built-in `setattr` function 
    to dynamically set the value of the specified parameter.
    The modified request is then added to the session and committed to the database.
    If no matching request is found, an information message is logged indicating that the movie 
    with the specified ID does not exist in the database.
    """
    async with async_session() as session:
        request = await session.scalar(
            select(Request).where(Request.movie_id == movie_id, Request.tg_id == user_id)
        )
        if request:
            setattr(request, parameter_name, new_value)
            session.add(request)
            await session.commit()
            logger.info(f"The {parameter_name} state has been changed for the movie with ID {movie_id}")
        else:
            logger.info(f"The movie with ID {movie_id} does not exist in the database")


async def get_favorite_for_user(user_id: int) -> list:
    """
    Retrieves a list of favorite movie requests for a specific user from the database.

    Parameters:
    - user_id (int): The unique identifier of the user.

    Returns:
    - list: A list of Request objects representing the favorite movie requests for the specified user.

    This function uses an asynchronous context manager (async with) to handle database operations.
    It logs an information message indicating the user for whom the favorites are being retrieved.
    The function then uses SQLAlchemy's select statement to query the database for movie requests 
    where the tg_id matches the specified user_id and the movie_favorite flag is True.
    The results are returned as a list of Request objects.
    """
    async with async_session() as session:
        logger.info(f"Getting favorite for user{user_id}")
        return await session.scalars(
            select(Request).where(Request.tg_id == user_id, Request.movie_favorite)
        )


async def get_viewed_for_user(user_id: int) -> list:
    """
    Retrieves a list of viewed movie requests for a specific user from the database.

    Parameters:
    - user_id (int): The unique identifier of the user.

    Returns:
    - list: A list of Request objects representing the viewed movie requests for the specified user.

    This function uses an asynchronous context manager (async with) to handle database operations.
    It logs an information message indicating the user for whom the viewed requests are being retrieved.
    The function then uses SQLAlchemy's select statement to query the database for movie requests 
    where the tg_id matches the specified user_id and the movie_viewed flag is True.
    The results are returned as a list of Request objects.
    """
    async with async_session() as session:
        logger.info(f"Getting viewed for user{user_id}")
        return await session.scalars(
            select(Request).where(Request.tg_id == user_id, Request.movie_viewed)
        )


async def get_user_requests(user_id: int) -> list:
    """
    Retrieves a list of all movie requests for a specific user from the database.

    Parameters:
    - user_id (int): The unique identifier of the user.

    Returns:
    - list: A list of Request objects representing all movie requests for the specified user.

    This function uses an asynchronous context manager (async with) to handle database operations.
    It logs an information message indicating the user for whom the requests are being retrieved.
    The function then uses SQLAlchemy's select statement to query the database for all movie requests 
    where the tg_id matches the specified user_id.
    The results are returned as a list of Request objects.
    """
    async with async_session() as session:
        logger.info(f"Getting all requests for user{user_id}")
        return await session.scalars(select(Request).where(Request.tg_id == user_id))


async def get_user_history(user_id: int, date: str) -> list:
    """
    Retrieves a list of movie requests for a specific user and date from the database.

    Parameters:
    - user_id (int): The unique identifier of the user.
    - date (str): The date for which the movie requests should be retrieved.

    Returns:
    - list: A list of Request objects representing the movie requests for the specified user and date.

    This function uses an asynchronous context manager (async with) to handle database operations.
    It logs an information message indicating the user and date for which the requests are being retrieved.
    The function then uses SQLAlchemy's select statement to query the database for movie requests 
    where the tg_id matches the specified user_id and the search_date starts with the specified date.
    The results are returned as a list of Request objects.
    """
    async with async_session() as session:
        logger.info(f"Getting history for user{user_id} on date {date}")
        return await session.scalars(
            select(Request).where(Request.tg_id == user_id, Request.search_date.startswith(date))
        )


async def get_request(request_id: int) -> list:
    """
    Retrieves a specific movie request from the database based on the request ID.

    Parameters:
    - request_id (int): The unique identifier of the movie request.

    Returns:
    - Request: The Request object representing the movie request with the specified ID.

    This function uses an asynchronous context manager (async with) to handle database operations.
    It logs an information message indicating the request ID for which the request is being retrieved.
    The function then uses SQLAlchemy's select statement to query the database for a movie request 
    where the id matches the specified request_id.
    The result is returned as a single Request object.
    """
    async with async_session() as session:
        logger.info(f"Getting request with ID{request_id}")
        return await session.scalar(select(Request).where(Request.id == request_id))

# Define a dictionary to map callback data to database functions
functions = {
    "history": get_user_requests,
    "favorites": get_favorite_for_user,
    "viewed": get_viewed_for_user
}
