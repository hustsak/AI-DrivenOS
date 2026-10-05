"""
AI-Driven Intelligent OS — Flask Web Application (v2)
Upgraded with: LLM interpreter, autonomous monitor, learning engine
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, render_template, request, jsonify
from agent.llm_agent import llm_interpret
from agent.monitor import start_monitor, get_alerts, get_suggestions, get_health_summary, get_alert_count
from agent.learner import record, get_recommendations, get_frequent_actions, get_session_stats
from utils.executor import execute
from utils.logger import get_recent_logs
import datetime

app = Flask(__name__)
app.secret_key = "ai_os_secret_2024"

start_monitor(interval=15)

_last_alert_index = 0


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/command", methods=["POST"])
def handle_command():
    data = request.get_json()
    user_input = (data or {}).get("command", "").strip()
    api_key    = (data or {}).get("api_key", "").strip()

    if not user_input:
        return jsonify({"error": "No command provided"}), 400

    interpreted = llm_interpret(user_input, api_key or None)

    if interpreted.get("action") == "need_pid":
        return jsonify({
            "user_input": user_input,
            "interpreted_action": "need_pid",
            "status": "need_input",
            "message": "Please provide a PID (e.g. 'kill process 1234')",
            "display": "Please provide a PID. Example: kill process 1234",
            "via": interpreted.get("via", "rule-based"),
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
        })

    result = execute(interpreted.get("action", "unknown"), interpreted.get("params", {}))
    record(interpreted.get("action", "unknown"), user_input, result.get("status", "unknown"))

    ts = datetime.datetime.now().strftime("%H:%M:%S")
    return jsonify({
        "user_input":         user_input,
        "interpreted_action": interpreted.get("action"),
        "action_description": interpreted.get("description", ""),
        "ai_response":        interpreted.get("ai_response", ""),
        "confidence":         interpreted.get("confidence", 0),
        "via":                interpreted.get("via", "rule-based"),
        "status":             result.get("status"),
        "message":            result.get("message"),
        "display":            result.get("display", ""),
        "data":               result.get("data"),
        "timestamp":          ts
    })


@app.route("/api/alerts", methods=["GET"])
def get_new_alerts():
    global _last_alert_index
    alerts = get_alerts(_last_alert_index)
    _last_alert_index = get_alert_count()
    return jsonify({"alerts": alerts, "suggestions": get_suggestions()})


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify(get_health_summary())


@app.route("/api/recommendations", methods=["GET"])
def recommendations():
    return jsonify({
        "recommendations": get_recommendations(),
        "frequent":        get_frequent_actions(3),
        "stats":           get_session_stats()
    })


@app.route("/api/logs", methods=["GET"])
def get_logs():
    return jsonify({"logs": get_recent_logs(30)})


@app.route("/api/status", methods=["GET"])
def quick_status():
    from utils.executor import get_system_status
    return jsonify(get_system_status())


if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  AI-Driven Intelligent OS")
    print("  Autonomous monitor: ON (checks every 15s)")
    print("  Learning engine:    ON")
    print("  LLM agent:          ON (set ANTHROPIC_API_KEY)")
    print("  Open: http://localhost:5000")
    print("=" * 55 + "\n")
    app.run(debug=True, port=5000)
