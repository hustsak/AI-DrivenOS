"""
AI Agent — Natural Language Command Interpreter
Supports rule-based intent recognition + optional LLM fallback
"""

import re
from datetime import datetime


# ─── Intent definitions ───────────────────────────────────────────────────────

INTENTS = {
    "list_processes": {
        "keywords": ["process", "processes", "running", "tasks", "task manager", "what's running", "show tasks"],
        "action": "list_processes",
        "description": "List running processes"
    },
    "kill_process": {
        "keywords": ["kill", "terminate", "stop process", "end process", "close process"],
        "action": "kill_process",
        "description": "Kill a process by PID"
    },
    "memory_usage": {
        "keywords": ["memory", "ram", "memory usage", "how much memory", "memory stats"],
        "action": "get_memory_usage",
        "description": "Show memory usage"
    },
    "optimize_memory": {
        "keywords": ["optimize memory", "free memory", "clear memory", "clean memory", "boost memory", "memory boost"],
        "action": "optimize_memory",
        "description": "Optimize memory usage"
    },
    "disk_usage": {
        "keywords": ["disk", "storage", "drive", "space", "disk space", "disk usage", "how much space"],
        "action": "get_disk_usage",
        "description": "Show disk usage"
    },
    "clean_disk": {
        "keywords": ["clean", "clean disk", "clean temp", "delete temp", "clear temp", "clean system",
                     "free up space", "cleanup", "garbage", "junk", "optimize system", "optimize"],
        "action": "clean_temp_files",
        "description": "Clean temporary files"
    },
    "list_files": {
        "keywords": ["files", "list files", "show files", "directory", "folder", "ls", "dir"],
        "action": "list_files",
        "description": "List files in a directory"
    },
    "cpu_info": {
        "keywords": ["cpu", "processor", "cpu usage", "core", "frequency", "cpu info"],
        "action": "get_cpu_info",
        "description": "Show CPU information"
    },
    "system_status": {
        "keywords": ["status", "system status", "overview", "dashboard", "health", "all stats",
                     "system info", "how is my system", "system check"],
        "action": "system_status",
        "description": "Full system status overview"
    },
    "open_app": {
        "keywords": ["open", "launch", "start app", "run app"],
        "action": "open_app",
        "description": "Open or launch an application"
    },
    "help": {
        "keywords": ["help", "what can you do", "commands", "options", "menu", "?"],
        "action": "help",
        "description": "Show available commands"
    }
}


# ─── Intent Parser ────────────────────────────────────────────────────────────

def interpret(user_input: str) -> dict:
    """
    Parse natural language input and return the matched action + any extracted params.
    Returns: { action, confidence, params, raw_input }
    """
    raw = user_input.strip()
    text = raw.lower()

    # Extract PID if present (for kill commands)
    pid_match = re.search(r'\b(\d{3,6})\b', text)
    extracted_pid = pid_match.group(1) if pid_match else None

    # Check open/launch explicitly
    open_match = re.search(r'\b(?:open|launch|start|run)\s+([\w\s-]+)', text)
    if open_match and not any(kw in text for kw in ["process", "task", "temp", "file", "memory", "disk", "cpu", "system"]):
        app_name = open_match.group(1).strip()
        return {
            "action": "open_app",
            "confidence": 0.9,
            "params": {"app_name": app_name},
            "raw_input": raw,
            "description": f"Open {app_name}"
        }

    # Check kill/terminate explicitly first (high priority)
    kill_triggers = ["kill", "terminate", "stop process", "end process", "close process"]
    if any(re.search(r'\b' + re.escape(kt) + r'\b', text) for kt in kill_triggers):
        kill_intent = INTENTS["kill_process"]
        pid_match2 = re.search(r'\b(\d{3,6})\b', text)
        p = pid_match2.group(1) if pid_match2 else None
        return {
            "action": kill_intent["action"],
            "confidence": 0.9,
            "params": {"pid": p} if p else {},
            "raw_input": raw,
            "description": kill_intent["description"],
            "need_pid": p is None
        }

    best_match = None
    best_score = 0

    for intent_name, intent_data in INTENTS.items():
        score = 0
        for kw in intent_data["keywords"]:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, text):
                score = max(score, len(kw.split()))

        if score > best_score:
            best_score = score
            best_match = intent_data

    if best_match is None:
        return {
            "action": "unknown",
            "confidence": 0,
            "params": {},
            "raw_input": raw,
            "message": "I don't understand that command. Type 'help' to see what I can do."
        }

    params = {}
    if best_match["action"] == "kill_process" and extracted_pid:
        params["pid"] = extracted_pid
    elif best_match["action"] == "kill_process" and not extracted_pid:
        return {
            "action": "need_pid",
            "confidence": 0.5,
            "params": {},
            "raw_input": raw,
            "message": "⚠️ Which process do you want to kill? Please provide a PID (e.g. 'kill process 1234')"
        }

    # Extract directory for list_files
    if best_match["action"] == "list_files":
        dir_match = re.search(r'(?:in|of|at|from)\s+([\w/\\.~-]+)', text)
        params["directory"] = dir_match.group(1) if dir_match else "."

    confidence = min(1.0, best_score / 3)

    return {
        "action": best_match["action"],
        "confidence": round(confidence, 2),
        "params": params,
        "raw_input": raw,
        "description": best_match["description"]
    }


# ─── Command Registry ─────────────────────────────────────────────────────────

def get_all_commands():
    """Return list of all available commands for help display."""
    return [
        {"command": "show processes", "description": "List all running processes"},
        {"command": "kill process <PID>", "description": "Terminate a process by PID"},
        {"command": "memory usage", "description": "Show RAM usage statistics"},
        {"command": "optimize memory", "description": "Free up memory (simulated)"},
        {"command": "disk usage", "description": "Show disk space on all drives"},
        {"command": "clean system", "description": "Clean temporary files"},
        {"command": "list files", "description": "List files in current directory"},
        {"command": "cpu info", "description": "Show CPU usage and stats"},
        {"command": "system status", "description": "Full system overview dashboard"},
        {"command": "help", "description": "Show this help menu"},
    ]
