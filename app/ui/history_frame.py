from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from app.ui.base_frame import BaseFrame
from app.utils.paths import REPORTS_DIR


class HistoryFrame(BaseFrame):
    def __init__(self, parent, app_context) -> None:
        super().__init__(parent, app_context)
        root = ttk.Frame(self)
        root.grid(sticky="nsew")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        filter_bar = ttk.Frame(root)
        filter_bar.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        for index in range(7):
            filter_bar.columnconfigure(index, weight=1 if index in (0, 1, 2) else 0)
        self.date_var = tk.StringVar()
        self.class_var = tk.StringVar()
        self.student_var = tk.StringVar()
        ttk.Entry(filter_bar, textvariable=self.date_var).grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ttk.Entry(filter_bar, textvariable=self.class_var).grid(row=0, column=1, sticky="ew", padx=(0, 8))
        ttk.Entry(filter_bar, textvariable=self.student_var).grid(row=0, column=2, sticky="ew", padx=(0, 8))
        ttk.Button(filter_bar, text="Loc", command=self.refresh_data).grid(row=0, column=3, padx=(0, 8))
        ttk.Button(filter_bar, text="Xuat CSV", command=self.export_csv).grid(row=0, column=4)
        columns = ("student_code", "full_name", "class_code", "attendance_date", "check_in_time", "status", "note")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=18)
        headings = {"student_code": "Ma SV", "full_name": "Ho ten", "class_code": "Lop", "attendance_date": "Ngay", "check_in_time": "Gio vao", "status": "Trang thai", "note": "Ghi chu"}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=120, anchor="center")
        self.tree.grid(row=1, column=0, sticky="nsew")

    def _current_rows(self) -> list[dict]:
        return self.app.attendance_service.list_attendance(self.date_var.get(), self.class_var.get(), self.student_var.get())

    def refresh_data(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in self._current_rows():
            self.tree.insert("", "end", values=(row["student_code"], row["full_name"], row["class_code"], row["attendance_date"], row["check_in_time"], row["status"], row["note"]))

    def export_csv(self) -> None:
        rows = self._current_rows()
        if not rows:
            messagebox.showwarning("Bao cao", "Khong co du lieu de xuat.")
            return
        output = REPORTS_DIR / "attendance_report.csv"
        self.app.attendance_service.export_csv(rows, Path(output))
        messagebox.showinfo("Bao cao", f"Da xuat bao cao tai:\n{output}")
