FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.6.1

# Set work directory
WORKDIR /app

# Copy poetry files and install dependencies
COPY pyproject.toml poetry.lock* ./

# Install dependencies with pip globally to avoid venv issues
RUN pip install fastapi uvicorn[standard] sqlalchemy alembic asyncpg pydantic[email] pydantic-settings passlib[argon2] argon2-cffi python-jose[cryptography] python-multipart httpx pytest pytest-asyncio slowapi structlog email-validator

# Copy application code
COPY . .

# Create keys directory
RUN mkdir -p /app/keys

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
