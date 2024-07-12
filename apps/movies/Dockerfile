FROM python:3.12

WORKDIR /opt/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt update && pip install --upgrade pip
COPY pyproject.toml poetry.lock /opt/app/

RUN pip install --no-compile poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi


COPY . .

EXPOSE 8000
