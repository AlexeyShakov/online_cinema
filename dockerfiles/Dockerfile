FROM python:3.10.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y gettext

WORKDIR /usr/src/online_cinema

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./ README.md ./

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

COPY src/ src/

CMD ["poetry", "run", "python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
