# A Rose By Any Name

A personal reading-journal app built with **FastAPI**, **SQLAlchemy** (SQLite), **Jinja2**, and **htmx**.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (package manager)

## Run locally

```bash
# 1. Install Python dependencies
uv sync

# 2. Start the dev server
uv run uvicorn rose.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000).

The SQLite database (`rose.db`) is created automatically in the project root on first run.

## Run with Docker

```bash
docker compose up --build
```

Open [http://localhost:8000](http://localhost:8000).

Data is persisted in a named Docker volume (`rose-data`) and survives container restarts and rebuilds. To reset the database, remove the volume:

```bash
docker compose down -v
```

## Environment variables

| Variable  | Default   | Description                      |
| --------- | --------- | -------------------------------- |
| `DB_PATH` | `rose.db` | Path to the SQLite database file |

## API

Interactive API docs are available at [http://localhost:8000/docs](http://localhost:8000/docs) when the server is running.
