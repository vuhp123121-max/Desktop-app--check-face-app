from __future__ import annotations

import csv
from pathlib import Path

from app.db.database import DatabaseManager
from app.utils.helpers import now_text, time_text, today_text


class AttendanceService:
    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def mark_attendance(self, student_id: int, status: str = "Co mat", note: str = "") -> tuple[bool, str]:
        # Moi sinh vien chi duoc diem danh 1 lan trong 1 ngay.
        attendance_date = today_text()
        with self.db.get_connection() as connection:
            existed = connection.execute("SELECT id FROM attendance WHERE student_id = ? AND attendance_date = ?", (student_id, attendance_date)).fetchone()
            if existed:
                return False, "Sinh vien da diem danh trong hom nay."

            connection.execute(
                """
                INSERT INTO attendance (student_id, attendance_date, check_in_time, status, note, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (student_id, attendance_date, time_text(), status, note.strip(), now_text()),
            )
        return True, "Diem danh thanh cong."

    def list_attendance(self, attendance_date: str = "", class_code: str = "", student_code: str = "") -> list[dict]:
        # Loc lich su theo ngay, lop va ma sinh vien de phuc vu tim kiem/bao cao.
        query = """
            SELECT a.id, s.student_code, s.full_name, c.class_code, a.attendance_date, a.check_in_time, a.status, a.note
            FROM attendance a
            JOIN students s ON s.id = a.student_id
            LEFT JOIN classes c ON c.id = s.class_id
            WHERE a.attendance_date LIKE ? AND IFNULL(c.class_code, '') LIKE ? AND s.student_code LIKE ?
            ORDER BY a.attendance_date DESC, a.check_in_time DESC
        """
        params = (f"%{attendance_date.strip()}%", f"%{class_code.strip()}%", f"%{student_code.strip()}%")
        with self.db.get_connection() as connection:
            rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]

    def today_total(self) -> int:
        # Dem nhanh tong so luot diem danh trong ngay de hien thi o dashboard.
        with self.db.get_connection() as connection:
            row = connection.execute("SELECT COUNT(*) AS total FROM attendance WHERE attendance_date = ?", (today_text(),)).fetchone()
        return int(row["total"])

    def export_csv(self, rows: list[dict], output_path: Path) -> Path:
        # Xuat bao cao CSV voi BOM de mo bang Excel khong bi loi tieng Viet.
        headers = ["student_code", "full_name", "class_code", "attendance_date", "check_in_time", "status", "note"]
        with output_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            for row in rows:
                writer.writerow({key: row.get(key, "") for key in headers})
        return output_path
