# Используем официальный образ Python в качестве базового
FROM python:3.12.7-alpine3.20

# Основная команда запуска контейнера на удоленном сервере
# docker run -it --name kinobot -v $(pwd)/.env:/bot/.env --restart=unless-stopped -d flatfooter/kinopoisk_bot:final_version


LABEL maintainer="flatfooter633@gmail.com"
ENV ADMIN="flatfooter633"

# Обновим индекс доступных пакетов, обновим пакеты и установим bash
RUN apk update && apk upgrade && apk add bash && apk add nano


# Устанавливаем зависимости
COPY requirements.txt /bot/
RUN pip install --no-cache-dir -r /bot/requirements.txt

# Копируем файлы приложения
COPY . ./bot

# Устанавливаем рабочую директорию
WORKDIR /bot

# Указываем команду для запуска приложения
ENTRYPOINT ["python", "./main.py"]
