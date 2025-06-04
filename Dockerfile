FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
RUN pip install poetry && poetry install --no-dev
COPY luna ./luna
ENTRYPOINT ["poetry", "run", "luna"]
