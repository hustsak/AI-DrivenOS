"""
Autonomous Monitor — runs in background, watches system health,
proactively alerts and optionally auto-acts when thresholds are breached.
This gives the project "intelligence" beyond just responding to commands.
"""

import threading
import time
import psutil
from datetime import datetime

# Thresholds
THRESHOLDS = {
    "cpu_percent":    80.0,   # % — alert if CPU stays above this
    "memory_percent": 80.0,   # % — alert + optionally auto-optimize
    "disk_percent":   90.0,   # % — alert
}

# Cooldown: don't fire the same alert twice within this many seconds
ALERT_COOLDOWN = 60

_alert_history = {}   # { alert_key: last_triggered_timestamp }
_alert_log     = []   # list of alert dicts shown in UI
_suggestions   = []   # list of current suggestion strings
_lock          = threading.Lock()
_monitor_thread = None
_running        = False


def _should_alert(key: str) -> bool:
    now = time.time()
    last = _alert_history.get(key, 0)
    if now - last > ALERT_COOLDOWN:
        _alert_history[key] = now
        return True
    return False


def _check_and_act():
    """One monitoring cycle — collect stats and generate alerts/suggestions."""
    global _suggestions

    alerts   = []
    new_sugg = []

    try:
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        ts = datetime.now().strftime("%H:%M:%S")

        # ── CPU ──────────────────────────────────────────────────────────────
        if cpu > THRESHOLDS["cpu_percent"]:
            if _should_alert("cpu_high"):
                alert = {
                    "type":    "warning",
                    "icon":    "🔥",
                    "title":   "High CPU Usage",
                    "message": f"CPU at {cpu:.0f}% — consider closing heavy processes.",
                    "action":  "list_processes",
                    "time":    ts,
                }
                alerts.append(alert)
                new_sugg.append(f"⚡ CPU is {cpu:.0f}% — want me to show top processes?")
        else:
            new_sugg.append(f"CPU: {cpu:.0f}% — normal")

        # ── Memory ───────────────────────────────────────────────────────────
        mem_pct = mem.percent
        if mem_pct > THRESHOLDS["memory_percent"]:
            if _should_alert("memory_high"):
                alert = {
                    "type":    "danger",
                    "icon":    "💾",
                    "title":   "Memory Critical",
                    "message": f"RAM at {mem_pct:.0f}% — auto-optimization recommended.",
                    "action":  "optimize_memory",
                    "time":    ts,
                }
                alerts.append(alert)
                new_sugg.append(f"💾 RAM is {mem_pct:.0f}% — I can optimize memory for you.")
        else:
            new_sugg.append(f"RAM: {mem_pct:.0f}% — healthy")

        # ── Disk ─────────────────────────────────────────────────────────────
        disk_pct = disk.percent
        if disk_pct > THRESHOLDS["disk_percent"]:
            if _should_alert("disk_high"):
                alert = {
                    "type":    "warning",
                    "icon":    "💿",
                    "title":   "Disk Almost Full",
                    "message": f"Disk at {disk_pct:.0f}% — consider cleaning temp files.",
                    "action":  "clean_temp_files",
                    "time":    ts,
                }
                alerts.append(alert)
                new_sugg.append(f"💿 Disk at {disk_pct:.0f}% — want me to clean temp files?")
        else:
            new_sugg.append(f"Disk: {disk_pct:.0f}% — OK")

    except Exception:
        pass

    with _lock:
        _alert_log.extend(alerts)
        if len(_alert_log) > 50:
            _alert_log[:] = _alert_log[-50:]
        _suggestions = new_sugg

    return alerts


def _monitor_loop(interval: int = 15):
    global _running
    while _running:
        _check_and_act()
        time.sleep(interval)


def start_monitor(interval: int = 15):
    """Start the background monitoring thread."""
    global _monitor_thread, _running
    if _monitor_thread and _monitor_thread.is_alive():
        return
    _running = True
    _monitor_thread = threading.Thread(target=_monitor_loop, args=(interval,), daemon=True)
    _monitor_thread.start()


def stop_monitor():
    global _running
    _running = False


def get_alerts(since_index: int = 0) -> list:
    """Return alerts newer than since_index."""
    with _lock:
        return _alert_log[since_index:]


def get_all_alerts() -> list:
    with _lock:
        return list(_alert_log)


def get_suggestions() -> list:
    """Return current smart suggestions based on last check."""
    with _lock:
        return list(_suggestions)


def get_alert_count() -> int:
    with _lock:
        return len(_alert_log)


def run_once() -> list:
    """Run a single check immediately and return any alerts fired."""
    return _check_and_act()


def get_health_summary() -> dict:
    """Return a snapshot health dict."""
    try:
        cpu  = psutil.cpu_percent(interval=0.5)
        mem  = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        def status(pct, warn=70, crit=85):
            if pct >= crit: return "critical"
            if pct >= warn: return "warning"
            return "healthy"

        return {
            "cpu":    {"value": round(cpu, 1),       "status": status(cpu)},
            "memory": {"value": round(mem.percent,1),"status": status(mem.percent)},
            "disk":   {"value": round(disk.percent,1),"status": status(disk.percent)},
            "overall": "critical" if any(
                v["status"] == "critical"
                for v in [{"status": status(cpu)}, {"status": status(mem.percent)}, {"status": status(disk.percent)}]
            ) else "warning" if any(
                v["status"] == "warning"
                for v in [{"status": status(cpu)}, {"status": status(mem.percent)}, {"status": status(disk.percent)}]
            ) else "healthy"
        }
    except Exception:
        return {"cpu": {}, "memory": {}, "disk": {}, "overall": "unknown"}
