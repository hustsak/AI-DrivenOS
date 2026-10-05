"""
Learning Engine — tracks command frequency, learns user habits,
and proactively recommends the most common actions.
This adds "adaptive intelligence" to the OS assistant.
"""

import json
import os
from collections import Counter
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "history.json")

_history = []   # list of { action, input, time, status }


def _load():
    global _history
    try:
        with open(HISTORY_FILE, "r") as f:
            _history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        _history = []


def _save():
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(_history[-200:], f, indent=2)
    except Exception:
        pass


def record(action: str, raw_input: str, status: str = "success"):
    """Record a command execution for learning."""
    _load()
    _history.append({
        "action":    action,
        "input":     raw_input,
        "status":    status,
        "time":      datetime.now().isoformat()
    })
    _save()


def get_frequent_actions(top_n: int = 3) -> list:
    """Return the top N most frequently used actions."""
    _load()
    if not _history:
        return []
    counts = Counter(e["action"] for e in _history if e.get("status") == "success")
    ACTION_LABELS = {
        "list_processes":  "Show processes",
        "get_memory_usage":"Memory usage",
        "optimize_memory": "Optimize memory",
        "get_cpu_info":    "CPU info",
        "get_disk_usage":  "Disk usage",
        "clean_temp_files":"Clean temp files",
        "system_status":   "System status",
        "list_files":      "List files",
        "help":            "Help",
    }
    return [
        {"action": a, "label": ACTION_LABELS.get(a, a), "count": c}
        for a, c in counts.most_common(top_n)
    ]


def get_recommendations() -> list:
    """Smart recommendations based on usage patterns."""
    _load()
    if len(_history) < 3:
        return ["Run 'system status' to get started", "Try 'optimize memory' if things feel slow"]

    freq = get_frequent_actions(3)
    recs = []
    for f in freq:
        recs.append(f"You often run '{f['label']}' — want to run it now?")

    # Time-based recommendation
    hour = datetime.now().hour
    if 8 <= hour < 10:
        recs.append("Morning tip: run 'system status' to start your day right")
    elif 17 <= hour < 20:
        recs.append("End of day: consider running 'clean temp files'")

    return recs[:3]


def get_session_stats() -> dict:
    """Stats for current session."""
    _load()
    if not _history:
        return {"total": 0, "success": 0, "top_action": "none"}
    total   = len(_history)
    success = sum(1 for e in _history if e.get("status") == "success")
    top     = get_frequent_actions(1)
    return {
        "total":      total,
        "success":    success,
        "top_action": top[0]["label"] if top else "none"
    }
