# A Rose By Any Name

A personal reading-journal app built with **FastAPI**, **SQLAlchemy** (SQLite), **Jinja2**, and **htmx**.

## Features

- Browse books and read their details without signing in
- Full book management (add, edit, delete) for signed-in users
- Per-book feedback with rating, review, and year of reading
- User accounts managed exclusively by admins (no self-registration)
- Session-based authentication with a default admin seed on first run

## Access levels

| Page / action                 | Anonymous | Logged-in user | Admin |
| ----------------------------- | --------- | -------------- | ----- |
| Homepage (recent books)       | ✅        | ✅             | ✅    |
| Book detail (read-only)       | ✅        | ✅             | ✅    |
| Add / edit / delete books     | ❌        | ✅             | ✅    |
| Add / edit / delete feedbacks | ❌        | ✅             | ✅    |
| Books list page               | ❌        | ✅             | ✅    |
| Feedbacks list page           | ❌        | ✅             | ✅    |
| Own profile (view & edit)     | ❌        | ✅             | ✅    |
| User management (all users)   | ❌        | ❌             | ✅    |

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

## Default admin account

On first startup (empty database) a default admin user is created:

| Field    | Default value      |
| -------- | ------------------ |
| Email    | `admin@rose.local` |
| Password | `changeme`         |

**Change the password immediately in production.** Override the defaults via environment variables:

```bash
ADMIN_EMAIL=you@example.com ADMIN_PASSWORD=strongpassword uv run uvicorn rose.main:app
```

## Environment variables

| Variable         | Default            | Description                                                         |
| ---------------- | ------------------ | ------------------------------------------------------------------- |
| `DB_PATH`        | `rose.db`          | Path to the SQLite database file                                    |
| `SECRET_KEY`     | _(random)_         | Key used to sign session cookies — set a stable value in production |
| `ADMIN_EMAIL`    | `admin@rose.local` | Email for the seeded admin account (first run only)                 |
| `ADMIN_PASSWORD` | `changeme`         | Password for the seeded admin account (first run only)              |

## API

Interactive API docs are available at [http://localhost:8000/docs](http://localhost:8000/docs) when the server is running.
