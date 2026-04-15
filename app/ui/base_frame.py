from __future__ import annotations

from tkinter import ttk


class BaseFrame(ttk.Frame):
    def __init__(self, parent, app_context) -> None:
        super().__init__(parent, padding=12)
        self.app = app_context
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def refresh_data(self) -> None:
        return None
