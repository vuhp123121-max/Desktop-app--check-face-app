from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from app.ui.base_frame import BaseFrame


class FaceRegistrationFrame(BaseFrame):
    def __init__(self, parent, app_context) -> None:
        super().__init__(parent, app_context)
        frame = ttk.Frame(self)
        frame.grid(sticky="nsew")
        frame.columnconfigure(0, weight=1)
        ttk.Label(frame, text="Dang ky khuon mat", font=("Segoe UI", 15, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 12))
        self.student_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Chua thuc hien.")
        ttk.Label(frame, text="Chon sinh vien").grid(row=1, column=0, sticky="w")
        self.student_combo = ttk.Combobox(frame, textvariable=self.student_var, state="readonly", width=50)
        self.student_combo.grid(row=2, column=0, sticky="ew", pady=(4, 8))
        ttk.Button(frame, text="Chup 10 anh khuon mat", command=self.capture_faces).grid(row=3, column=0, sticky="w")
        ttk.Label(frame, textvariable=self.status_var, foreground="blue").grid(row=4, column=0, sticky="w", pady=(12, 0))

    def refresh_data(self) -> None:
        students = self.app.student_service.list_students()
        values = [f"{item['id']} - {item['student_code']} - {item['full_name']}" for item in students]
        self.student_combo["values"] = values
        if values and not self.student_var.get():
            self.student_var.set(values[0])

    def capture_faces(self) -> None:
        selected = self.student_var.get().strip()
        if not selected:
            messagebox.showwarning("Khuon mat", "Hay chon sinh vien truoc.")
            return
        student_id = int(selected.split(" - ", 1)[0])
        student = self.app.student_service.get_student(student_id)
        if not student:
            messagebox.showerror("Khuon mat", "Khong tim thay sinh vien.")
            return
        ok, message = self.app.face_service.capture_samples(student_id, student["student_code"])
        self.status_var.set(message)
        if ok:
            messagebox.showinfo("Khuon mat", message)
        else:
            messagebox.showwarning("Khuon mat", message)
