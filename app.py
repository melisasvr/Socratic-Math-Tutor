import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from socratic_tutor.ui import run_app


if __name__ == "__main__":
    run_app()