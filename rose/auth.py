import hashlib
import secrets
from typing import Optional

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from .database import get_db
from .models import User

# ── Password helpers ──────────────────────────────────────────────────────────


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}:{hashed}"


def verify_password(password: str, stored: str) -> bool:
    try:
        salt, hashed = stored.split(":", 1)
        expected = hashlib.sha256((salt + password).encode()).hexdigest()
        return secrets.compare_digest(hashed, expected)
    except Exception:
        return False


# ── Session helpers ───────────────────────────────────────────────────────────


def get_current_user(request: Request, db: Session) -> Optional[User]:
    """Read the logged-in user from the signed session cookie.
    Pass db explicitly; not a FastAPI dependency itself."""
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.get(User, user_id)


# ── FastAPI dependencies ──────────────────────────────────────────────────────


def require_login(request: Request, db: Session = Depends(get_db)) -> User:
    """Dependency for API routes: raises HTTP 401 if not authenticated."""
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


def require_admin(request: Request, db: Session = Depends(get_db)) -> User:
    """Dependency for API routes: raises HTTP 403 if not an admin."""
    user = require_login(request, db)
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
