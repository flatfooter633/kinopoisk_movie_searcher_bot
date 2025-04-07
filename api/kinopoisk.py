from logging import getLogger
from copy import deepcopy
from aiohttp.client_exceptions import ClientConnectorError
from typing import Dict, Optional, Any, List

import aiohttp
import asyncio

# Получение логгера
logger = getLogger("api_logger")


async def get_movies(
        session: aiohttp.ClientSession,
        url: str,
        headers: Dict[str, str],
        query_params: Dict[str, Any]
) -> Optional[List[Dict[str, Any]]]:
    try:
        async with session.get(url, headers=headers, params=query_params, timeout=10) as response:
            if response.status != 200:
                raise Exception(
                    f"Ошибка HTTP-запроса. Запрос не выполнен с кодом состояния {response.status}"
                )
            result = await response.json()
            if result.get("total") > 0:
                logger.info("Информация о фильмах загружена")
                return result.get("docs")
            else:
                raise Exception(
                    "Фильмы, соответствующие указанным параметрам, не найдены."
                )
    except Exception as e:
        logger.error(f"Ошибка получения информации: {e}")
        return None


async def selection_of_movies(
        session: aiohttp.ClientSession,
        query_dict: Dict[str, Any],
        add_to_query: Optional[Dict[str, Any]] = None,
        query_name: Optional[str] = None,
        budget: Optional[str] = None
) -> Optional[List[Dict[str, Any]]]:
    result_query = deepcopy(query_dict)
    if query_name is not None:
        result_query["query_params"]["query"] = query_name
    elif add_to_query is not None:
        result_query["query_params"]["limit"] = add_to_query.get("limit")
        result_query["query_params"]["countries.name"] = add_to_query.get("countries")
        result_query["query_params"]["year"] = add_to_query.get("years")
        result_query["query_params"]["rating.kp"] = add_to_query.get("ratings")
        result_query["query_params"]["ageRating"] = add_to_query.get("age_ratings")
        result_query["query_params"]["genres.name"] = add_to_query.get("genre")
    elif budget is not None:
        result_query["query_params"]["budget.value"] = budget
    url = result_query.get("url")
    query_params = result_query.get("query_params")
    headers = result_query.get("headers")
    logger.info(f"Запрос на получение информации о фильмах: {url}")
    return await get_movies(session, url, headers, query_params)


async def http_session_start(
        query: Dict[str, Any],
        add_to_query: Optional[Dict[str, Any]] = None,
        query_name: Optional[str] = None,
        budget: Optional[str] = None
) -> Optional[List[Dict[str, Any]]]:
    try:
        # Создание aiohttp-сессии
        async with aiohttp.ClientSession() as session:
            # Запрос на получение информации о фильмах по базовому запросу
            result = await asyncio.create_task(
                selection_of_movies(session, query, add_to_query, query_name, budget)
            )
    except ClientConnectorError:
        logger.error("Ошибка соединения с сервером")
        result = None
    return result
