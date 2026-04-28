
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "filter_config.json")


def load_filter_classes():
    if not os.path.exists(CONFIG_PATH):
        return []  # default = no filtering (or everything allowed depending on your logic)

    try:
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
            classes = data.get("classes", [])
            if not isinstance(classes, list):
                return []
            return [str(name).strip().lower() for name in classes if str(name).strip()]
    except Exception:
        return []
