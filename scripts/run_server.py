
import os
import sys
from pathlib import Path
import requests


def _find_repo_root(start: Path, marker: str = "backend", max_up: int = 6) -> Path:
    cur = start.resolve()
    for _ in range(max_up):
        if (cur / marker).is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start.resolve().parent.parent


# Ensure repo root is on sys.path before importing local package
PROJECT_ROOT = _find_repo_root(Path(__file__).resolve().parent)
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))


def main():
    from backend.app import create_app
    # Allow overriding the host/port via env for flexibility
    host = os.environ.get('FLASK_RUN_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_RUN_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '1') in ('1', 'true', 'True')

    app = create_app()
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()

# Example usage
url = "http://127.0.0.1:5000/recommendations/answer"
payload = {"question": "What are the best sneakers under $100?"}
print("Posting:", payload)
r = requests.post(url, json=payload, timeout=30)
print("Status:", r.status_code)
try:
    print("JSON:", r.json())
except Exception:
    print("Text:", r.text)
