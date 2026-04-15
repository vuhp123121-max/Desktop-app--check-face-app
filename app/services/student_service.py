from __future__ import annotations

from app.db.database import DatabaseManager
from app.utils.helpers import now_text


class StudentService:
    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def list_students(self, keyword: str = "") -> list[dict]:
        # Lay danh sach sinh vien va cho phep tim theo ma SV, ho ten hoac lop.
        query = """
            SELECT s.id, s.student_code, s.full_name, c.class_code, s.date_of_birth,
                   s.gender, s.face_image_path, s.embedding_path
            FROM students s
            LEFT JOIN classes c ON c.id = s.class_id
            WHERE s.student_code LIKE ? OR s.full_name LIKE ? OR IFNULL(c.class_code, '') LIKE ?
            ORDER BY s.student_code
        """
        term = f"%{keyword.strip()}%"
        with self.db.get_connection() as connection:
            rows = connection.execute(query, (term, term, term)).fetchall()
        return [dict(row) for row in rows]

    def get_student(self, student_id: int) -> dict | None:
        # Lay chi tiet 1 sinh vien de do vao form sua.
        with self.db.get_connection() as connection:
            row = connection.execute(
                """
                SELECT s.*, c.class_code, c.class_name
                FROM students s
                LEFT JOIN classes c ON c.id = s.class_id
                WHERE s.id = ?
                """,
                (student_id,),
            ).fetchone()
        return dict(row) if row else None

    def create_student(self, student_code: str, full_name: str, class_id: int | None, date_of_birth: str, gender: str) -> None:
        # Khi them moi, created_at va updated_at se cung mang mot moc thoi gian.
        timestamp = now_text()
        with self.db.get_connection() as connection:
            connection.execute(
                """
                INSERT INTO students (student_code, full_name, class_id, date_of_birth, gender, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (student_code.strip(), full_name.strip(), class_id, date_of_birth.strip(), gender.strip(), timestamp, timestamp),
            )

    def update_student(self, student_id: int, student_code: str, full_name: str, class_id: int | None, date_of_birth: str, gender: str) -> None:
        # Cap nhat thong tin sinh vien da ton tai.
        with self.db.get_connection() as connection:
            connection.execute(
                """
                UPDATE students
                SET student_code = ?, full_name = ?, class_id = ?, date_of_birth = ?, gender = ?, updated_at = ?
                WHERE id = ?
                """,
                (student_code.strip(), full_name.strip(), class_id, date_of_birth.strip(), gender.strip(), now_text(), student_id),
            )

    def delete_student(self, student_id: int) -> None:
        # Xoa du lieu lien quan truoc de tranh ban ghi mo coi.
        with self.db.get_connection() as connection:
            connection.execute("DELETE FROM face_samples WHERE student_id = ?", (student_id,))
            connection.execute("DELETE FROM attendance WHERE student_id = ?", (student_id,))
            connection.execute("DELETE FROM students WHERE id = ?", (student_id,))

    def update_face_data(self, student_id: int, face_image_path: str, embedding_path: str) -> None:
        # Luu duong dan anh mau va file embedding sau khi dang ky khuon mat.
        with self.db.get_connection() as connection:
            connection.execute(
                """
                UPDATE students
                SET face_image_path = ?, embedding_path = ?, updated_at = ?
                WHERE id = ?
                """,
                (face_image_path, embedding_path, now_text(), student_id),
            )
