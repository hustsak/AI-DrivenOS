"""
Logger — records all commands and results to log.txt
"""

import os
import datetime

LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "log.txt")


def log_command(action: str, status: str, timestamp: str = None):
    """Append a command log entry."""
    if timestamp is None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = f"[{timestamp}] ACTION={action:<25} STATUS={status}\n"

    try:
        with open(LOG_FILE, "a") as f:
            f.write(entry)
    except Exception:
        pass  # Silent fail — logging shouldn't crash the app


def get_recent_logs(limit=20):
    """Return the last N log entries."""
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
        return lines[-limit:]
    except FileNotFoundError:
        return []
