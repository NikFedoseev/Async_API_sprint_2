FROM python:3.12

WORKDIR /opt/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt update && pip install --upgrade pip
COPY /requirements/base.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
