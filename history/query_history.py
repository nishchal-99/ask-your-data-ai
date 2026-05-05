import json
import os
from datetime import datetime

HISTORY_FILE = "history/history_store.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as file:
        return json.load(file)


def save_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def add_query_to_history(question, sql_query, risk_level):
    history = load_history()

    history_item = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "sql_query": sql_query,
        "risk_level": risk_level,
        "favorite": False,
    }

    history.insert(0, history_item)
    save_history(history)


def toggle_favorite(index):
    history = load_history()

    if 0 <= index < len(history):
        history[index]["favorite"] = not history[index].get("favorite", False)
        save_history(history)


def clear_history():
    save_history([])