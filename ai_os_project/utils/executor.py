"""
Command Executor — routes AI-parsed actions to OS simulation functions
Also handles logging and system status aggregation.
"""

import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from os_sim.process_manager import list_processes, kill_process, get_cpu_info, open_application
from os_sim.memory_manager import get_memory_usage, optimize_memory
from os_sim.file_manager import get_disk_usage, clean_temp_files, list_files
from agent.interpreter import get_all_commands
from utils.logger import log_command


def execute(action: str, params: dict = None) -> dict:
    """Execute a parsed action and return the result."""
    params = params or {}

    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    result = None

    # ── Route to correct OS function ──────────────────────────────────────────
    if action == "list_processes":
        result = list_processes()

    elif action == "kill_process":
        pid = params.get("pid")
        result = kill_process(pid)

    elif action == "get_memory_usage":
        result = get_memory_usage()

    elif action == "optimize_memory":
        result = optimize_memory()

    elif action == "get_disk_usage":
        result = get_disk_usage()

    elif action == "clean_temp_files":
        result = clean_temp_files()

    elif action == "list_files":
        directory = params.get("directory", ".")
        result = list_files(directory)

    elif action == "get_cpu_info":
        result = get_cpu_info()

    elif action == "system_status":
        result = get_system_status()

    elif action == "open_app":
        app_name = params.get("app_name") or params.get("app") or ""
        result = open_application(app_name)

    elif action == "help":
        result = get_help()

    elif action == "unknown":
        result = {
            "status": "unknown",
            "message": params.get("message", "Command not recognized. Type 'help' for options."),
            "data": None,
            "display": "❓ Command not recognized. Try: 'show processes', 'memory usage', 'clean system'"
        }

    elif action == "need_pid":
        result = {
            "status": "need_input",
            "message": "Please provide a PID to kill (e.g. 'kill process 1234')",
            "data": None,
            "display": "⚠️ Please provide a PID. Example: kill process 1234"
        }

    else:
        result = {
            "status": "error",
            "message": f"Unknown action: {action}",
            "data": None,
            "display": f"❌ Unknown action: {action}"
        }

    # ── Log every command ──────────────────────────────────────────────────────
    log_command(action, result.get("status", "unknown"), timestamp)

    result["timestamp"] = timestamp
    return result


def get_system_status():
    """Aggregate all system metrics into one overview."""
    cpu = get_cpu_info()
    mem = get_memory_usage()
    disk = get_disk_usage()

    cpu_d = cpu.get("data", {})
    mem_d = mem.get("data", {})
    disk_d = disk.get("data", [])
    first_disk = disk_d[0] if disk_d else {}

    lines = [
        "╔══════════════════════════════════════╗",
        "║       SYSTEM STATUS OVERVIEW         ║",
        "╚══════════════════════════════════════╝\n",
        f"🖥️  CPU Usage:    {cpu_d.get('usage_percent', 'N/A')}%",
        f"    Cores:       {cpu_d.get('core_count', 'N/A')}",
        f"    Frequency:   {cpu_d.get('frequency_mhz', 'N/A')} MHz\n",
        f"💾  RAM Used:     {mem_d.get('used_gb', 'N/A')} / {mem_d.get('total_gb', 'N/A')} GB",
        f"    Usage:       {mem_d.get('percent', 'N/A')}%",
        f"    Available:   {mem_d.get('available_gb', 'N/A')} GB\n",
        f"💿  Disk Used:    {first_disk.get('used_gb', 'N/A')} / {first_disk.get('total_gb', 'N/A')} GB",
        f"    Usage:       {first_disk.get('percent', 'N/A')}%",
        f"    Free:        {first_disk.get('free_gb', 'N/A')} GB\n",
    ]

    status_icon = "🟢 Healthy"
    if mem_d.get('percent', 0) > 85 or (cpu_d.get('usage_percent') or 0) > 90:
        status_icon = "🔴 High Load"
    elif mem_d.get('percent', 0) > 70:
        status_icon = "🟡 Moderate"

    lines.append(f"System Health: {status_icon}")

    return {
        "status": "success",
        "message": "System status retrieved",
        "data": {
            "cpu": cpu_d,
            "memory": mem_d,
            "disk": first_disk
        },
        "display": "\n".join(lines)
    }


def get_help():
    """Show all available commands."""
    cmds = get_all_commands()
    lines = [
        "╔══════════════════════════════════════════╗",
        "║     AI OS ASSISTANT — AVAILABLE COMMANDS ║",
        "╚══════════════════════════════════════════╝\n",
    ]
    for c in cmds:
        lines.append(f"  ❯ {c['command']:<30} {c['description']}")

    lines.append("\n💡 Tip: Use natural language! e.g. 'How's my memory?' or 'Clean up my system'")

    return {
        "status": "success",
        "message": "Help displayed",
        "data": cmds,
        "display": "\n".join(lines)
    }
