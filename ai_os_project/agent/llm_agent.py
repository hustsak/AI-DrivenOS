"""
LLM Agent — Multi-Provider Natural Language Prompt Interpreter
Supports Google Gemini, OpenAI, Anthropic Claude, and Local Ollama.
Falls back seamlessly to the rule-based interpreter if LLM is unavailable.
"""

import json
import os
import re
import requests
from agent.interpreter import interpret as rule_based_interpret

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

SYSTEM_PROMPT = """You are an AI-driven Operating System assistant.
Your task is to interpret natural language user prompts and map them into a single OS action.

Available OS actions:
- list_processes   : List running processes (e.g. "what's running", "show task manager", "top cpu processes")
- kill_process     : Kill/terminate a process by PID (e.g. "kill process 1234", "close PID 4589", "stop process 99")
- get_memory_usage : Show RAM statistics (e.g. "how much memory is free", "ram usage", "am I out of memory")
- optimize_memory  : Free up memory (e.g. "clear ram", "optimize memory", "free memory", "speed up ram")
- get_disk_usage   : Show disk usage (e.g. "storage left", "disk space", "how full is my drive")
- clean_temp_files : Clean temporary files (e.g. "clean my system", "delete temp files", "free up disk space")
- list_files       : List files in directory (e.g. "list files", "show folder contents")
- get_cpu_info     : Show CPU information (e.g. "cpu usage", "processor stats", "how hot is my CPU")
- open_app         : Open or launch an application (e.g. "open telegram", "launch chrome", "start notepad") -> extract app name into params.app_name
- system_status    : Full system status overview (e.g. "my pc feels slow", "system check", "overall status")
- help             : Show help menu (e.g. "what can you do", "commands list", "help me")

Instructions:
1. Interpret the user's intent even if written casually, vaguely, or in non-English phrasing.
2. If the user wants to open or launch an application, set action to "open_app" and put the app name in params.app_name (e.g. {"app_name": "telegram"}).
3. If the user wants to terminate a process, extract the numeric PID into params.pid if present. If no PID is given for kill, set action to "need_pid".
3. Return ONLY a valid JSON object (no markdown, no wrapped text):
{
  "action": "<action_name>",
  "params": {},
  "confidence": 0.95,
  "description": "Short summary of action",
  "ai_response": "Friendly conversational summary or insight for the user"
}
"""


def detect_provider(api_key: str = None) -> tuple:
    """
    Detect LLM provider and effective key based on input or environment variables.
    Returns: (provider_name, effective_api_key)
    """
    key = (api_key or "").strip()

    # Check manual key signature first
    if key.startswith("AIzaSy"):
        return ("gemini", key)
    elif key.startswith("sk-ant-"):
        return ("anthropic", key)
    elif key.startswith("sk-"):
        return ("openai", key)
    elif key.lower() == "ollama":
        return ("ollama", "")

    # Check environment provider override
    env_provider = os.environ.get("LLM_PROVIDER", "").lower().strip()

    if key:
        # User passed a key without known prefix — default to env_provider or gemini/openai
        if env_provider:
            return (env_provider, key)
        return ("gemini" if "gemini" in key.lower() else "openai", key)

    # Check environment variables
    if env_provider:
        if env_provider == "gemini":
            return ("gemini", os.environ.get("GEMINI_API_KEY", ""))
        elif env_provider == "openai":
            return ("openai", os.environ.get("OPENAI_API_KEY", ""))
        elif env_provider == "anthropic":
            return ("anthropic", os.environ.get("ANTHROPIC_API_KEY", ""))
        elif env_provider == "ollama":
            return ("ollama", "")

    if os.environ.get("GEMINI_API_KEY"):
        return ("gemini", os.environ.get("GEMINI_API_KEY", ""))
    if os.environ.get("OPENAI_API_KEY"):
        return ("openai", os.environ.get("OPENAI_API_KEY", ""))
    if os.environ.get("ANTHROPIC_API_KEY"):
        return ("anthropic", os.environ.get("ANTHROPIC_API_KEY", ""))

    # Auto-detect local Ollama instance if available
    try:
        ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        r = requests.get(f"{ollama_host.rstrip('/')}/api/tags", timeout=0.5)
        if r.status_code == 200:
            return ("ollama", "")
    except Exception:
        pass

    return (None, None)


def call_gemini(user_input: str, api_key: str) -> dict:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "parts": [
                {"text": f"{SYSTEM_PROMPT}\n\nUser command: {user_input}"}
            ]
        }],
        "generationConfig": {
            "response_mime_type": "application/json"
        }
    }
    resp = requests.post(url, json=payload, timeout=8)
    resp.raise_for_status()
    data = resp.json()
    raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
    parsed = json.loads(raw_text)
    parsed["via"] = "llm (gemini)"
    return parsed


def call_openai(user_input: str, api_key: str) -> dict:
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    url = f"{base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=8)
    resp.raise_for_status()
    data = resp.json()
    raw_text = data["choices"][0]["message"]["content"]
    parsed = json.loads(raw_text)
    parsed["via"] = "llm (openai)"
    return parsed


def call_anthropic(user_input: str, api_key: str) -> dict:
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    payload = {
        "model": os.environ.get("ANTHROPIC_MODEL", "claude-3-5-haiku-20241022"),
        "max_tokens": 300,
        "system": SYSTEM_PROMPT,
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=8)
    resp.raise_for_status()
    data = resp.json()
    raw_text = data["content"][0]["text"].strip()
    raw_text = re.sub(r"```json|```", "", raw_text).strip()
    parsed = json.loads(raw_text)
    parsed["via"] = "llm (claude)"
    return parsed


_session = requests.Session()
_cached_ollama_model = None


def get_ollama_default_model(host: str) -> str:
    """Fetch the first available model installed in Ollama with in-memory caching."""
    global _cached_ollama_model
    if _cached_ollama_model:
        return _cached_ollama_model

    env_model = os.environ.get("OLLAMA_MODEL")
    if env_model:
        _cached_ollama_model = env_model
        return env_model

    try:
        r = _session.get(f"{host.rstrip('/')}/api/tags", timeout=1.5)
        if r.status_code == 200:
            models = r.json().get("models", [])
            if models:
                _cached_ollama_model = models[0].get("name", "qwen2.5-coder:7b")
                return _cached_ollama_model
    except Exception:
        pass

    _cached_ollama_model = "qwen2.5-coder:7b"
    return _cached_ollama_model


def call_ollama(user_input: str) -> dict:
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    model = get_ollama_default_model(host)
    url = f"{host.rstrip('/')}/api/generate"
    payload = {
        "model": model,
        "prompt": f"{SYSTEM_PROMPT}\n\nUser command: {user_input}",
        "stream": False,
        "format": "json",
        "options": {
            "num_predict": 120,
            "temperature": 0.1
        }
    }
    resp = _session.post(url, json=payload, timeout=6)
    resp.raise_for_status()
    data = resp.json()
    raw_text = data["response"].strip()
    raw_text = re.sub(r"```json|```", "", raw_text).strip()
    parsed = json.loads(raw_text)
    parsed["via"] = f"llm (ollama:{model})"
    return parsed


def llm_interpret(user_input: str, api_key: str = None) -> dict:
    """
    Fast & intelligent interpreter pipeline:
    1. Checks fast-path rule matcher (0ms latency for exact commands).
    2. Uses LLM for complex/vague prompts.
    3. Gracefully falls back to rule-based parser on network delay.
    """
    # Fast path: instant response for high-confidence clear commands
    rule_res = rule_based_interpret(user_input)
    if rule_res.get("confidence", 0) >= 0.8 and rule_res.get("action") not in ("unknown", "need_pid"):
        rule_res["via"] = "fast-path (0ms)"
        return rule_res

    provider, effective_key = detect_provider(api_key)

    if not provider:
        rule_res["via"] = "rule-based"
        return rule_res

    try:
        parsed = None
        if provider == "gemini" and effective_key:
            parsed = call_gemini(user_input, effective_key)
        elif provider == "openai" and effective_key:
            parsed = call_openai(user_input, effective_key)
        elif provider == "anthropic" and effective_key:
            parsed = call_anthropic(user_input, effective_key)
        elif provider == "ollama":
            parsed = call_ollama(user_input)

        if parsed and isinstance(parsed, dict) and "action" in parsed:
            parsed["raw_input"] = user_input
            parsed.setdefault("confidence", 0.95)
            parsed.setdefault("params", {})
            return parsed

    except Exception as err:
        print(f"[LLM Agent] Fast fallback active. Provider '{provider}' notice: {err}")

    rule_res["via"] = "rule-based (fallback)"
    return rule_res


