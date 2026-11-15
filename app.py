"""Start the demo web page:  python app.py   (then open the printed local URL)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from demo import build_app  # noqa: E402

if __name__ == "__main__":
    build_app().launch()
