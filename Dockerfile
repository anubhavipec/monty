FROM python:3.11-slim

# 1. Install the Lambda Web Adapter
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.3 /lambda-adapter /opt/extensions/lambda-adapter

WORKDIR /app

# 2. Install poetry
RUN pip install poetry

# 3. Copy only dependency files
COPY pyproject.toml poetry.lock* /app/

# 4. Install dependencies (Crucial: note the space before --no-root)
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# 5. Copy the rest of the application code
COPY . /app

ENV PORT=8000
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]