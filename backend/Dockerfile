FROM python:3.11-slim

WORKDIR /app

RUN pip install "poetry==1.5.1"

COPY ./poetry.lock ./pyproject.toml /app/

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi --no-root

COPY backend/ .

COPY data /app/data

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]