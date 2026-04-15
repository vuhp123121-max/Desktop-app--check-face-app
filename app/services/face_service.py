from __future__ import annotations

import ctypes
import json
import shutil
import tempfile
from pathlib import Path

import cv2
import numpy as np

from app.db.database import DatabaseManager
from app.services.student_service import StudentService
from app.utils.helpers import now_text
from app.utils.paths import DATASET_DIR


class FaceService:
    def __init__(self, db: DatabaseManager, student_service: StudentService) -> None:
        self.db = db
        self.student_service = student_service
        cascade_path = self._prepare_cascade_file()
        self.cascade = cv2.CascadeClassifier(self._opencv_safe_path(cascade_path))

    def _prepare_cascade_file(self) -> Path:
        source = Path(cv2.data.haarcascades) / 'haarcascade_frontalface_default.xml'
        local_dir = Path(tempfile.gettempdir()) / 'big_projject_cascades'
        local_dir.mkdir(parents=True, exist_ok=True)
        local_path = local_dir / 'haarcascade_frontalface_default.xml'
        if source.exists() and not local_path.exists():
            shutil.copyfile(source, local_path)
        if not local_path.exists():
            raise FileNotFoundError(f'Khong tim thay file cascade: {source}')
        return local_path

    def _opencv_safe_path(self, path: Path) -> str:
        raw_path = str(path)
        if not hasattr(ctypes, 'windll'):
            return raw_path
        buffer = ctypes.create_unicode_buffer(260)
        result = ctypes.windll.kernel32.GetShortPathNameW(raw_path, buffer, len(buffer))
        return buffer.value if result else raw_path

    def _write_image(self, path: Path, image) -> bool:
        extension = path.suffix or '.jpg'
        success, buffer = cv2.imencode(extension, image)
        if not success:
            return False
        buffer.tofile(str(path))
        return True

    def _read_gray_image(self, path: Path):
        data = np.fromfile(str(path), dtype=np.uint8)
        if data.size == 0:
            return None
        return cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)

    def _open_camera(self) -> cv2.VideoCapture:
        candidates = [
            (0, cv2.CAP_DSHOW),
            (0, cv2.CAP_MSMF),
            (1, cv2.CAP_DSHOW),
            (1, cv2.CAP_MSMF),
            (0, cv2.CAP_ANY),
            (1, cv2.CAP_ANY),
        ]
        for index, backend in candidates:
            camera = cv2.VideoCapture(index, backend)
            if camera.isOpened():
                ok, _frame = camera.read()
                if ok:
                    return camera
            camera.release()
        return cv2.VideoCapture()

    def capture_samples(self, student_id: int, student_code: str, sample_count: int = 10) -> tuple[bool, str]:
        if self.cascade.empty():
            return False, 'Khong tai duoc bo nhan dien khuon mat OpenCV.'
        student_dir = DATASET_DIR / student_code
        student_dir.mkdir(parents=True, exist_ok=True)
        camera = self._open_camera()
        if not camera.isOpened():
            return False, 'Khong mo duoc webcam. Hay thu dong ung dung camera khac, doi camera 0/1 hoac rut-cam lai webcam.'
        captured_paths: list[str] = []
        try:
            while len(captured_paths) < sample_count:
                ok, frame = camera.read()
                if not ok:
                    break
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
                for (x, y, w, h) in faces[:1]:
                    face_roi = frame[y : y + h, x : x + w]
                    face_roi = cv2.resize(face_roi, (200, 200))
                    image_path = student_dir / f'sample_{len(captured_paths) + 1:02d}.jpg'
                    if self._write_image(image_path, face_roi):
                        captured_paths.append(str(image_path))
                    else:
                        continue
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, f'Captured {len(captured_paths)}/{sample_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    break
                cv2.imshow('Dang ky khuon mat - Nhan Q de dung', frame)
                if cv2.waitKey(250) & 0xFF == ord('q'):
                    break
        finally:
            camera.release()
            cv2.destroyAllWindows()
        if not captured_paths:
            return False, 'Chua chup duoc anh khuon mat nao.'
        with self.db.get_connection() as connection:
            for image_path in captured_paths:
                connection.execute('INSERT INTO face_samples (student_id, image_path, captured_at) VALUES (?, ?, ?)', (student_id, image_path, now_text()))
        embedding_path = self._build_simple_embedding(student_dir)
        self.student_service.update_face_data(student_id, captured_paths[0], str(embedding_path))
        return True, f'Da luu {len(captured_paths)} anh khuon mat.'

    def _build_simple_embedding(self, student_dir: Path) -> Path:
        histograms: list[list[float]] = []
        for image_path in student_dir.glob('*.jpg'):
            image = self._read_gray_image(image_path)
            if image is None:
                continue
            resized = cv2.resize(image, (100, 100))
            histogram = cv2.calcHist([resized], [0], None, [32], [0, 256]).flatten()
            normalized = cv2.normalize(histogram, histogram).flatten().tolist()
            histograms.append(normalized)
        mean_hist = np.mean(np.array(histograms), axis=0).tolist() if histograms else []
        embedding_path = student_dir / 'embedding.json'
        embedding_path.write_text(json.dumps({'histogram': mean_hist}), encoding='utf-8')
        return embedding_path

    def recognize_and_mark(self, attendance_service) -> tuple[bool, str]:
        if self.cascade.empty():
            return False, 'Khong tai duoc bo nhan dien khuon mat OpenCV.'
        students = self.student_service.list_students()
        known_faces = []
        for student in students:
            embedding_path = student.get('embedding_path')
            if not embedding_path:
                continue
            path = Path(embedding_path)
            if not path.exists():
                continue
            data = json.loads(path.read_text(encoding='utf-8'))
            histogram = np.array(data.get('histogram', []), dtype=np.float32)
            if histogram.size == 0:
                continue
            known_faces.append((student, histogram))
        if not known_faces:
            return False, 'Chua co du lieu khuon mat de nhan dien.'
        camera = self._open_camera()
        if not camera.isOpened():
            return False, 'Khong mo duoc webcam. Hay thu dong ung dung camera khac, doi camera 0/1 hoac rut-cam lai webcam.'
        result_message = 'Khong nhan dien duoc sinh vien.'
        matched = False
        try:
            for _ in range(120):
                ok, frame = camera.read()
                if not ok:
                    continue
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
                for (x, y, w, h) in faces[:1]:
                    face_roi = gray[y : y + h, x : x + w]
                    face_roi = cv2.resize(face_roi, (100, 100))
                    histogram = cv2.calcHist([face_roi], [0], None, [32], [0, 256]).flatten()
                    histogram = cv2.normalize(histogram, histogram).flatten()
                    best_student = None
                    best_score = -1.0
                    for student, known_hist in known_faces:
                        score = cv2.compareHist(histogram, known_hist, cv2.HISTCMP_CORREL)
                        if score > best_score:
                            best_score = score
                            best_student = student
                    label = 'Unknown'
                    if best_student and best_score >= 0.80:
                        success, message = attendance_service.mark_attendance(best_student['id'])
                        label = f"{best_student['full_name']} ({best_score:.2f})"
                        result_message = message
                        matched = success
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.imshow('Diem danh khuon mat - Nhan Q de dung', frame)
                    cv2.waitKey(1200)
                    return matched, result_message
                cv2.imshow('Diem danh khuon mat - Nhan Q de dung', frame)
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break
        finally:
            camera.release()
            cv2.destroyAllWindows()
        return matched, result_message
