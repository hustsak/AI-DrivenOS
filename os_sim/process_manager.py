"""
Process Manager — simulates OS process management using psutil
"""

import psutil
import datetime


def list_processes(limit=15):
    """List top running processes sorted by CPU usage."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try:
            info = proc.info
            processes.append({
                "pid": info['pid'],
                "name": info['name'] or "unknown",
                "cpu": round(info['cpu_percent'] or 0, 1),
                "memory": round(info['memory_percent'] or 0, 1),
                "status": info['status']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Sort by CPU usage descending
    processes.sort(key=lambda x: x['cpu'], reverse=True)
    top = processes[:limit]

    lines = [f"{'PID':<8} {'NAME':<25} {'CPU%':<8} {'MEM%':<8} {'STATUS'}"]
    lines.append("-" * 65)
    for p in top:
        lines.append(f"{p['pid']:<8} {p['name'][:24]:<25} {p['cpu']:<8} {p['memory']:<8} {p['status']}")

    return {
        "status": "success",
        "message": f"Top {len(top)} processes by CPU usage",
        "data": top,
        "display": "\n".join(lines)
    }


def kill_process(pid):
    """Safely terminate a process by PID (demo mode — won't kill system procs)."""
    PROTECTED_NAMES = {"python", "python3", "bash", "sh", "systemd", "init", "kernel"}

    try:
        pid = int(pid)
        proc = psutil.Process(pid)
        name = proc.name().lower()

        if any(p in name for p in PROTECTED_NAMES):
            return {
                "status": "denied",
                "message": f"❌ Cannot kill protected process '{name}' (PID {pid}) — system safety lock engaged.",
                "data": None
            }

        # Simulate kill (don't actually kill in demo mode)
        return {
            "status": "success",
            "message": f"✅ Process '{proc.name()}' (PID {pid}) terminated successfully.",
            "data": {"pid": pid, "name": proc.name()}
        }

    except psutil.NoSuchProcess:
        return {"status": "error", "message": f"❌ No process found with PID {pid}", "data": None}
    except psutil.AccessDenied:
        return {"status": "error", "message": f"❌ Access denied to kill PID {pid}", "data": None}
    except ValueError:
        return {"status": "error", "message": "❌ Invalid PID — must be a number", "data": None}


def get_cpu_info():
    """Return overall CPU stats."""
    cpu_percent = psutil.cpu_percent(interval=None)
    cpu_count = psutil.cpu_count()
    freq = psutil.cpu_freq()

    return {
        "status": "success",
        "message": "CPU information retrieved",
        "data": {
            "usage_percent": cpu_percent,
            "core_count": cpu_count,
            "frequency_mhz": round(freq.current, 1) if freq else "N/A"
        },
        "display": (
            f"CPU Usage:     {cpu_percent}%\n"
            f"Cores:         {cpu_count}\n"
            f"Frequency:     {round(freq.current, 1) if freq else 'N/A'} MHz"
        )
    }


def open_application(app_name: str) -> dict:
    """Launch an application on the user's operating system with smart path resolution."""
    import subprocess
    import os
    import webbrowser

    app = (app_name or "").lower().strip()
    if not app:
        return {"status": "error", "message": "❌ Please specify an application name to open."}

    appdata = os.environ.get("APPDATA", "")
    localappdata = os.environ.get("LOCALAPPDATA", "")
    prog = os.environ.get("ProgramFiles", "C:\\Program Files")
    prog86 = os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")

    # Candidate paths & commands for popular apps
    candidates = {
        "telegram": [
            os.path.join(appdata, "Telegram Desktop", "Telegram.exe"),
            os.path.join(prog, "Telegram Desktop", "Telegram.exe"),
            os.path.join(prog86, "Telegram Desktop", "Telegram.exe"),
            "telegram:"
        ],
        "chrome": [
            os.path.join(prog, "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(prog86, "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(localappdata, "Google", "Chrome", "Application", "chrome.exe"),
            "chrome"
        ],
        "discord": [
            os.path.join(localappdata, "Discord", "Update.exe"),
            "discord:"
        ],
        "spotify": [
            os.path.join(appdata, "Spotify", "Spotify.exe"),
            "spotify:"
        ],
        "code": ["code"],
        "vscode": ["code"],
        "visual studio code": ["code"],
        "notepad": ["notepad.exe"],
        "calc": ["calc.exe"],
        "calculator": ["calc.exe"],
        "explorer": ["explorer.exe"],
        "file explorer": ["explorer.exe"],
        "exploror": ["explorer.exe"],
        "edge": ["msedge"]
    }

    target_list = candidates.get(app, [app])

    for target in target_list:
        if os.path.isabs(target) and os.path.exists(target):
            try:
                subprocess.Popen([target])
                return {
                    "status": "success",
                    "message": f"Launched '{app_name}'",
                    "data": {"app": app_name, "path": target},
                    "display": f"🚀 Successfully launched '{app_name}' on your PC!"
                }
            except Exception:
                continue
        elif not os.path.isabs(target):
            try:
                subprocess.Popen(f'start "" "{target}"', shell=True)
                return {
                    "status": "success",
                    "message": f"Launched '{app_name}'",
                    "data": {"app": app_name, "target": target},
                    "display": f"🚀 Successfully launched '{app_name}' on your PC!"
                }
            except Exception:
                continue

    # Fallback for Telegram web
    if "telegram" in app:
        webbrowser.open("https://web.telegram.org")
        return {
            "status": "success",
            "message": "Opened Telegram Web in browser",
            "data": {"app": app_name},
            "display": "🌐 Opened Telegram Web in your browser!"
        }

    return {
        "status": "error",
        "message": f"Could not find or launch application '{app_name}'",
        "data": None,
        "display": f"❌ Could not find or launch '{app_name}'. Make sure it is installed on your PC."
    }

