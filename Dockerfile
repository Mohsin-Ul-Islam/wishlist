FROM python:3.10 as production

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry install --no-dev

COPY ./wishlist ./wishlist

CMD [ "sh", "-c", "uvicorn --host 0.0.0.0 --port ${PORT:-8080} wishlist.app:app" ]
