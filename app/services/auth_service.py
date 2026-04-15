from __future__ import annotations

from app.db.database import DatabaseManager


class AuthService:
    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def login(self, username: str, password: str) -> bool:
        with self.db.get_connection() as connection:
            row = connection.execute(
                "SELECT id FROM users WHERE username = ? AND password = ?",
                (username.strip(), password.strip()),
            ).fetchone()
        return row is not None
