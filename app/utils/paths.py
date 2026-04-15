from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DATASET_DIR = DATA_DIR / "dataset"
REPORTS_DIR = BASE_DIR / "reports"
SQL_DIR = BASE_DIR / "sql"
DB_PATH = DATA_DIR / "attendance.db"


def ensure_directories() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    DATASET_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
