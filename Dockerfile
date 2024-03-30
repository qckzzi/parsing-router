FROM python:3.12.2-slim

RUN pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry install --only main --no-root

COPY parsing_router /parsing_router

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENTRYPOINT ["poetry", "run", "faststream", "run", "parsing_router/main:app", "--log-level", "debug"]