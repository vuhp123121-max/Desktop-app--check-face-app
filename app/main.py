from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from app.db.database import DatabaseManager
from app.services.attendance_service import AttendanceService
from app.services.auth_service import AuthService
from app.services.class_service import ClassService
from app.services.face_service import FaceService
from app.services.student_service import StudentService
from app.ui.attendance_frame import AttendanceFrame
from app.ui.dashboard_frame import DashboardFrame
from app.ui.face_registration_frame import FaceRegistrationFrame
from app.ui.history_frame import HistoryFrame
from app.ui.login_frame import LoginFrame
from app.ui.students_frame import StudentsFrame


class AttendanceApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("He thong diem danh khuon mat")
        self.geometry("1180x720")
        self.minsize(1024, 640)

        # Khoi tao database va cac service dung chung cho toan bo ung dung.
        self.db = DatabaseManager()
        self.db.initialize()
        self.auth_service = AuthService(self.db)
        self.class_service = ClassService(self.db)
        self.student_service = StudentService(self.db)
        self.attendance_service = AttendanceService(self.db)
        self.face_service = FaceService(self.db, self.student_service)

        # Man hinh dau tien la dang nhap. Sau khi dang nhap moi chuyen sang layout chinh.
        self.login_frame = LoginFrame(self, self)
        self.login_frame.pack(fill="both", expand=True)

        self.main_container = None
        self.content_container = None
        self.frames = {}

    def show_main_layout(self) -> None:
        # An man hinh dang nhap va tao bo cuc menu + khu vuc noi dung.
        self.login_frame.pack_forget()
        self.main_container = ttk.Frame(self, padding=8)
        self.main_container.pack(fill="both", expand=True)
        self.main_container.columnconfigure(1, weight=1)
        self.main_container.rowconfigure(0, weight=1)

        sidebar = ttk.Frame(self.main_container, padding=12)
        sidebar.grid(row=0, column=0, sticky="ns")
        ttk.Label(sidebar, text="Menu", font=("Segoe UI", 15, "bold")).pack(anchor="w", pady=(0, 12))

        self.content_container = ttk.Frame(self.main_container, padding=8)
        self.content_container.grid(row=0, column=1, sticky="nsew")
        self.content_container.rowconfigure(0, weight=1)
        self.content_container.columnconfigure(0, weight=1)

        # Moi muc menu se anh xa den mot frame giao dien rieng.
        screens = {
            "Dashboard": DashboardFrame,
            "Quan ly sinh vien": StudentsFrame,
            "Dang ky khuon mat": FaceRegistrationFrame,
            "Diem danh": AttendanceFrame,
            "Lich su va bao cao": HistoryFrame,
        }
        for name, frame_class in screens.items():
            ttk.Button(sidebar, text=name, command=lambda screen=name: self.show_screen(screen)).pack(fill="x", pady=4)
            frame = frame_class(self.content_container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[name] = frame

        self.show_screen("Dashboard")

    def show_screen(self, screen_name: str) -> None:
        # Chi hien thi 1 man hinh tai 1 thoi diem.
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[screen_name]
        frame.grid()
        frame.refresh_data()

    def refresh_dashboard(self) -> None:
        # Ham nay duoc goi sau khi them/xoa/diem danh de cap nhat thong ke nhanh.
        dashboard = self.frames.get("Dashboard")
        if dashboard:
            dashboard.refresh_data()


def run_app() -> None:
    app = AttendanceApp()
    app.mainloop()
