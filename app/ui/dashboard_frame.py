from __future__ import annotations

from tkinter import ttk

from app.ui.base_frame import BaseFrame


class DashboardFrame(BaseFrame):
    def __init__(self, parent, app_context) -> None:
        super().__init__(parent, app_context)
        container = ttk.Frame(self)
        container.grid(sticky="nsew")
        for index in range(3):
            container.columnconfigure(index, weight=1)

        self.student_total = self._build_card(container, 0, "Tong sinh vien")
        self.class_total = self._build_card(container, 1, "Tong lop hoc")
        self.attendance_total = self._build_card(container, 2, "Diem danh hom nay")

    def _build_card(self, parent, column: int, title: str) -> ttk.Label:
        card = ttk.LabelFrame(parent, text=title, padding=16)
        card.grid(row=0, column=column, padx=8, sticky="nsew")
        value_widget = ttk.Label(card, text="0", font=("Segoe UI", 18, "bold"))
        value_widget.grid(row=0, column=0, sticky="nsew")
        return value_widget

    def refresh_data(self) -> None:
        self.student_total.config(text=str(len(self.app.student_service.list_students())))
        self.class_total.config(text=str(len(self.app.class_service.list_classes())))
        self.attendance_total.config(text=str(self.app.attendance_service.today_total()))
