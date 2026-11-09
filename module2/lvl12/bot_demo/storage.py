import json
from pathlib import Path

USERS_FILE = Path("data/users.json")


def load_users() -> dict:
    if not USERS_FILE.exists():
        return {}
    return json.loads(USERS_FILE.read_text(encoding="utf-8"))


def save_user(user_id: int, name: str) -> int:
    """Записати візит користувача і повернути загальну кількість його візитів."""
    users = load_users()
    user = users.setdefault(str(user_id), {"name": name, "visits": 0})
    user["visits"] += 1

    USERS_FILE.parent.mkdir(exist_ok=True)
    USERS_FILE.write_text(json.dumps(users, ensure_ascii=False, indent=2), encoding="utf-8")
    return user["visits"]
