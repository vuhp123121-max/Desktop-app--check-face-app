from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from app.ui.base_frame import BaseFrame


class StudentsFrame(BaseFrame):
    def __init__(self, parent, app_context) -> None:
        super().__init__(parent, app_context)
        self.selected_student_id: int | None = None
        root = ttk.Frame(self)
        root.grid(sticky="nsew")
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)
        self._build_form(root)
        self._build_table(root)
        self.refresh_data()

    def _build_form(self, parent) -> None:
        form = ttk.LabelFrame(parent, text="Thong tin sinh vien", padding=12)
        form.grid(row=0, column=0, sticky="nsw", padx=(0, 12))
        self.student_code_var = tk.StringVar()
        self.full_name_var = tk.StringVar()
        self.date_of_birth_var = tk.StringVar()
        self.gender_var = tk.StringVar(value="Nam")
        self.keyword_var = tk.StringVar()
        self.class_var = tk.StringVar()
        ttk.Label(form, text="Ma sinh vien").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(form, textvariable=self.student_code_var, width=28).grid(row=1, column=0, sticky="ew")
        ttk.Label(form, text="Ho ten").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Entry(form, textvariable=self.full_name_var, width=28).grid(row=3, column=0, sticky="ew")
        ttk.Label(form, text="Lop").grid(row=4, column=0, sticky="w", pady=4)
        self.class_combo = ttk.Combobox(form, textvariable=self.class_var, state="readonly", width=26)
        self.class_combo.grid(row=5, column=0, sticky="ew")
        ttk.Label(form, text="Ngay sinh (YYYY-MM-DD)").grid(row=6, column=0, sticky="w", pady=4)
        ttk.Entry(form, textvariable=self.date_of_birth_var, width=28).grid(row=7, column=0, sticky="ew")
        ttk.Label(form, text="Gioi tinh").grid(row=8, column=0, sticky="w", pady=4)
        ttk.Combobox(form, textvariable=self.gender_var, values=["Nam", "Nu", "Khac"], state="readonly", width=26).grid(row=9, column=0, sticky="ew")
        ttk.Button(form, text="Them", command=self.create_student).grid(row=10, column=0, sticky="ew", pady=(10, 4))
        ttk.Button(form, text="Cap nhat", command=self.update_student).grid(row=11, column=0, sticky="ew", pady=4)
        ttk.Button(form, text="Xoa", command=self.delete_student).grid(row=12, column=0, sticky="ew", pady=4)
        ttk.Button(form, text="Lam moi", command=self.clear_form).grid(row=13, column=0, sticky="ew", pady=4)

    def _build_table(self, parent) -> None:
        panel = ttk.Frame(parent)
        panel.grid(row=0, column=1, sticky="nsew")
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(1, weight=1)
        search_bar = ttk.Frame(panel)
        search_bar.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        search_bar.columnconfigure(0, weight=1)
        ttk.Entry(search_bar, textvariable=self.keyword_var).grid(row=0, column=0, sticky="ew")
        ttk.Button(search_bar, text="Tim", command=self.refresh_data).grid(row=0, column=1, padx=(8, 0))
        columns = ("student_code", "full_name", "class_code", "date_of_birth", "gender")
        self.tree = ttk.Treeview(panel, columns=columns, show="headings", height=16)
        headings = {"student_code": "Ma SV", "full_name": "Ho ten", "class_code": "Lop", "date_of_birth": "Ngay sinh", "gender": "Gioi tinh"}
        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(column, width=120, anchor="center")
        self.tree.grid(row=1, column=0, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self.on_select_student)
        scrollbar = ttk.Scrollbar(panel, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns")

    def refresh_data(self) -> None:
        classes = self.app.class_service.list_classes()
        class_display = [f"{item['id']} - {item['class_code']}" for item in classes]
        self.class_combo["values"] = class_display
        if class_display and not self.class_var.get():
            self.class_var.set(class_display[0])
        for item in self.tree.get_children():
            self.tree.delete(item)
        students = self.app.student_service.list_students(self.keyword_var.get())
        for student in students:
            self.tree.insert("", "end", iid=str(student["id"]), values=(student["student_code"], student["full_name"], student.get("class_code", ""), student.get("date_of_birth", ""), student.get("gender", "")))

    def _selected_class_id(self) -> int | None:
        selected = self.class_var.get().strip()
        if not selected:
            return None
        return int(selected.split(" - ", 1)[0])

    def create_student(self) -> None:
        if not self.student_code_var.get().strip() or not self.full_name_var.get().strip():
            messagebox.showwarning("Sinh vien", "Vui long nhap ma SV va ho ten.")
            return
        try:
            self.app.student_service.create_student(self.student_code_var.get(), self.full_name_var.get(), self._selected_class_id(), self.date_of_birth_var.get(), self.gender_var.get())
            self.refresh_data()
            self.clear_form()
            self.app.refresh_dashboard()
        except Exception as error:
            messagebox.showerror("Sinh vien", str(error))

    def update_student(self) -> None:
        if self.selected_student_id is None:
            messagebox.showwarning("Sinh vien", "Hay chon sinh vien can cap nhat.")
            return
        try:
            self.app.student_service.update_student(self.selected_student_id, self.student_code_var.get(), self.full_name_var.get(), self._selected_class_id(), self.date_of_birth_var.get(), self.gender_var.get())
            self.refresh_data()
            self.app.refresh_dashboard()
        except Exception as error:
            messagebox.showerror("Sinh vien", str(error))

    def delete_student(self) -> None:
        if self.selected_student_id is None:
            messagebox.showwarning("Sinh vien", "Hay chon sinh vien can xoa.")
            return
        if not messagebox.askyesno("Xoa", "Ban chac chan muon xoa sinh vien nay?"):
            return
        self.app.student_service.delete_student(self.selected_student_id)
        self.refresh_data()
        self.clear_form()
        self.app.refresh_dashboard()

    def clear_form(self) -> None:
        self.selected_student_id = None
        self.student_code_var.set("")
        self.full_name_var.set("")
        self.date_of_birth_var.set("")
        self.gender_var.set("Nam")

    def on_select_student(self, _event=None) -> None:
        selected = self.tree.selection()
        if not selected:
            return
        student_id = int(selected[0])
        student = self.app.student_service.get_student(student_id)
        if not student:
            return
        self.selected_student_id = student_id
        self.student_code_var.set(student["student_code"])
        self.full_name_var.set(student["full_name"])
        self.date_of_birth_var.set(student.get("date_of_birth", "") or "")
        self.gender_var.set(student.get("gender", "") or "Nam")
        if student.get("class_id") and student.get("class_code"):
            self.class_var.set(f"{student['class_id']} - {student['class_code']}")
