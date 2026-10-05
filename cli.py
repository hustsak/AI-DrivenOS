#!/usr/bin/env python3
"""
AI-Driven Intelligent OS — CLI Interface
Run this for a pure terminal experience with LLM natural language understanding.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from agent.llm_agent import llm_interpret
from utils.executor import execute
from utils.logger import get_recent_logs
import datetime

BANNER = """
╔══════════════════════════════════════════════════════╗
║                                                      ║
║       🧠  AI-DRIVEN INTELLIGENT OS PROTOTYPE         ║
║         LLM Natural Language OS Interface            ║
║                                                      ║
╚══════════════════════════════════════════════════════╝

  Type natural language commands or use:
    help          → show all commands
    logs          → show command history
    exit / quit   → exit the assistant

"""

def print_output(result: dict, interpreted: dict):
    """Print a formatted result block."""
    status = result.get("status", "unknown")
    icon = {"success": "✅", "error": "❌", "denied": "🔒", "unknown": "❓"}.get(status, "ℹ️")
    display = result.get("display") or result.get("message") or "(no output)"

    ai_response = interpreted.get("ai_response")
    if ai_response:
        print(f"\033[94m🤖 AI Insight:\033[0m {ai_response}")

    print(f"\n{icon} {result.get('message', '')}")
    print("─" * 60)
    print(display)
    print()


def run_cli():
    """Main CLI loop."""
    print(BANNER)

    while True:
        try:
            raw = input("\033[96m❯ \033[0m").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Goodbye!")
            break

        if not raw:
            continue

        if raw.lower() in ("exit", "quit", "q"):
            print("\n👋 AI OS shutting down. Goodbye!")
            break

        if raw.lower() == "logs":
            logs = get_recent_logs(20)
            if logs:
                print("\n📋 Recent Commands:")
                print("─" * 60)
                for line in logs:
                    print(line.rstrip())
            else:
                print("\n📋 No logs yet.")
            continue

        # ── AI Pipeline ──
        print(f"\033[90m  → Interpreting prompt with LLM...\033[0m", end="\r")

        interpreted = llm_interpret(raw)
        result = execute(interpreted["action"], interpreted.get("params", {}))

        action = interpreted.get("action", "unknown")
        confidence = interpreted.get("confidence", 0)
        via = interpreted.get("via", "rule-based")
        ts = datetime.datetime.now().strftime("%H:%M:%S")

        print(f"\033[90m  [{ts}] Action: {action} | Via: {via} | Confidence: {confidence:.0%}\033[0m")
        print_output(result, interpreted)


if __name__ == "__main__":
    run_cli()

