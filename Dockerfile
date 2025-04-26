# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --upgrade pip
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Sync the project into a new environment, asserting the lockfile is up to date
RUN uv sync --locked --no-dev
# Expose port (FastAPI default)
EXPOSE 8000

# Start the app
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

