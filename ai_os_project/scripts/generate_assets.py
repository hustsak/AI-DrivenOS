"""
AI-OS Visual Assets Generator
Generates premium SVG and animated GIF visual assets for GitHub presentation.
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# ── Color Palette ────────────────────────────────────────────────────────────
BG_DARK = "#090b10"
BG_PANEL = "#0f121a"
BORDER_COLOR = "#1f2433"
ACCENT_CYAN = "#00d4ff"
ACCENT_GREEN = "#10b981"
ACCENT_PURPLE = "#7c3aed"
TEXT_MAIN = "#e2e8f0"
TEXT_MUTED = "#64748b"


def create_banner_svg():
    path = os.path.join(ASSETS_DIR, "ai-os-banner.svg")
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 420" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#080a0f"/>
      <stop offset="50%" stop-color="#0f131d"/>
      <stop offset="100%" stop-color="#090b11"/>
    </linearGradient>

    <linearGradient id="headMetal" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3a4254"/>
      <stop offset="40%" stop-color="#1e2330"/>
      <stop offset="100%" stop-color="#0f121a"/>
    </linearGradient>

    <linearGradient id="titleMetal" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="60%" stop-color="#cbd5e1"/>
      <stop offset="100%" stop-color="#00d4ff"/>
    </linearGradient>

    <radialGradient id="cyanGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00d4ff" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#00d4ff" stop-opacity="0"/>
    </radialGradient>

    <filter id="glow">
      <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <style>
      .mono { font-family: 'JetBrains Mono', 'Space Grotesk', monospace, sans-serif; }
      .sans { font-family: 'Space Grotesk', system-ui, -apple-system, sans-serif; }
      .glow-text { filter: drop-shadow(0px 0px 8px rgba(0, 212, 255, 0.4)); }
    </style>
  </defs>

  <!-- Background Layer -->
  <rect width="1200" height="420" rx="16" fill="url(#bgGrad)" stroke="#1e2433" stroke-width="1.5"/>

  <!-- Technical Grid overlay -->
  <g opacity="0.05" stroke="#00d4ff" stroke-width="1">
    <path d="M0 60 H1200 M0 120 H1200 M0 180 H1200 M0 240 H1200 M0 300 H1200 M0 360 H1200" />
    <path d="M100 0 V420 M200 0 V420 M300 0 V420 M400 0 V420 M500 0 V420 M600 0 V420 M700 0 V420 M800 0 V420 M900 0 V420 M1000 0 V420 M1100 0 V420" />
  </g>

  <!-- Ambient Light Glow behind Robot -->
  <circle cx="920" cy="210" r="220" fill="url(#cyanGlow)"/>

  <!-- LEFT COLUMN: Typography & Telemetry -->
  <g transform="translate(80, 0)">

    <!-- Top System Tag -->
    <g transform="translate(0, 75)">
      <rect width="210" height="24" rx="4" fill="rgba(0, 212, 255, 0.08)" stroke="rgba(0, 212, 255, 0.3)" stroke-width="1"/>
      <circle cx="14" cy="12" r="3.5" fill="#00d4ff"/>
      <text x="26" y="16" class="mono" font-size="10" font-weight="700" fill="#00d4ff" letter-spacing="1.5">REASONING OS ENGINE v2</text>
    </g>

    <!-- Main Title -->
    <text x="0" y="175" class="sans glow-text" font-size="76" font-weight="800" fill="url(#titleMetal)" letter-spacing="-1">AI-OS</text>

    <!-- Subtitle -->
    <text x="0" y="215" class="mono" font-size="14" font-weight="600" fill="#94a3b8" letter-spacing="4">INTELLIGENT SYSTEM LAYER</text>

    <!-- Tagline -->
    <g transform="translate(0, 260)">
      <text x="0" y="0" class="mono" font-size="12" font-weight="700" fill="#00d4ff" letter-spacing="3">UNDERSTAND.</text>
      <text x="135" y="0" class="mono" font-size="12" font-weight="700" fill="#e2e8f0" letter-spacing="3">DECIDE.</text>
      <text x="225" y="0" class="mono" font-size="12" font-weight="700" fill="#10b981" letter-spacing="3">EXECUTE.</text>
    </g>

    <!-- Telemetry Badges -->
    <g transform="translate(0, 310)">
      <!-- Badge 1: LLM Engine -->
      <rect x="0" y="0" width="185" height="28" rx="6" fill="#141824" stroke="#2a3245" stroke-width="1"/>
      <text x="12" y="18" class="mono" font-size="10" fill="#a78bfa">🤖 OLLAMA / GEMINI / CLAUDE</text>

      <!-- Badge 2: Fast Path -->
      <rect x="197" y="0" width="145" height="28" rx="6" fill="#141824" stroke="#2a3245" stroke-width="1"/>
      <text x="209" y="18" class="mono" font-size="10" fill="#34d399">⚡ 0MS FAST-PATH</text>

      <!-- Badge 3: Windows OS -->
      <rect x="354" y="0" width="140" height="28" rx="6" fill="#141824" stroke="#2a3245" stroke-width="1"/>
      <text x="366" y="18" class="mono" font-size="10" fill="#38bdf8">💻 WINDOWS OS</text>
    </g>
  </g>

  <!-- RIGHT COLUMN: 3D Robotic AI Assistant Head -->
  <g transform="translate(900, 200)">

    <!-- Floating Node Connections -->
    <g stroke="rgba(0, 212, 255, 0.2)" stroke-width="1.2" stroke-dasharray="4,4">
      <line x1="-120" y1="-80" x2="-20" y2="-40" />
      <line x1="-140" y1="20" x2="-50" y2="10" />
      <line x1="-110" y1="100" x2="-30" y2="50" />
      <line x1="120" y1="-70" x2="30" y2="-40" />
      <line x1="130" y1="60" x2="40" y2="30" />
    </g>

    <circle cx="-120" cy="-80" r="3" fill="#00d4ff"/>
    <circle cx="-140" cy="20" r="3" fill="#7c3aed"/>
    <circle cx="-110" cy="100" r="3" fill="#10b981"/>
    <circle cx="120" cy="-70" r="3" fill="#00d4ff"/>
    <circle cx="130" cy="60" r="3" fill="#00d4ff"/>

    <!-- Outer Telemetry Ring -->
    <circle cx="0" cy="0" r="140" fill="none" stroke="rgba(0, 212, 255, 0.15)" stroke-width="1" stroke-dasharray="8 6"/>
    <circle cx="0" cy="0" r="125" fill="none" stroke="rgba(226, 232, 240, 0.08)" stroke-width="1"/>

    <!-- Neck Structure -->
    <path d="M-25 90 L25 90 L35 130 L-35 130 Z" fill="#151924" stroke="#2e374d" stroke-width="1.5"/>
    <rect x="-20" y="98" width="40" height="4" rx="2" fill="#00d4ff" opacity="0.6"/>

    <!-- Head Main Outline (Geometrical Metallic Contour) -->
    <path d="M-65 -40 
             C-65 -100, 65 -100, 65 -40 
             C65 20, 50 80, 0 92 
             C-50 80, -65 20, -65 -40 Z" 
          fill="url(#headMetal)" 
          stroke="#4b556b" 
          stroke-width="2"/>

    <!-- Side Cranial Panels -->
    <path d="M-60 -30 C-60 -80, -20 -90, 0 -90" fill="none" stroke="#64748b" stroke-width="1.5" opacity="0.6"/>
    <path d="M60 -30 C60 -80, 20 -90, 0 -90" fill="none" stroke="#64748b" stroke-width="1.5" opacity="0.6"/>

    <!-- Temple Joint Nodes -->
    <circle cx="-62" cy="-25" r="5" fill="#10141f" stroke="#00d4ff" stroke-width="1.5"/>
    <circle cx="62" cy="-25" r="5" fill="#10141f" stroke="#00d4ff" stroke-width="1.5"/>

    <!-- Dark Translucent Visor Plate -->
    <path d="M-52 -35 C-52 -55, 52 -55, 52 -35 C52 10, 38 40, 0 45 C-38 40, -52 10, -52 -35 Z" 
          fill="#0a0d14" 
          stroke="#252c3d" 
          stroke-width="1.5"/>

    <!-- Dual Glowing Aperture Eyes -->
    <!-- Left Eye -->
    <g transform="translate(-22, -18)">
      <circle cx="0" cy="0" r="14" fill="#060910" stroke="#1e293b" stroke-width="1.5"/>
      <circle cx="0" cy="0" r="10" fill="none" stroke="#00d4ff" stroke-width="1.5" opacity="0.7"/>
      <circle cx="0" cy="0" r="5" fill="#00d4ff" filter="url(#glow)"/>
      <circle cx="0" cy="0" r="2" fill="#ffffff"/>
    </g>

    <!-- Right Eye -->
    <g transform="translate(22, -18)">
      <circle cx="0" cy="0" r="14" fill="#060910" stroke="#1e293b" stroke-width="1.5"/>
      <circle cx="0" cy="0" r="10" fill="none" stroke="#00d4ff" stroke-width="1.5" opacity="0.7"/>
      <circle cx="0" cy="0" r="5" fill="#00d4ff" filter="url(#glow)"/>
      <circle cx="0" cy="0" r="2" fill="#ffffff"/>
    </g>

    <!-- Visor Glare Line -->
    <path d="M-40 -42 L30 -42" stroke="rgba(255,255,255,0.15)" stroke-width="2" stroke-linecap="round"/>

    <!-- Jaw & Mouth Telemetry Indicator -->
    <rect x="-18" y="24" width="36" height="3" rx="1.5" fill="#1e293b"/>
    <rect x="-10" y="24" width="20" height="3" rx="1.5" fill="#00d4ff" opacity="0.8"/>
  </g>

</svg>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Created {path}")


def create_assistant_svg():
    path = os.path.join(ASSETS_DIR, "ai-assistant.svg")
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 480" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#07090e"/>
      <stop offset="100%" stop-color="#0f131c"/>
    </linearGradient>

    <linearGradient id="headMetal2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3b4354"/>
      <stop offset="50%" stop-color="#1f2432"/>
      <stop offset="100%" stop-color="#0d1017"/>
    </linearGradient>

    <radialGradient id="cyanGlow2" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00d4ff" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#00d4ff" stop-opacity="0"/>
    </radialGradient>

    <style>
      .mono { font-family: 'JetBrains Mono', monospace; }
      .sans { font-family: 'Space Grotesk', sans-serif; }

      @keyframes pulseGlow {
        0%, 100% { opacity: 0.4; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.05); }
      }
      @keyframes scanLine {
        0% { transform: translateY(-30px); opacity: 0; }
        50% { opacity: 1; }
        100% { transform: translateY(30px); opacity: 0; }
      }
      @keyframes eyeGlow {
        0%, 100% { fill: #00d4ff; }
        50% { fill: #38bdf8; }
      }
      @keyframes orbitRot {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }

      .animated-glow { animation: pulseGlow 4s infinite ease-in-out; transform-origin: 425px 230px; }
      .animated-scan { animation: scanLine 3s infinite linear; }
      .animated-eye { animation: eyeGlow 2s infinite ease-in-out; }
      .animated-orbit { animation: orbitRot 12s infinite linear; transform-origin: 425px 210px; }
    </style>
  </defs>

  <!-- Background Container -->
  <rect width="850" height="480" rx="14" fill="url(#bgGrad2)" stroke="#1d2333" stroke-width="1.5"/>

  <!-- Ambient Backdrop Glow -->
  <circle cx="425" cy="210" r="180" fill="url(#cyanGlow2)" class="animated-glow"/>

  <!-- Orbital HUD Ring -->
  <g class="animated-orbit">
    <circle cx="425" cy="210" r="150" fill="none" stroke="rgba(0, 212, 255, 0.2)" stroke-width="1.2" stroke-dasharray="12 8 4 8"/>
    <circle cx="275" cy="210" r="3" fill="#00d4ff"/>
    <circle cx="575" cy="210" r="3" fill="#7c3aed"/>
    <circle cx="425" cy="60" r="3" fill="#10b981"/>
  </g>

  <!-- Top Telemetry Header -->
  <g transform="translate(30, 40)">
    <text x="0" y="0" class="mono" font-size="11" font-weight="700" fill="#00d4ff" letter-spacing="2">SYSTEM AGENT // LIVE VISUAL TELEMETRY</text>
    <rect x="0" y="10" width="790" height="1" fill="#1a202c"/>
  </g>

  <!-- ROBOT AI ASSISTANT HEAD (Center 425, 210) -->
  <g transform="translate(425, 210)">

    <!-- Neck Interface -->
    <path d="M-30 95 L30 95 L40 140 L-40 140 Z" fill="#141824" stroke="#2d364a" stroke-width="1.5"/>
    <rect x="-24" y="105" width="48" height="4" rx="2" fill="#00d4ff" opacity="0.7"/>

    <!-- Head Chassis -->
    <path d="M-75 -45 C-75 -115, 75 -115, 75 -45 C75 25, 55 90, 0 102 C-55 90, -75 25, -75 -45 Z" 
          fill="url(#headMetal2)" 
          stroke="#475569" 
          stroke-width="2"/>

    <!-- Cranial Contour Panels -->
    <path d="M-68 -35 C-68 -90, -25 -102, 0 -102" fill="none" stroke="#64748b" stroke-width="1.5" opacity="0.6"/>
    <path d="M68 -35 C68 -90, 25 -102, 0 -102" fill="none" stroke="#64748b" stroke-width="1.5" opacity="0.6"/>

    <!-- Temple Nodes -->
    <circle cx="-72" cy="-28" r="6" fill="#0f121a" stroke="#00d4ff" stroke-width="1.5"/>
    <circle cx="72" cy="-28" r="6" fill="#0f121a" stroke="#00d4ff" stroke-width="1.5"/>

    <!-- Visor Plate -->
    <path d="M-60 -38 C-60 -60, 60 -60, 60 -38 C60 12, 44 48, 0 52 C-44 48, -60 12, -60 -38 Z" 
          fill="#07090e" 
          stroke="#242b3b" 
          stroke-width="1.5"/>

    <!-- Scanline effect across visor -->
    <g class="animated-scan">
      <line x1="-50" y1="0" x2="50" y2="0" stroke="rgba(0, 212, 255, 0.4)" stroke-width="1.5"/>
    </g>

    <!-- Eyes (Left & Right) -->
    <g transform="translate(-26, -18)">
      <circle cx="0" cy="0" r="16" fill="#05070a" stroke="#1e293b" stroke-width="1.5"/>
      <circle cx="0" cy="0" r="11" fill="none" stroke="#00d4ff" stroke-width="1.2" opacity="0.8"/>
      <circle cx="0" cy="0" r="6" fill="#00d4ff" class="animated-eye"/>
      <circle cx="0" cy="0" r="2" fill="#ffffff"/>
    </g>

    <g transform="translate(26, -18)">
      <circle cx="0" cy="0" r="16" fill="#05070a" stroke="#1e293b" stroke-width="1.5"/>
      <circle cx="0" cy="0" r="11" fill="none" stroke="#00d4ff" stroke-width="1.2" opacity="0.8"/>
      <circle cx="0" cy="0" r="6" fill="#00d4ff" class="animated-eye"/>
      <circle cx="0" cy="0" r="2" fill="#ffffff"/>
    </g>

    <!-- Jaw Bar -->
    <rect x="-20" y="28" width="40" height="3" rx="1.5" fill="#1e293b"/>
    <rect x="-12" y="28" width="24" height="3" rx="1.5" fill="#00d4ff" opacity="0.8"/>
  </g>

  <!-- Bottom Telemetry Status Bar -->
  <g transform="translate(30, 420)">
    <!-- Status Card -->
    <rect width="790" height="36" rx="8" fill="#0f131d" stroke="#1e2536" stroke-width="1"/>
    
    <circle cx="20" cy="18" r="4" fill="#10b981"/>
    <text x="32" y="22" class="mono" font-size="11" font-weight="700" fill="#e2e8f0">STATE: IDLE / READY</text>

    <text x="320" y="22" class="mono" font-size="11" fill="#94a3b8">MODEL: <tspan fill="#00d4ff">ollama:qwen2.5-coder:7b</tspan></text>
    <text x="640" y="22" class="mono" font-size="11" fill="#94a3b8">LATENCY: <tspan fill="#34d399">0.0 ms (fast-path)</tspan></text>
  </g>

</svg>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Created {path}")


def create_terminal_svg():
    path = os.path.join(ASSETS_DIR, "terminal-demo.svg")
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 520" width="100%" height="100%">
  <defs>
    <style>
      .mono { font-family: 'JetBrains Mono', Consolas, monospace; }
      .prompt { fill: #00d4ff; font-weight: bold; }
      .cmd { fill: #f8fafc; font-weight: 500; }
      .ai-header { fill: #a78bfa; font-weight: bold; }
      .ai-insight { fill: #38bdf8; }
      .success { fill: #34d399; font-weight: bold; }
      .output { fill: #cbd5e1; }
      .muted { fill: #64748b; }
      .bar-fill { fill: #10b981; }
    </style>
  </defs>

  <!-- Window Container -->
  <rect width="900" height="520" rx="12" fill="#090b10" stroke="#1e2433" stroke-width="1.5"/>

  <!-- Terminal Header Bar -->
  <rect width="900" height="38" rx="12" fill="#121622"/>
  <rect y="26" width="900" height="12" fill="#121622"/>
  <line x1="0" y1="38" x2="900" y2="38" stroke="#1f2638" stroke-width="1"/>

  <!-- Window Dots -->
  <circle cx="20" cy="19" r="5.5" fill="#ff5f56"/>
  <circle cx="38" cy="19" r="5.5" fill="#ffbd2e"/>
  <circle cx="56" cy="19" r="5.5" fill="#27c93f"/>

  <!-- Title -->
  <text x="450" y="23" text-anchor="middle" class="mono" font-size="11" fill="#64748b" letter-spacing="1">user@ai-os — interactive terminal (bash)</text>

  <!-- Terminal Body Content -->
  <g transform="translate(24, 65)">

    <!-- Command 1: open telegram -->
    <g transform="translate(0, 0)">
      <text class="mono prompt" font-size="13">❯</text>
      <text x="18" class="mono cmd" font-size="13">open telegram</text>

      <text y="22" class="mono muted" font-size="11">  [21:15:35] Action: open_app | Via: llm (ollama:qwen2.5-coder:7b) | Confidence: 100%</text>
      <text y="38" class="mono ai-insight" font-size="11">🤖 AI Insight: Telegram Desktop is launching now.</text>

      <text y="60" class="mono success" font-size="12">✅ Launched 'telegram'</text>
      <line x1="0" y1="68" x2="850" y2="68" stroke="#1b202e" stroke-width="1"/>
      <text y="84" class="mono output" font-size="12">🚀 Successfully launched 'telegram' on your PC!</text>
    </g>

    <!-- Command 2: how is my memory? -->
    <g transform="translate(0, 125)">
      <text class="mono prompt" font-size="13">❯</text>
      <text x="18" class="mono cmd" font-size="13">how is my memory?</text>

      <text y="22" class="mono muted" font-size="11">  [21:16:02] Action: get_memory_usage | Via: fast-path (0ms) | Confidence: 95%</text>

      <text y="44" class="mono success" font-size="12">✅ RAM Memory usage retrieved</text>
      <line x1="0" y1="52" x2="850" y2="52" stroke="#1b202e" stroke-width="1"/>

      <text y="70" class="mono output" font-size="12">RAM Usage:     [<tspan fill="#10b981">████████████░░░░░░░░</tspan>] 51.8%</text>
      <text y="88" class="mono output" font-size="12">Used:          16.43 GB / 31.71 GB</text>
      <text y="106" class="mono output" font-size="12">Available:     15.28 GB</text>
    </g>

    <!-- Command 3: open visual studio code -->
    <g transform="translate(0, 275)">
      <text class="mono prompt" font-size="13">❯</text>
      <text x="18" class="mono cmd" font-size="13">open visual studio code</text>

      <text y="22" class="mono muted" font-size="11">  [21:16:40] Action: open_app | Via: llm (ollama:qwen2.5-coder:7b) | Confidence: 100%</text>

      <text y="44" class="mono success" font-size="12">✅ Launched 'Visual Studio Code'</text>
      <line x1="0" y1="52" x2="850" y2="52" stroke="#1b202e" stroke-width="1"/>
      <text y="70" class="mono output" font-size="12">🚀 Successfully launched 'Visual Studio Code' on your PC!</text>
    </g>

    <!-- Command Prompt Active -->
    <g transform="translate(0, 385)">
      <text class="mono prompt" font-size="13">❯</text>
      <rect x="18" y="-11" width="8" height="15" fill="#00d4ff" opacity="0.8"/>
    </g>

  </g>
</svg>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Created {path}")


def create_architecture_svg():
    path = os.path.join(ASSETS_DIR, "architecture.svg")
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 580" width="100%" height="100%">
  <defs>
    <linearGradient id="boxGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#121622"/>
      <stop offset="100%" stop-color="#0b0e16"/>
    </linearGradient>

    <style>
      .mono { font-family: 'JetBrains Mono', monospace; }
      .sans { font-family: 'Space Grotesk', sans-serif; }
      .box { fill: url(#boxGrad); stroke: #222a3d; stroke-width: 1.5; rx: 8; }
      .box-highlight { fill: url(#boxGrad); stroke: #00d4ff; stroke-width: 1.5; rx: 8; }
      .title { font-size: 11px; font-weight: bold; fill: #00d4ff; letter-spacing: 1px; }
      .label { font-size: 12px; font-weight: bold; fill: #e2e8f0; }
      .sub { font-size: 10px; fill: #94a3b8; }
      .line { stroke: #2a344a; stroke-width: 1.5; }
      .line-active { stroke: #00d4ff; stroke-width: 1.5; stroke-dasharray: 4,4; }
    </style>
  </defs>

  <!-- Background -->
  <rect width="1000" height="580" rx="14" fill="#080a0f" stroke="#1d2333" stroke-width="1.5"/>

  <!-- Header -->
  <text x="40" y="45" class="mono" font-size="14" font-weight="700" fill="#00d4ff" letter-spacing="2">SYSTEM ARCHITECTURE MAP</text>
  <text x="40" y="65" class="mono" font-size="11" fill="#64748b">AI-Driven OS Layer &amp; Multi-LLM Execution Flow</text>

  <!-- 1. USER INPUT -->
  <g transform="translate(400, 90)">
    <rect width="200" height="42" class="box"/>
    <text x="100" y="25" text-anchor="middle" class="label">👤 USER PROMPT</text>
    <text x="100" y="36" text-anchor="middle" class="sub">("open telegram", "how is my RAM")</text>
  </g>

  <!-- Down Line -->
  <line x1="500" y1="132" x2="500" y2="160" class="line"/>

  <!-- 2. AI INTERPRETER PIPELINE -->
  <g transform="translate(350, 160)">
    <rect width="300" height="50" class="box-highlight"/>
    <text x="150" y="24" text-anchor="middle" class="title">🧠 AI AGENT INTERPRETER</text>
    <text x="150" y="40" text-anchor="middle" class="sub">Fast-Path Rule Matcher + Multi-LLM Engine</text>
  </g>

  <!-- Lines from Interpreter to LLM Providers -->
  <path d="M500 210 V235 H150 V260" class="line"/>
  <path d="M500 210 V235 H380 V260" class="line"/>
  <path d="M500 210 V235 H620 V260" class="line"/>
  <path d="M500 210 V235 H850 V260" class="line"/>

  <!-- 3. MULTI-LLM ENGINE BOXES -->
  <!-- Ollama -->
  <g transform="translate(60, 260)">
    <rect width="180" height="55" class="box"/>
    <text x="90" y="25" text-anchor="middle" class="label" fill="#38bdf8">🦙 OLLAMA (Local)</text>
    <text x="90" y="42" text-anchor="middle" class="sub">qwen2.5-coder:7b / llama3</text>
  </g>
  <!-- Gemini -->
  <g transform="translate(290, 260)">
    <rect width="180" height="55" class="box"/>
    <text x="90" y="25" text-anchor="middle" class="label" fill="#a78bfa">♊ GOOGLE GEMINI</text>
    <text x="90" y="42" text-anchor="middle" class="sub">gemini-1.5-flash API</text>
  </g>
  <!-- OpenAI -->
  <g transform="translate(530, 260)">
    <rect width="180" height="55" class="box"/>
    <text x="90" y="25" text-anchor="middle" class="label" fill="#34d399">🤖 OPENAI</text>
    <text x="90" y="42" text-anchor="middle" class="sub">gpt-4o-mini API</text>
  </g>
  <!-- Claude -->
  <g transform="translate(760, 260)">
    <rect width="180" height="55" class="box"/>
    <text x="90" y="25" text-anchor="middle" class="label" fill="#f472b6">🧠 CLAUDE</text>
    <text x="90" y="42" text-anchor="middle" class="sub">claude-3-5-haiku API</text>
  </g>

  <!-- Convergence Lines to Intent & Dispatcher -->
  <path d="M150 315 V340 H500" class="line"/>
  <path d="M380 315 V340 H500" class="line"/>
  <path d="M620 315 V340 H500" class="line"/>
  <path d="M850 315 V340 H500" class="line"/>
  <line x1="500" y1="340" x2="500" y2="365" class="line"/>

  <!-- 4. STRUCTURED ACTION INTENT -->
  <g transform="translate(340, 365)">
    <rect width="320" height="46" class="box"/>
    <text x="160" y="22" text-anchor="middle" class="title">📋 STRUCTURED JSON INTENT</text>
    <text x="160" y="38" text-anchor="middle" class="sub">{"action": "open_app", "params": {"app": "telegram"}}</text>
  </g>

  <line x1="500" y1="411" x2="500" y2="435" class="line"/>

  <!-- 5. COMMAND DISPATCHER & SAFETY LAYER -->
  <g transform="translate(320, 435)">
    <rect width="360" height="46" class="box-highlight"/>
    <text x="180" y="22" text-anchor="middle" class="title">🛡️ EXECUTOR &amp; SAFETY DISPATCHER</text>
    <text x="180" y="38" text-anchor="middle" class="sub">utils/executor.py + Command Logger</text>
  </g>

  <path d="M500 481 V505 H170 V525" class="line"/>
  <path d="M500 481 V505 H500 V525" class="line"/>
  <path d="M500 481 V505 H830 V525" class="line"/>

  <!-- 6. WINDOWS OS EXECUTION LAYER -->
  <!-- App Launcher -->
  <g transform="translate(70, 525)">
    <rect width="200" height="40" class="box"/>
    <text x="100" y="24" text-anchor="middle" class="label" fill="#00d4ff">🚀 APP LAUNCHER</text>
  </g>
  <!-- System Monitor -->
  <g transform="translate(400, 525)">
    <rect width="200" height="40" class="box"/>
    <text x="100" y="24" text-anchor="middle" class="label" fill="#10b981">📊 PROCESS &amp; RAM STATS</text>
  </g>
  <!-- File Cleanup -->
  <g transform="translate(730, 525)">
    <rect width="200" height="40" class="box"/>
    <text x="100" y="24" text-anchor="middle" class="label" fill="#a78bfa">🧹 DISK &amp; FILE CLEANER</text>
  </g>

</svg>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Created {path}")


def create_animated_gifs():
    """Generates optimized GIF animations matching the SVGs."""

    # 1. ai-assistant.gif (850 x 480, 12 frames loop)
    assistant_gif_path = os.path.join(ASSETS_DIR, "ai-assistant.gif")
    frames = []
    width, height = 850, 480

    states = [
        ("BOOT // ONLINE", "#00d4ff", "SYSTEM READY"),
        ("LISTENING...", "#00d4ff", "USER PROMPT DETECTED"),
        ("THINKING...", "#a78bfa", "OLLAMA MODEL INFERENCE"),
        ("EXECUTING...", "#38bdf8", "ACTION: open_app [telegram]"),
        ("SUCCESS", "#10b981", "✓ TELEGRAM LAUNCHED"),
        ("IDLE / READY", "#00d4ff", "AWAITING NEXT COMMAND")
    ]

    for i in range(18):
        img = Image.new("RGB", (width, height), color="#090b10")
        draw = ImageDraw.Draw(img)

        # Outer border
        draw.rounded_rectangle([1, 1, width-2, height-2], radius=14, fill="#090b10", outline="#1d2333", width=2)

        # Header
        draw.text((30, 30), "SYSTEM AGENT // LIVE VISUAL TELEMETRY", fill="#00d4ff")

        # Head Center (425, 210)
        cx, cy = 425, 210
        pulse = math.sin(i * 0.5) * 8

        # Orbital Ring
        draw.ellipse([cx-150-pulse, cy-150-pulse, cx+150+pulse, cy+150+pulse], outline="#00d4ff", width=1)

        # Robot Head Body Contour
        head_pts = [(cx-70, cy-50), (cx+70, cy-50), (cx+50, cy+80), (cx, cy+95), (cx-50, cy+80)]
        draw.polygon(head_pts, fill="#1a202c", outline="#475569", width=2)

        # Visor
        visor_pts = [(cx-55, cy-40), (cx+55, cy-40), (cx+40, cy+45), (cx, cy+50), (cx-40, cy+45)]
        draw.polygon(visor_pts, fill="#07090e", outline="#242b3b", width=2)

        # Eyes
        state_idx = (i // 3) % len(states)
        st_title, st_color, st_msg = states[state_idx]

        # Left Eye & Right Eye
        eye_color = st_color
        draw.ellipse([cx-40, cy-30, cx-10, cy], outline="#1e293b", width=2)
        draw.ellipse([cx-30, cy-22, cx-20, cy-12], fill=eye_color)

        draw.ellipse([cx+10, cy-30, cx+40, cy], outline="#1e293b", width=2)
        draw.ellipse([cx+20, cy-22, cx+30, cy-12], fill=eye_color)

        # Bottom Bar
        draw.rounded_rectangle([30, 415, 820, 455], radius=8, fill="#0f131d", outline="#1e2536", width=1)
        draw.ellipse([45, 431, 53, 439], fill=st_color)
        draw.text((65, 428), f"STATE: {st_title} — {st_msg}", fill="#e2e8f0")

        frames.append(img)

    frames[0].save(
        assistant_gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=400,
        loop=0,
        optimize=True
    )
    print(f"Created {assistant_gif_path}")

    # 2. terminal-demo.gif (900 x 520)
    term_gif_path = os.path.join(ASSETS_DIR, "terminal-demo.gif")
    t_frames = []
    tw, th = 900, 520

    t_lines = [
        "❯ open telegram",
        "  [21:15:35] Action: open_app | Via: llm (ollama:qwen2.5-coder:7b) | Confidence: 100%",
        "🤖 AI Insight: Telegram Desktop is launching now.",
        "✅ Launched 'telegram'",
        "🚀 Successfully launched 'telegram' on your PC!",
        "",
        "❯ how is my memory?",
        "  [21:16:02] Action: get_memory_usage | Via: fast-path (0ms) | Confidence: 95%",
        "✅ RAM Memory usage retrieved",
        "RAM Usage:     [████████████░░░░░░░░] 51.8%",
        "Used:          16.43 GB / 31.71 GB",
        ""
    ]

    for step in range(1, len(t_lines) + 1):
        img = Image.new("RGB", (tw, th), color="#090b10")
        draw = ImageDraw.Draw(img)

        # Window Frame
        draw.rounded_rectangle([1, 1, tw-2, th-2], radius=12, fill="#090b10", outline="#1e2433", width=2)
        draw.rectangle([0, 0, tw, 38], fill="#121622")
        draw.ellipse([15, 14, 25, 24], fill="#ff5f56")
        draw.ellipse([33, 14, 43, 24], fill="#ffbd2e")
        draw.ellipse([51, 14, 61, 24], fill="#27c93f")
        draw.text((360, 12), "user@ai-os — interactive terminal (bash)", fill="#64748b")

        y = 60
        for line in t_lines[:step]:
            col = "#00d4ff" if line.startswith("❯") else "#34d399" if line.startswith("✅") else "#38bdf8" if "🤖" in line else "#cbd5e1"
            draw.text((30, y), line, fill=col)
            y += 24

        t_frames.append(img)

    t_frames[0].save(
        term_gif_path,
        save_all=True,
        append_images=t_frames[1:],
        duration=600,
        loop=0,
        optimize=True
    )
    print(f"Created {term_gif_path}")

    # 3. architecture.gif (1000 x 580)
    arch_gif_path = os.path.join(ASSETS_DIR, "architecture.gif")
    arch_img = Image.new("RGB", (1000, 580), color="#080a0f")
    draw = ImageDraw.Draw(arch_img)
    draw.rounded_rectangle([1, 1, 998, 578], radius=14, fill="#080a0f", outline="#1d2333", width=2)
    draw.text((40, 30), "SYSTEM ARCHITECTURE MAP // RUNTIME DATA STREAM", fill="#00d4ff")

    a_frames = []
    for f_idx in range(10):
        frame = arch_img.copy()
        f_draw = ImageDraw.Draw(frame)

        # Draw nodes
        f_draw.rounded_rectangle([380, 80, 620, 130], radius=8, fill="#121622", outline="#00d4ff", width=2)
        f_draw.text((430, 98), "👤 USER PROMPT", fill="#e2e8f0")

        f_draw.rounded_rectangle([320, 180, 680, 240], radius=8, fill="#121622", outline="#00d4ff", width=2)
        f_draw.text((380, 202), "🧠 AI AGENT INTERPRETER", fill="#00d4ff")

        f_draw.rounded_rectangle([320, 300, 680, 360], radius=8, fill="#121622", outline="#10b981", width=2)
        f_draw.text((370, 322), "🛡️ EXECUTOR & SAFETY LAYER", fill="#10b981")

        f_draw.rounded_rectangle([320, 420, 680, 480], radius=8, fill="#121622", outline="#38bdf8", width=2)
        f_draw.text((390, 442), "💻 WINDOWS SYSTEM KERNEL", fill="#38bdf8")

        # Moving cyan particle pulse
        p_y = 130 + (f_idx * 30) % 350
        f_draw.ellipse([495, p_y, 505, p_y+10], fill="#00d4ff")

        a_frames.append(frame)

    a_frames[0].save(
        arch_gif_path,
        save_all=True,
        append_images=a_frames[1:],
        duration=250,
        loop=0,
        optimize=True
    )
    print(f"Created {arch_gif_path}")


if __name__ == "__main__":
    print("Generating AI-OS GitHub Visual Assets...")
    create_banner_svg()
    create_assistant_svg()
    create_terminal_svg()
    create_architecture_svg()
    create_animated_gifs()
    print("All assets generated successfully in assets/!")
