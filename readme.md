# Тема: Поиск фильмов на Кинопоиске
Этот бот представляет собой телеграм-бота, который помогает пользователям искать информацию о фильмах и сериалах.
Скрипт предназначен для обработки различных пользовательских команд, таких как поиск по названию, фильтрация по жанру и стране, а также получение подробной информации о фильме. 
Код включает функции для проверки пользовательского ввода, выполнения запросов к API и форматирования ответных сообщений для Telegram-бота.

Скрипт также содержит набор предопределенных переменных: 
* идентификаторы стикеров, 
* списки стран и жанров, 
* текст справки, 
* шаблоны запросов к API 
* и приветственные сообщения. 

Эти переменные используются во всем скрипте для обеспечения согласованного поведения и функциональности. 
Все важные данные, такие как API-ключи, токен бота, скрыты с помощью переменной окружения.

Сценарий хорошо документирован с комментариями, объясняющими назначение и функциональность каждого раздела. 
В нем приведены рекомендации по обработке ошибок, проверке вводимых данных и форматированию запросов API.

В целом, скрипт представляет собой комплексное решение для взаимодействия с Telegram-ботом и использования API Кинопоиска для поиска фильмов. 
Он предоставляет удобный интерфейс и различные функциональные возможности для получения информации о фильме на основе пользовательского ввода.
Данный скрипт проверяет вводимые пользователем данные для запросов поиска фильмов, используя комбинацию встроенных и пользовательских функций Python. 

## Асинхронный режим работы бота
Асинхронность работы данного бота обеспечивает следующие преимущества:

1. **Увеличение производительности:** 
Асинхронные операции позволяют выполнять несколько задач одновременно, что в свою очередь увеличивает общую производительность бота. Это особенно важно, когда боту необходимо обрабатывать большое количество запросов от пользователей.
######
2. **Уменьшение времени ожидания:** 
Благодаря асинхронности, бот может обрабатывать запросы пользователей параллельно, не ожидая завершения предыдущих операций. Это позволяет сократить время ожидания ответа от бота и улучшить пользовательский опыт.
######
3. **Отказоустойчивость:** 
Асинхронность помогает избежать блокировки всего приложения при возникновении ошибок в одной из операций. Если один из запросов зависнет или завершится с ошибкой, другие запросы будут продолжать обрабатываться, не влияя на работу бота в целом.
######
4. **Лучшее использование ресурсов:** 
Асинхронные операции позволяют боту эффективно использовать ресурсы системы, такие как память и процессор. Это особенно важно, когда боту необходимо обрабатывать большое количество запросов от пользователей.
######
5. **Улучшение масштабируемости:** 
Асинхронность позволяет боту легко масштабироваться, добавляя новые серверы или увеличивая мощность существующих серверов. Это особенно важно, когда боту необходимо обрабатывать большое количество запросов от пользователей.
######
6. **Улучшение безопасности:** 
Асинхронность помогает избежать блокировки всего приложения при возникновении ошибок в одной из операций. Это позволяет изолировать ошибки и предотвратить их распространение, что в свою очередь улучшает безопасность бота.


## Архитектура телеграм-бота

Архитектура проекта для бота — это важная составляющая его успеха.
Если она хорошо продумана, бот становится более простым в разработке и эффективным в использовании.
Также благодаря этому его удобно поддерживать.

Часто при построении архитектуры используют модульную функциональность.
Она позволяет создавать ботов или другие приложения с чёткой структурой и тем самым упрощает их разработку.
Каждая директория такого бота выполняет определённую функцию.


<table style="width: 100%; border-collapse: collapse; border: none; empty-cells: show; max-width: 100%; box-sizing: border-box;"><tbody style="box-sizing: border-box;"><tr style="user-select: none; box-sizing: border-box;"><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;"><strong style="font-weight: 700; box-sizing: border-box;">Директория</strong></p></td><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;"><strong style="font-weight: 700; box-sizing: border-box;">За что отвечает</strong></p></td></tr><tr style="user-select: none; box-sizing: border-box;"><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;">database/</p></td><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;">Работа с базой данных. Содержит модули для подключения, выполнения запросов и работы с моделями данных</p></td></tr><tr style="user-select: none; box-sizing: border-box;"><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;">api/</p></td><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;">Работа со сторонним сервисом через программный интерфейс (API). Содержит модули для запроса к сторонним сервисам и обработку ответов</p></td></tr><tr style="user-select: none; box-sizing: border-box;"><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;">handlers/</p></td><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;">Обработчики сообщений. Каждый обработчик соответствует определённой команде или типу сообщения</p></td></tr><tr style="user-select: none; box-sizing: border-box;"><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;">keyboards/</p></td><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;">Создание кнопок. Модули для генерации клавиатур с кнопками для удобного взаимодействия пользователя с ботом</p></td></tr><tr style="user-select: none; box-sizing: border-box;"><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;">states/</p></td><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;">Состояния. Хранение и управление состояниями диалога с пользователем</p></td></tr><tr style="user-select: none; box-sizing: border-box;"><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;">utils/</p></td><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;">Вспомогательные функции. Общие функции, используемые в разных модулях проекта</p></td></tr><tr style="user-select: none; box-sizing: border-box;"><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;">.env</p></td><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;">Переменные окружения. Хранение конфиденциальных данных, таких как API-ключи</p></td></tr><tr style="user-select: none; box-sizing: border-box;"><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;">config.py</p></td><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;">Конфигурационный файл. Настройка основных параметров бота, таких как токен доступа к Telegram и API</p></td></tr><tr style="user-select: none; box-sizing: border-box;"><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;">loader.py</p></td><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;">Инициализация бота. Подключение всех необходимых модулей и запуск бота</p></td></tr><tr style="user-select: none; box-sizing: border-box;"><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;">main.py</p></td><td style="vertical-align: top; text-align: left; min-width: 5px; box-sizing: border-box; user-select: text; border: 1px solid rgb(221, 221, 221);"><p style="margin-top: 0px; margin-bottom: 12px; color: var(--ui-sb-color-text-main); box-sizing: border-box; font-size: 1rem; line-height: 1.375;">Запуск бота из loader</p></td></tr></tbody></table>

Данный проект соответствует указанной архитектуре.

## Описание внешнего вида и пользовательского интерфейса (UI)

При запуске Python-скрипта окно телеграм-бота принимает следующие команды:

* **/start** — приветствие и регистрация пользователя в базе данных;
* **/help** — для получения справки о доступных командах бота;
* **/movie_search** — поиск фильма/сериала по названию;
* **/movie_by_param** — поиск фильмов/сериалов по параметрам;
* **/low_budget_movie** — поиск фильмов/сериалов с низким бюджетом;
* **/high_budget_movie** — поиск фильмов/сериалов с высоким бюджетом;
* **/history** — возможность просмотра истории запросов и поиска фильма/сериала.



В **сценарий поиска по параметрам** включены следующие **вопросы**:

* жанр фильма/сериала (комедия, ужасы, фантастика и так далее);
* страны производства фильма/сериала;
* год релиза фильма/сериала;
* рейтинг фильма/сериала;
* возрастной рейтинг фильма/сериала;
* количество выводимых вариантов.

В **вывод** каждого фильма/сериала включены:

* название,
* описание,
* рейтинг,
* год производства,
* жанр,
* возрастной рейтинг,
* постер.

В **вывод истории** запросов включены:

* дата поиска,
* название фильма/сериала,
* описание фильма/сериала,
* рейтинг,
* год производства,
* жанр,
* возрастной рейтинг,
* постер.

В дополнение к выше указанным функциям данный бот:
* при запросе истории уточняет, за какую дату показывать историю;
* выводит информацию о каждом фильме/сериале через [пагинацию](https://github.com/ksinn/python-telegram-bot-pagination?tab=readme-ov-file#usage);
* реализует в истории поиска кнопки для отметки просмотренных и непросмотренных фильмов и сериалов.


## Ссылки: 
* [API Кинопоиска](https://kinopoisk.dev/)
* Документация для неофициального API кинопоиска ([kinopoisk.dev](https://api.kinopoisk.dev/documentation)). 1.4 OAS 3.0
* [Полное руководство по SQLAlchemy](https://pythonru.com/biblioteki/vvedenie-v-sqlalchemy)
