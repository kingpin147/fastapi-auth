FROM python:3.12

LABEL Maintainer="M Nouman Aattique"

WORKDIR /code

COPY . /code/

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi

CMD ["uvicorn", "fastapi_auth.main:app", "--host", "0.0.0.0", "--port", "8000"]