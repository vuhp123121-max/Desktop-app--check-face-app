from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from app.ui.base_frame import BaseFrame


class AttendanceFrame(BaseFrame):
    def __init__(self, parent, app_context) -> None:
        super().__init__(parent, app_context)
        root = ttk.Frame(self)
        root.grid(sticky="nsew")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(2, weight=1)
        ttk.Label(root, text="Diem danh bang khuon mat", font=("Segoe UI", 15, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 12))
        self.message_var = tk.StringVar(value="San sang diem danh.")
        ttk.Button(root, text="Mo webcam va diem danh", command=self.start_attendance).grid(row=1, column=0, sticky="w")
        ttk.Label(root, textvariable=self.message_var, foreground="blue").grid(row=1, column=0, sticky="e")
        columns = ("student_code", "full_name", "class_code", "attendance_date", "check_in_time", "status")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=16)
        names = {"student_code": "Ma SV", "full_name": "Ho ten", "class_code": "Lop", "attendance_date": "Ngay", "check_in_time": "Gio vao", "status": "Trang thai"}
        for col in columns:
            self.tree.heading(col, text=names[col])
            self.tree.column(col, width=120, anchor="center")
        self.tree.grid(row=2, column=0, sticky="nsew", pady=(12, 0))

    def refresh_data(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows = self.app.attendance_service.list_attendance()
        for row in rows[:20]:
            self.tree.insert("", "end", values=(row["student_code"], row["full_name"], row["class_code"], row["attendance_date"], row["check_in_time"], row["status"]))

    def start_attendance(self) -> None:
        ok, message = self.app.face_service.recognize_and_mark(self.app.attendance_service)
        self.message_var.set(message)
        if ok:
            messagebox.showinfo("Diem danh", message)
        else:
            messagebox.showwarning("Diem danh", message)
        self.refresh_data()
        self.app.refresh_dashboard()
