FROM python:3.13-slim

# Install uv for fast dependency installation
RUN pip install --no-cache-dir uv

WORKDIR /app

# Install Python dependencies
COPY pyproject.toml ./
RUN uv pip install --system --no-cache \
    "fastapi>=0.115.0" \
    "uvicorn[standard]>=0.30.0" \
    "sqlalchemy>=2.0.0" \
    "jinja2>=3.1.0" \
    "pydantic[email]>=2.7.0" \
    "python-multipart>=0.0.9" \
    "aiosqlite>=0.20.0" \
    "itsdangerous>=2.1.0"

# Copy application source
COPY rose/ ./rose/
COPY templates/ ./templates/
COPY static/ ./static/

# Database lives in /data so it can be mounted as a volume
RUN mkdir -p /data
ENV DB_PATH=/data/rose.db

EXPOSE 8000

CMD ["uvicorn", "rose.main:app", "--host", "0.0.0.0", "--port", "8000"]

