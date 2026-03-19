# ── Stage 1: install UIKit via npm ────────────────────────────────────────────
FROM node:22-slim AS ui-builder

WORKDIR /build
COPY package.json package-lock.json* ./
RUN npm ci --omit=dev

# ── Stage 2: Python application ───────────────────────────────────────────────
FROM python:3.13-slim AS app

# Install uv for fast, reproducible dependency installation
RUN pip install --no-cache-dir uv

WORKDIR /app

# Install Python dependencies (no venv needed inside the container)
COPY pyproject.toml ./
RUN uv pip install --system --no-cache -r pyproject.toml 2>/dev/null || \
    uv pip install --system --no-cache \
        "fastapi>=0.135.1" \
        "peewee>=4.0.1" \
        "python-multipart>=0.0.22" \
        "uvicorn[standard]>=0.41.0"

# Copy application source
COPY rose/ ./rose/
COPY ui/ ./ui/

# Copy UIKit dist from the Node build stage
COPY --from=ui-builder /build/node_modules/uikit/dist ./node_modules/uikit/dist

# books.db lives in /data so it can be mounted as a volume
RUN mkdir -p /data
ENV DB_PATH=/data/books.db

EXPOSE 8000

CMD ["uvicorn", "rose.main:app", "--host", "0.0.0.0", "--port", "8000"]
