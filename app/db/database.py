from __future__ import annotations

import sqlite3
from pathlib import Path

from app.utils.paths import DB_PATH, SQL_DIR, ensure_directories


class DatabaseManager:
    def __init__(self, db_path: Path = DB_PATH) -> None:
        # Tao san cac thu muc can dung truoc khi lam viec voi database.
        ensure_directories()
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        # row_factory giup truy cap cot theo ten, vi du row["full_name"].
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self) -> None:
        # Doc file schema.sql va tao bang neu chua ton tai.
        schema_path = SQL_DIR / "schema.sql"
        schema_sql = schema_path.read_text(encoding="utf-8")
        with self.get_connection() as connection:
            connection.executescript(schema_sql)

            # Tao tai khoan mac dinh de dang nhap demo nhanh.
            connection.execute(
                """
                INSERT OR IGNORE INTO users (username, password, full_name, role, created_at)
                VALUES (?, ?, ?, ?, datetime('now', 'localtime'))
                """,
                ("admin", "admin123", "Administrator", "admin"),
            )

            # Tao san 1 lop mac dinh de nguoi dung co the them sinh vien ngay.
            connection.execute(
                """
                INSERT OR IGNORE INTO classes (class_code, class_name, created_at)
                VALUES (?, ?, datetime('now', 'localtime'))
                """,
                ("CNTT-K1", "Cong nghe thong tin K1"),
            )
