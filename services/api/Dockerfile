FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system dependencies for psycopg2 and build tools
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Set environment variables required by alembic
ENV PYTHONPATH=/app

CMD ["bash", "-c", "cd /app && alembic upgrade head && python -m services.etl.run_all && uvicorn services.api.main_final:app --host 0.0.0.0 --port 8000"]