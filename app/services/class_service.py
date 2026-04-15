from __future__ import annotations

from app.db.database import DatabaseManager
from app.utils.helpers import now_text


class ClassService:
    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def list_classes(self) -> list[dict]:
        with self.db.get_connection() as connection:
            rows = connection.execute("SELECT id, class_code, class_name FROM classes ORDER BY class_code").fetchall()
        return [dict(row) for row in rows]

    def create_class(self, class_code: str, class_name: str) -> None:
        with self.db.get_connection() as connection:
            connection.execute(
                "INSERT INTO classes (class_code, class_name, created_at) VALUES (?, ?, ?)",
                (class_code.strip(), class_name.strip(), now_text()),
            )
