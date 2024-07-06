FROM python:3.12

WORKDIR /opt/app


COPY pyproject.toml poetry.lock /opt/app/

RUN pip install --no-compile --upgrade pip \
 && pip install --no-compile poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

COPY . .

CMD ["python", "main.py"]