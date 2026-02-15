from pathlib import Path
import os


def find_project_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / "pyproject.toml").exists():
            return p
    return start.parents[2]


HERE = Path(__file__).resolve()
PROJECT_ROOT = find_project_root(HERE)


DATA_ROOT = Path(os.getenv("BA_RAGMAS_DATA_DIR", PROJECT_ROOT))
DB_DIR = DATA_ROOT / "db"
DOCUMENTS_DIR = DATA_ROOT / "documents"
