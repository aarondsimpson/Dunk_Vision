from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAYER_DATA_DIR = ROOT / "player_data"
SESSION_DATA_DIR = ROOT / "session_data"

for directory in (PLAYER_DATA_DIR, SESSION_DATA_DIR):
    directory.mkdir(parents=True, exist_ok=True)