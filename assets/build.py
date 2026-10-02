#!/usr/bin/env python3
"""Generates the animated SVG assets used by the profile README.

Run from the repository root:  python3 assets/build.py

Every asset is self-contained (no external fonts, scripts or images), so it
renders inside GitHub's <img> sandbox. Motion uses CSS keyframes and SMIL,
and CSS motion is disabled for viewers who prefer reduced motion.
"""
import random
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent
random.seed(1337)

ACCENT = "#ff1e3c"
WHITE = "#ffffff"
CRIMSON = "#a8001a"
ROSE = "#ff7a8a"
BG = "#050505"
PANEL = "#2a0309"
TEXT = "#ffffff"
DIM = "#9a7a7f"
MONO = "'Fira Code','JetBrains Mono','Cascadia Code',Consolas,'Courier New',monospace"

# Bump when restyling: renamed files dodge cached copies of the old render.
THEME = "red"

REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def write(name, body):
    (OUT / name).write_text(body.strip() + "\n", encoding="utf-8")
    print("wrote", name)


# --------------------------------------------------------------------------
# Hero banner: hex rain, moving grid, radar sweep, glitching name, HUD.
# --------------------------------------------------------------------------
def hero():
    w, h = 1200, 380
    streams = []
    for i in range(26):
        x = 18 + i * 46 + random.randint(-6, 6)
        chars = "".join(random.choice("0123456789ABCDEF") for _ in range(16))
        tspans = "".join(
            f'<tspan x="{x}" dy="22">{c}</tspan>' for c in chars
        )
        dur = random.uniform(7, 15)
        delay = -random.uniform(0, dur)
        op = random.uniform(0.10, 0.30)
        streams.append(
            f'<text class="rain" style="animation-duration:{dur:.1f}s;'
            f'animation-delay:{delay:.1f}s" opacity="{op:.2f}" y="0">{tspans}</text>'
        )

    # Radar blips (angle-independent positions inside the scope)
    cx, cy, r = 985, 190, 128
    blips = []
    for i, (bx, by, col) in enumerate(
        [(-60, -48, CRIMSON), (42, -78, ROSE), (78, 34, ACCENT), (-30, 70, WHITE), (14, 12, ACCENT)]
    ):
        blips.append(
            f'<g transform="translate({cx + bx} {cy + by})">'
            f'<circle r="4" fill="{col}" class="blip" style="animation-delay:{i * 0.8:.1f}s"/>'
            f'<circle r="4" fill="none" stroke="{col}" class="ping" style="animation-delay:{i * 0.8:.1f}s"/>'
            "</g>"
        )

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Prayatna Pokhrel — Cybersecurity Undergraduate and Aspiring SOC Analyst">
  <title>Prayatna Pokhrel — Cybersecurity Undergraduate // Aspiring SOC Analyst</title>
  <defs>
    <radialGradient id="glow" cx="30%" cy="45%" r="75%">
      <stop offset="0" stop-color="{PANEL}"/>
      <stop offset="1" stop-color="{BG}"/>
    </radialGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="{ACCENT}" stroke-opacity=".07"/>
      <animateTransform attributeName="patternTransform" type="translate" from="0 0" to="40 40" dur="6s" repeatCount="indefinite"/>
    </pattern>
    <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/>
      <stop offset="1" stop-color="{ACCENT}" stop-opacity=".55"/>
    </linearGradient>
    <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{ACCENT}" stop-opacity=".16"/>
      <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="threat" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{WHITE}"/>
      <stop offset=".5" stop-color="{ACCENT}"/>
      <stop offset="1" stop-color="{CRIMSON}"/>
    </linearGradient>
    <linearGradient id="title" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{WHITE}"/>
      <stop offset=".55" stop-color="{WHITE}"/>
      <stop offset="1" stop-color="{ACCENT}"/>
    </linearGradient>
    <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ACCENT}"/>
      <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="veil" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{BG}" stop-opacity=".88"/>
      <stop offset=".45" stop-color="{BG}" stop-opacity=".7"/>
      <stop offset=".62" stop-color="{BG}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="frame"><rect width="{w}" height="{h}" rx="14"/></clipPath>
    <clipPath id="scope"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>
  </defs>
  <style>
    text{{font-family:{MONO}}}
    .rain{{fill:{ACCENT};font-size:15px;animation:fall linear infinite}}
    @keyframes fall{{from{{transform:translateY(-360px)}}to{{transform:translateY({h}px)}}}}
    .blip{{opacity:0;animation:blip 4s ease-out infinite}}
    .ping{{opacity:0;stroke-width:1.5;transform-box:fill-box;transform-origin:center;animation:ping 4s ease-out infinite}}
    @keyframes blip{{0%{{opacity:0}}8%{{opacity:1}}60%{{opacity:.35}}100%{{opacity:0}}}}
    @keyframes ping{{0%{{opacity:.9;transform:scale(1)}}50%{{opacity:0;transform:scale(5)}}100%{{opacity:0}}}}
    .name{{font-size:62px;font-weight:700;letter-spacing:4px}}
    .g1{{fill:{CRIMSON};opacity:.75;animation:g1 5s steps(1) infinite}}
    .g2{{fill:{WHITE};opacity:.75;animation:g2 5s steps(1) infinite}}
    @keyframes g1{{0%,88%,100%{{transform:translate(0,0);opacity:0}}89%{{transform:translate(-5px,2px);opacity:.8}}91%{{transform:translate(4px,-2px)}}93%{{transform:translate(-2px,0)}}95%{{opacity:0}}}}
    @keyframes g2{{0%,88%,100%{{transform:translate(0,0);opacity:0}}89%{{transform:translate(5px,-2px);opacity:.8}}92%{{transform:translate(-4px,2px)}}94%{{transform:translate(2px,0)}}95%{{opacity:0}}}}
    .cursor{{animation:blink 1s steps(1) infinite}}
    @keyframes blink{{50%{{opacity:0}}}}
    .live{{animation:pulse 1.6s ease-in-out infinite}}
    @keyframes pulse{{50%{{opacity:.25}}}}
    .scanbar{{animation:scan 5s linear infinite}}
    @keyframes scan{{from{{transform:translateY(-80px)}}to{{transform:translateY({h}px)}}}}
    .meter{{transform-box:fill-box;transform-origin:left;animation:meter 6s ease-in-out infinite}}
    @keyframes meter{{0%,100%{{transform:scaleX(.22)}}45%{{transform:scaleX(.38)}}70%{{transform:scaleX(.18)}}}}
    .ticker{{animation:tick 22s linear infinite}}
    @keyframes tick{{from{{transform:translateX(0)}}to{{transform:translateX(-1100px)}}}}
    {REDUCED}
  </style>

  <g clip-path="url(#frame)">
    <rect width="{w}" height="{h}" fill="url(#glow)"/>
    <rect width="{w}" height="{h}" fill="url(#grid)"/>
    {''.join(streams)}
    <rect width="{w}" height="{h}" fill="url(#veil)"/>

    <!-- radar -->
    <g>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="{BG}" fill-opacity=".75" stroke="{ACCENT}" stroke-opacity=".55"/>
      <circle cx="{cx}" cy="{cy}" r="{r * 2 // 3}" fill="none" stroke="{ACCENT}" stroke-opacity=".25"/>
      <circle cx="{cx}" cy="{cy}" r="{r // 3}" fill="none" stroke="{ACCENT}" stroke-opacity=".25"/>
      <path d="M{cx - r} {cy}H{cx + r}M{cx} {cy - r}V{cy + r}" stroke="{ACCENT}" stroke-opacity=".2"/>
      <g clip-path="url(#scope)">
        <path d="M{cx} {cy}L{cx + r} {cy}A{r} {r} 0 0 0 {cx + r * 0.5:.1f} {cy - r * 0.866:.1f}Z" fill="url(#sweep)" opacity=".7">
          <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="4s" repeatCount="indefinite"/>
        </path>
      </g>
      {''.join(blips)}
      <circle cx="{cx}" cy="{cy}" r="3" fill="{ACCENT}"/>
      <text x="{cx}" y="{cy + r + 26}" text-anchor="middle" font-size="12" fill="{DIM}" letter-spacing="3">THREAT SURFACE SCAN</text>
    </g>

    <!-- HUD header -->
    <text x="40" y="44" font-size="13" fill="{DIM}" letter-spacing="2">SYS://SOC-CONSOLE <tspan fill="{ACCENT}">▸</tspan> NODE KTM-NP <tspan fill="{ACCENT}">▸</tspan> SESSION 0x7E3A</text>
    <circle cx="672" cy="40" r="5" fill="{WHITE}" class="live"/>
    <text x="684" y="44" font-size="13" fill="{WHITE}" letter-spacing="2">MONITORING</text>

    <!-- identity -->
    <text x="40" y="132" font-size="16" fill="{ACCENT}" letter-spacing="2">$ whoami<tspan class="cursor">_</tspan></text>
    <g class="name">
      <text x="40" y="205" class="g1">PRAYATNA POKHREL</text>
      <text x="40" y="205" class="g2">PRAYATNA POKHREL</text>
      <text x="40" y="205" fill="url(#title)">PRAYATNA POKHREL</text>
    </g>
    <rect x="40" y="226" width="560" height="2" fill="url(#rule)"/>
    <text x="40" y="262" font-size="19" fill="{ACCENT}" letter-spacing="3">CYBERSECURITY UNDERGRADUATE</text>
    <text x="40" y="292" font-size="19" fill="{TEXT}" letter-spacing="3">// ASPIRING SOC ANALYST</text>

    <!-- threat meter -->
    <text x="40" y="340" font-size="12" fill="{DIM}" letter-spacing="2">ALERT QUEUE</text>
    <rect x="150" y="331" width="220" height="10" rx="2" fill="{PANEL}" stroke="{ACCENT}" stroke-opacity=".3"/>
    <rect x="150" y="331" width="220" height="10" rx="2" fill="url(#threat)" class="meter"/>
    <text x="384" y="340" font-size="12" fill="{WHITE}" letter-spacing="2">TRIAGED</text>

    <!-- scan line + HUD corners -->
    <rect width="{w}" height="80" fill="url(#scan)" class="scanbar"/>
    <g fill="none" stroke="{ACCENT}" stroke-width="2.5" stroke-opacity=".9">
      <path d="M16 46V16H46"/><path d="M{w - 46} 16H{w - 16}V46"/>
      <path d="M16 {h - 46}V{h - 16}H46"/><path d="M{w - 46} {h - 16}H{w - 16}V{h - 46}"/>
    </g>
  </g>
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14" fill="none" stroke="{ACCENT}" stroke-opacity=".35"/>
</svg>
"""
    write(f"hero-{THEME}.svg", svg)


# --------------------------------------------------------------------------
# Terminal: lines "type" themselves out in sequence, then the loop restarts.
# --------------------------------------------------------------------------
def terminal():
    w = 900
    cycle = 16.0
    lines = [
        ("cmd", "whoami --verbose"),
        ("out", "Prayatna Pokhrel · Cybersecurity & Ethical Hacking undergrad"),
        ("out", "Softwarica College · BSc (Hons), Coventry University"),
        ("cmd", "cat /etc/mission"),
        ("out", "target_role: SOC Analyst  |  base: Kathmandu, Nepal"),
        ("out", "studying:    CompTIA Security+"),
        ("cmd", "tail -f /var/log/focus.log"),
        ("ok", "[OK]  security monitoring   [OK]  alert triage"),
        ("ok", "[OK]  log analysis          [OK]  incident investigation"),
        ("cmd", "echo $MINDSET"),
        ("hi", "observe -> correlate -> investigate -> improve"),
    ]
    top, lh, left = 74, 30, 32
    h = top + lh * len(lines) + 34
    char_w = 9.6  # approx. advance of a 16px monospace glyph

    parts, clips = [], []
    t = 0.4
    for i, (kind, text) in enumerate(lines):
        y = top + i * lh
        prompt = kind == "cmd"
        full = escape(text)
        width = (len(text) + (3 if prompt else 0)) * char_w + 12
        dur = (0.04 * len(text)) if prompt else 0.25
        start, end = t / cycle, (t + dur) / cycle
        hold = (cycle - 1.2) / cycle
        clips.append(
            f'<clipPath id="l{i}"><rect x="{left - 4}" y="{y - 20}" height="28" width="0">'
            f'<animate attributeName="width" dur="{cycle}s" repeatCount="indefinite" calcMode="linear" '
            f'keyTimes="0;{start:.4f};{end:.4f};{hold:.4f};1" values="0;0;{width:.0f};{width:.0f};0"/>'
            "</rect></clipPath>"
        )
        colour = {"cmd": TEXT, "out": "#cdb8bb", "ok": WHITE, "hi": ACCENT}[kind]
        content = (
            f'<tspan fill="{WHITE}">❯ </tspan><tspan fill="{colour}">{full}</tspan>'
            if prompt
            else f'<tspan fill="{colour}">{full}</tspan>'
        )
        parts.append(f'<text x="{left}" y="{y}" clip-path="url(#l{i})">{content}</text>')
        t += dur + (0.35 if prompt else 0.15)

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Terminal: whoami, mission and focus areas">
  <title>Operator terminal</title>
  <defs>{''.join(clips)}
    <linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{PANEL}"/><stop offset=".6" stop-color="#14070a"/><stop offset="1" stop-color="{BG}"/>
    </linearGradient>
  </defs>
  <style>
    text{{font-family:{MONO};font-size:16px;white-space:pre}}
    .cursor{{animation:blink 1s steps(1) infinite}}
    @keyframes blink{{50%{{opacity:0}}}}
    .border{{stroke-dasharray:6 10;animation:march 1.2s linear infinite}}
    @keyframes march{{to{{stroke-dashoffset:-16}}}}
    {REDUCED}
  </style>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="12" fill="{BG}" stroke="{ACCENT}" stroke-opacity=".35"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="12" fill="none" stroke="{ACCENT}" stroke-opacity=".6" class="border"/>
  <path d="M1 40V13A12 12 0 0 1 13 1H{w - 13}A12 12 0 0 1 {w - 1} 13V40Z" fill="url(#bar)"/>
  <circle cx="26" cy="21" r="6" fill="{ACCENT}"/><circle cx="46" cy="21" r="6" fill="{ROSE}"/><circle cx="66" cy="21" r="6" fill="{WHITE}"/>
  <text x="{w / 2}" y="26" text-anchor="middle" fill="{DIM}" font-size="13" style="font-size:13px">analyst@soc-lab: ~/profile</text>
  {''.join(parts)}
  <text x="{left}" y="{top + lh * len(lines)}"><tspan fill="{WHITE}">❯ </tspan><tspan fill="{ACCENT}" class="cursor">█</tspan></text>
</svg>
"""
    write(f"terminal-{THEME}.svg", svg)


# --------------------------------------------------------------------------
# Investigation pipeline: packets flow between the four mindset stages.
# --------------------------------------------------------------------------
def pipeline():
    w, h = 1000, 200
    stages = [
        ("OBSERVE", "telemetry · logs"),
        ("CORRELATE", "SIEM · rules"),
        ("INVESTIGATE", "triage · evidence"),
        ("IMPROVE", "lessons · tuning"),
    ]
    cols = [WHITE, ROSE, ACCENT, CRIMSON]
    xs = [125 + i * 250 for i in range(4)]
    y = 92
    nodes, links = [], []
    for i, ((name, sub), x, col) in enumerate(zip(stages, xs, cols)):
        nodes.append(
            f'<g>'
            f'<circle cx="{x}" cy="{y}" r="44" fill="{PANEL}" stroke="{col}" stroke-width="2"/>'
            f'<circle cx="{x}" cy="{y}" r="44" fill="none" stroke="{col}" class="halo" style="animation-delay:{i * 0.75}s"/>'
            f'<circle cx="{x}" cy="{y}" r="34" fill="none" stroke="{col}" stroke-opacity=".35" stroke-dasharray="4 6" class="spin" style="animation-duration:{8 + i * 2}s"/>'
            f'<text x="{x}" y="{y + 7}" text-anchor="middle" font-size="20" fill="{WHITE}" font-weight="700">0{i + 1}</text>'
            f'<text x="{x}" y="{y + 72}" text-anchor="middle" font-size="15" fill="{TEXT}" letter-spacing="3" font-weight="700">{name}</text>'
            f'<text x="{x}" y="{y + 94}" text-anchor="middle" font-size="12" fill="{DIM}">{sub}</text>'
            "</g>"
        )
    for i in range(3):
        x1, x2 = xs[i] + 50, xs[i + 1] - 50
        links.append(
            f'<path id="p{i}" d="M{x1} {y}H{x2}" stroke="{ACCENT}" stroke-opacity=".3" stroke-width="2" stroke-dasharray="3 6"/>'
            f'<path d="M{x2 - 8} {y - 6}L{x2} {y}L{x2 - 8} {y + 6}" fill="none" stroke="{ACCENT}" stroke-opacity=".6" stroke-width="2"/>'
        )
        for k in range(2):
            links.append(
                f'<circle r="4" fill="{cols[i + 1]}" opacity="0">'
                f'<animateMotion dur="2.4s" begin="{i * 0.6 + k * 1.2:.1f}s" repeatCount="indefinite"><mpath href="#p{i}"/></animateMotion>'
                f'<animate attributeName="opacity" values="0;1;1;0" dur="2.4s" begin="{i * 0.6 + k * 1.2:.1f}s" repeatCount="indefinite"/>'
                "</circle>"
            )
    # feedback loop: IMPROVE back to OBSERVE
    loop = (
        f'<path id="back" d="M{xs[3]} {y - 46}C{xs[3]} {y - 92} {xs[0]} {y - 92} {xs[0]} {y - 46}" '
        f'fill="none" stroke="{ACCENT}" stroke-opacity=".35" stroke-width="1.5" stroke-dasharray="2 6"/>'
        f'<circle r="3.5" fill="{ACCENT}"><animateMotion dur="5s" repeatCount="indefinite"><mpath href="#back"/></animateMotion></circle>'
    )
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Analyst loop: observe, correlate, investigate, improve">
  <title>observe → correlate → investigate → improve</title>
  <style>
    text{{font-family:{MONO}}}
    .halo{{transform-box:fill-box;transform-origin:center;animation:halo 3s ease-out infinite}}
    @keyframes halo{{0%{{opacity:.8;transform:scale(1)}}100%{{opacity:0;transform:scale(1.45)}}}}
    .spin{{transform-box:fill-box;transform-origin:center;animation:spin linear infinite}}
    @keyframes spin{{to{{transform:rotate(360deg)}}}}
    {REDUCED}
  </style>
  <rect width="{w}" height="{h}" rx="12" fill="{BG}"/>
  {loop}
  {''.join(links)}
  {''.join(nodes)}
</svg>
"""
    write(f"pipeline-{THEME}.svg", svg)


# --------------------------------------------------------------------------
# Section divider: a data packet travelling along a circuit trace.
# --------------------------------------------------------------------------
def divider():
    w, h = 1000, 24
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="divider">
  <defs>
    <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{ACCENT}" stop-opacity=".55"/>
      <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="packet" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/>
      <stop offset=".7" stop-color="{ACCENT}"/>
      <stop offset="1" stop-color="{WHITE}"/>
    </linearGradient>
  </defs>
  <path d="M0 12H440L452 4H548L560 12H{w}" fill="none" stroke="url(#fade)" stroke-width="1.5"/>
  <text x="500" y="14" text-anchor="middle" font-family="{MONO}" font-size="9" fill="{ACCENT}" fill-opacity=".8" letter-spacing="2">◆ ◆ ◆</text>
  <rect y="10.5" width="90" height="3" rx="1.5" fill="url(#packet)">
    <animate attributeName="x" from="-90" to="{w}" dur="3.5s" repeatCount="indefinite"/>
  </rect>
</svg>
"""
    write(f"divider-{THEME}.svg", svg)


# --------------------------------------------------------------------------
# Footer: network heartbeat trace drawing itself across the panel.
# --------------------------------------------------------------------------
def footer():
    w, h = 1200, 130
    pts, x = [], 0
    while x <= w:
        if x % 300 == 140:
            pts += [f"{x} 70", f"{x + 10} 70", f"{x + 18} 30", f"{x + 28} 105", f"{x + 36} 55", f"{x + 44} 70"]
            x += 50
        else:
            pts.append(f"{x} 70")
            x += 10
    d = "M" + " L".join(pts)
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Network heartbeat">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{PANEL}"/>
    </linearGradient>
    <linearGradient id="beam" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CRIMSON}" stop-opacity=".15"/><stop offset=".75" stop-color="{ACCENT}"/><stop offset="1" stop-color="{WHITE}"/>
    </linearGradient>
  </defs>
  <style>
    .trace{{stroke-dasharray:1600 2400;animation:draw 4s linear infinite}}
    @keyframes draw{{from{{stroke-dashoffset:1600}}to{{stroke-dashoffset:-2400}}}}
    {REDUCED}
  </style>
  <rect width="{w}" height="{h}" fill="url(#bg)"/>
  <path d="{d}" fill="none" stroke="{ACCENT}" stroke-opacity=".12" stroke-width="2"/>
  <path d="{d}" fill="none" stroke="url(#beam)" stroke-width="2.5" stroke-linejoin="round" class="trace"/>
  <text x="{w / 2}" y="122" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{DIM}" letter-spacing="4">// END OF TRANSMISSION · STAY VIGILANT //</text>
</svg>
"""
    write(f"footer-{THEME}.svg", svg)


if __name__ == "__main__":
    hero()
    terminal()
    pipeline()
    divider()
    footer()
