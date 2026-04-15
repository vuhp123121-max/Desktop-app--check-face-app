from __future__ import annotations

from datetime import datetime


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def today_text() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def time_text() -> str:
    return datetime.now().strftime("%H:%M:%S")
