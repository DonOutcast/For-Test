FROM python:3.12-slim AS  base

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR=1


RUN apt-get update && \
    apt-get install -y --no-install-recommends libffi-dev libpq-dev liblz4-dev libunwind-dev && \
    pip install --upgrade pip poetry && \
    apt-get clean



FROM base AS  builder
WORKDIR $PYTHONPATH
COPY ./backend/pyproject.toml ./backend/poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi


FROM builder AS  user_setup
RUN groupadd -r -g 1000 app_group && useradd -r -g app_group -u 1000 app_user && \
    chown -R app_user:app_group $PYTHONPATH

FROM user_setup AS  development
COPY --from=builder $PYTHONPATH $PYTHONPATH
COPY ./backend/ $PYTHONPATH/

CMD ["bash", "-c", "python3 manage.py collectstatic --noinput && python3 manage.py runserver 0.0.0.0:8000"]
