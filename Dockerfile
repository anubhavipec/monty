# Use a lightweight Python base image
FROM python:3.9-slim

# Install poetry
RUN pip install poetry

# Set working directory
WORKDIR /app

# Copy dependency files first (for better caching)
COPY pyproject.toml poetry.lock* /app/

# Config poetry: don't create virtualenv inside container
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copy the rest of the application
COPY . /app

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]