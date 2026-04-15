from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk


class LoginFrame(ttk.Frame):
    def __init__(self, parent, app_context) -> None:
        super().__init__(parent, padding=24)
        self.app = app_context
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        wrapper = ttk.Frame(self, padding=24)
        wrapper.grid(row=0, column=0, sticky="nsew")
        wrapper.columnconfigure(1, weight=1)

        ttk.Label(wrapper, text="Dang nhap he thong", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 16))
        ttk.Label(wrapper, text="Ten dang nhap").grid(row=1, column=0, sticky="w", pady=6)
        self.username_var = tk.StringVar(value="admin")
        ttk.Entry(wrapper, textvariable=self.username_var, width=30).grid(row=1, column=1, sticky="ew", pady=6)
        ttk.Label(wrapper, text="Mat khau").grid(row=2, column=0, sticky="w", pady=6)
        self.password_var = tk.StringVar(value="admin123")
        ttk.Entry(wrapper, textvariable=self.password_var, width=30, show="*").grid(row=2, column=1, sticky="ew", pady=6)
        ttk.Button(wrapper, text="Dang nhap", command=self.handle_login).grid(row=3, column=0, columnspan=2, pady=(16, 0))

    def handle_login(self) -> None:
        ok = self.app.auth_service.login(self.username_var.get(), self.password_var.get())
        if not ok:
            messagebox.showerror("Dang nhap", "Sai ten dang nhap hoac mat khau.")
            return
        self.app.show_main_layout()
