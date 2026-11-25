#!/usr/bin/env python3
"""Generate the SVG assets for the GitHub profile README.

Run from the repo root:  python3 scripts/generate.py
All content lives in the CONTENT section below; edit it and re-run.
"""

from pathlib import Path
from textwrap import wrap
from html import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

# ---------------------------------------------------------------- theme
BG = "#0d0d0d"
PANEL = "#141414"
LINE = "#232323"
GRID = "#161616"
ORANGE = "#FF4D00"
ORANGE_SOFT = "#ff6a26"
WHITE = "#f5f5f5"
MUTED = "#8a8a8a"
DIM = "#5c5c5c"

SANS = "Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

BASE_CSS = f"""
  .sans {{ font-family: {SANS}; }}
  .mono {{ font-family: {MONO}; }}
  .fade {{ animation: fade .8s cubic-bezier(.22,1,.36,1) both; }}
  @keyframes fade {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
  @keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .25; }} }}
  @media (prefers-reduced-motion: reduce) {{
    * {{ animation: none !important; opacity: 1 !important; transform: none !important; stroke-dashoffset: 0 !important; }}
  }}
"""


def esc(s: str) -> str:
    return escape(s, quote=True)


def svg(w: int, h: int, body: str, css: str = "", title: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">\n'
        f"<title>{esc(title)}</title>\n<style>{BASE_CSS}{css}</style>\n{body}\n</svg>\n"
    )


def grid_pattern(pid: str, size: int = 32) -> str:
    return (
        f'<defs><pattern id="{pid}" width="{size}" height="{size}" patternUnits="userSpaceOnUse">'
        f'<path d="M {size} 0 L 0 0 0 {size}" fill="none" stroke="{GRID}" stroke-width="1"/>'
        f"</pattern></defs>"
    )


def lines(x, y, text, width, size, fill, cls="sans", lh=1.5, weight=400, delay=None):
    out = []
    style = f' style="animation-delay:{delay}s"' if delay is not None else ""
    fade = " fade" if delay is not None else ""
    for i, ln in enumerate(wrap(text, width)):
        out.append(
            f'<text x="{x}" y="{y + i * size * lh:.1f}" class="{cls}{fade}"{style} '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}">{esc(ln)}</text>'
        )
    return "\n".join(out), len(wrap(text, width))


def pills(x, y, tags, size=12, gap=8, max_x=None):
    out, cx = [], x
    for t in tags:
        w = int(len(t) * size * 0.62) + 20
        if max_x and cx + w > max_x:
            break
        out.append(
            f'<rect x="{cx}" y="{y}" width="{w}" height="24" rx="12" fill="none" stroke="{LINE}"/>'
            f'<text x="{cx + w / 2}" y="{y + 16}" text-anchor="middle" class="mono" '
            f'font-size="{size}" fill="{MUTED}">{esc(t)}</text>'
        )
        cx += w + gap
    return "\n".join(out)


def mark(x, y, s=18):
    return f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="2" fill="{ORANGE}"/>'


# ---------------------------------------------------------------- CONTENT
STATS = [("4+", "YEARS IN PRODUCTION"), ("1,000+", "DAILY USERS SERVED"), ("p95 <200ms", "GLOBAL LATENCY")]

PRINCIPLES = [
    ("Build for the worst day",
     "Systems earn trust on their busiest, messiest day: peak traffic, flaky networks, a dependency that goes down."),
    ("Latency is a feature",
     "Users feel every round trip. Moving work closer to them, and letting apps keep working offline, often matters most."),
    ("Trust is built in",
     "When the data belongs to real people, security and accountability are requirements from the first line of code."),
    ("Own the outcome",
     "Code is only the means. I care whether the people using what I build can actually get their job done better."),
]

PROJECTS = [
    ("qura", "Qura Election Platform", "WEB · USSD",
     "Runs student, SACCO and board elections end to end. Vote in under a minute from any phone, on the web or over USSD with no internet, with receipts verifiable against a tamper-evident audit trail.",
     ["TypeScript", "React", "USSD"], "qura.co.ke"),
    ("zaria", "Zaria Professional", "WEB · AI",
     "Five-minute skill diagnostics per team, programs built from an organisation's own playbooks, an AI study companion, and verifiable certificates. Privacy designed in from day one.",
     ["React", "TypeScript", "SQLite", "AI"], "pds-landing.pages.dev"),
    ("ploracs", "Ploracs Wellness App", "MOBILE · EDGE",
     "Cross-platform wellness app with a Flutter client and a Hono.js backend on Cloudflare Workers. Offline-first sync, and p95 latency held under 200ms for users worldwide.",
     ["Flutter", "Dart", "Hono.js", "D1"], "ploracs.com"),
    ("csms", "County Statistical Management System", "PUBLIC SECTOR",
     "Collection, validation and publication of official statistics for Nakuru County, with workflow approvals, audit trails, automated reports and a public access portal.",
     ["Django", "PostGIS", "React", "Celery"], "statistics.nakuru.go.ke"),
    ("cpims", "CPIMS: Kenya Child Protection", "PUBLIC SECTOR · MOBILE",
     "Kenya's national case management system for child protection. Helped launch the Flutter Android client that took it to social workers in the field, serving 1,000+ daily users.",
     ["Flutter", "Django", "PostgreSQL"], "national infrastructure"),
    ("pona", "Pona WebRTC Platform", "HEALTH · REALTIME",
     "Custom WebRTC media server in TypeScript for secure HD consultations between patients and clinicians, with signalling, peer negotiation and ephemeral session chat.",
     ["TypeScript", "WebRTC", "React", "Laravel"], "healthcare"),
]

TOOLKIT = [
    ("Interfaces & apps", "Interfaces people can actually use, on whatever screen they are holding.",
     ["React", "TypeScript", "Flutter"]),
    ("Backends & APIs", "Clear contracts, boring reliability, and data models that age well.",
     ["Python", "Django", "Node", "Laravel"]),
    ("Infrastructure", "Ship often, ship safely, and run close to the people using it.",
     ["Cloudflare", "AWS", "Docker", "CI/CD"]),
    ("Data, AI & Automation", "Trustworthy data first, and AI only where it genuinely earns its place.",
     ["PostgreSQL", "PostGIS", "Celery", "LLMs"]),
]

EXPERIENCE = [
    ("MAR 2026 — NOW", "Software Engineering Consultant", "County Government of Nakuru"),
    ("OCT 2025 — MAR 2026", "Full-Stack Software Engineer", "GoWriters Publishers · Remote"),
    ("AUG 2025", "Software Engineering Consultant", "Kenya Ministry of Health · KMHFR"),
    ("JUN 2024 — JUL 2025", "Software Engineer", "Pona"),
    ("JUL 2022 — SEP 2024", "Lead Developer, EVIS", "Kabarak University · Incubation Center"),
    ("2022 — 2023", "Chapter Lead & Core Team Lead", "Google Developer Group on Campus, Kabarak"),
]

SECTIONS = [("01", "PRINCIPLES"), ("02", "SELECTED WORK"), ("03", "TOOLKIT"), ("04", "EXPERIENCE"), ("05", "GET IN TOUCH")]

BUTTONS = [("portfolio", "PORTFOLIO", True), ("linkedin", "LINKEDIN", False), ("resume", "RESUME ↓", False)]


# ---------------------------------------------------------------- builders
def header():
    W, H = 1000, 380
    # heartbeat / latency trace across the bottom
    pts, x = [], 0
    import math
    while x <= W:
        y = 300 + math.sin(x / 23) * 3 + math.sin(x / 7) * 1.5
        if 560 < x < 600:  # a single spike: the "worst day", absorbed
            y -= (1 - abs(x - 580) / 20) * 46
        pts.append(f"{x},{y:.1f}")
        x += 4
    trace = " ".join(pts)

    stats = []
    for i, (v, label) in enumerate(STATS):
        sx = 64 + i * 210
        stats.append(
            f'<g class="fade" style="animation-delay:{1.4 + i * .15}s">'
            f'<text x="{sx}" y="346" class="sans" font-size="22" font-weight="700" fill="{WHITE}">{esc(v)}</text>'
            f'<text x="{sx}" y="364" class="mono" font-size="10" letter-spacing="1.5" fill="{DIM}">{esc(label)}</text></g>'
        )

    css = f"""
      .trace {{ stroke-dasharray: 2200; stroke-dashoffset: 2200; animation: draw 3s ease-out .6s forwards; }}
      @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
      .dot {{ animation: pulse 2s ease-in-out infinite; }}
      .caret {{ animation: pulse 1s steps(1) infinite; }}
    """
    body = f"""
{grid_pattern("g")}
<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#g)"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{LINE}"/>

{mark(64, 44)}
<text x="94" y="58" class="mono" font-size="13" fill="{MUTED}">wekesa360</text>
<circle cx="{W - 190}" cy="53" r="4" fill="{ORANGE}" class="dot"/>
<text x="{W - 178}" y="58" class="mono" font-size="12" fill="{MUTED}">available · Kenya</text>

<text x="64" y="150" class="sans fade" style="animation-delay:.1s" font-size="64" font-weight="800" letter-spacing="-2" fill="{WHITE}">Michael Wekesa</text>
<text x="64" y="200" class="sans fade" style="animation-delay:.35s" font-size="30" font-weight="700" letter-spacing="-.5" fill="{WHITE}">Software Engineer. <tspan fill="{ORANGE}">Systems Built to Last.</tspan></text>
<text x="64" y="236" class="mono fade" style="animation-delay:.6s" font-size="14" fill="{MUTED}">$ full-stack products, from the data model to the app in people's hands<tspan class="caret" fill="{ORANGE}"> ▍</tspan></text>

<polyline class="trace" points="{trace}" fill="none" stroke="{ORANGE}" stroke-width="1.6" stroke-opacity=".9"/>
<text x="606" y="262" class="mono fade" style="animation-delay:2.4s" font-size="10" fill="{ORANGE_SOFT}">peak load · absorbed</text>
<line x1="64" y1="318" x2="{W - 64}" y2="318" stroke="{LINE}"/>
{''.join(stats)}
"""
    return svg(W, H, body, css, "Michael Wekesa — Software Engineer. Systems Built to Last.")


def section(num, title):
    W, H = 1000, 56
    tw = len(title) * 11 + 110
    # Transparent background: mid-grey title and rule read on both GitHub themes.
    body = f"""
<text x="0" y="36" class="mono" font-size="14" fill="{ORANGE}">{num}</text>
<text x="34" y="36" class="sans t" font-size="15" font-weight="700" letter-spacing="3">{esc(title)}</text>
<line x1="{tw}" y1="31" x2="{W - 16}" y2="31" class="rule"/>
<rect x="{W - 8}" y="27" width="8" height="8" rx="1" fill="{ORANGE}"/>
"""
    css = """
      .t { fill: #8b949e; }
      .rule { stroke: #8b949e; stroke-opacity: .35; }
    """
    return svg(W, H, body, css, f"{num} {title}")


def principles():
    W, H = 1000, 300
    cw, ch, gap = 488, 138, 24
    cells = []
    for i, (t, d) in enumerate(PRINCIPLES):
        x = (i % 2) * (cw + gap)
        y = (i // 2) * (ch + gap)
        text, _ = lines(x + 28, y + 82, d, 62, 14, MUTED)
        cells.append(f"""
<g class="fade" style="animation-delay:{.1 + i * .12}s">
<rect x="{x + .5}" y="{y + .5}" width="{cw - 1}" height="{ch - 1}" rx="14" fill="{PANEL}" stroke="{LINE}"/>
<text x="{x + 28}" y="{y + 40}" class="mono" font-size="12" fill="{ORANGE}">0{i + 1}</text>
<text x="{x + 60}" y="{y + 41}" class="sans" font-size="19" font-weight="700" fill="{WHITE}">{esc(t)}</text>
{text}
</g>""")
    return svg(W, H, "".join(cells), "", "Engineering principles")


def project(slug, name, kind, desc, tags, foot):
    W, H = 488, 270
    text, _ = lines(28, 112, desc, 58, 13.5, MUTED, lh=1.55)
    title_size = 21 if len(name) < 30 else 18
    css = f"""
      .arrow {{ animation: nudge 2.4s ease-in-out infinite; }}
      @keyframes nudge {{ 0%,100% {{ transform: translate(0,0); }} 50% {{ transform: translate(3px,-3px); }} }}
      .bar {{ transform-origin: left; transform: scaleX(0); animation: grow 1.2s cubic-bezier(.22,1,.36,1) .2s forwards; }}
      @keyframes grow {{ to {{ transform: scaleX(1); }} }}
    """
    body = f"""
{grid_pattern("p" + slug, 24)}
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{BG}" stroke="{LINE}"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#p{slug})" opacity=".6"/>
<rect x="28" y="1" width="64" height="3" fill="{ORANGE}" class="bar"/>
<text x="28" y="44" class="mono" font-size="11" letter-spacing="1.5" fill="{ORANGE}">{esc(kind)}</text>
<g class="arrow"><text x="{W - 28}" y="46" text-anchor="end" class="sans" font-size="20" fill="{DIM}">↗</text></g>
<text x="28" y="80" class="sans" font-size="{title_size}" font-weight="700" letter-spacing="-.3" fill="{WHITE}">{esc(name)}</text>
{text}
{pills(28, 200, tags, max_x=W - 28)}
<text x="28" y="252" class="mono" font-size="11" fill="{DIM}">{esc(foot)}</text>
"""
    return svg(W, H, body, css, name)


def toolkit():
    W, H = 1000, 250
    cw, gap = 232, 24
    cols = []
    for i, (t, p, tools) in enumerate(TOOLKIT):
        x = i * (cw + gap)
        text, _ = lines(x + 22, 92, p, 30, 13, MUTED)
        chips = "".join(
            f'<rect x="{x + 22 + (j % 2) * 96}" y="{168 + (j // 2) * 32}" width="88" height="24" rx="6" fill="{BG}" stroke="{LINE}"/>'
            f'<text x="{x + 66 + (j % 2) * 96}" y="{184 + (j // 2) * 32}" text-anchor="middle" class="mono" font-size="11.5" fill="{WHITE}">{esc(tool)}</text>'
            for j, tool in enumerate(tools)
        )
        cols.append(f"""
<g class="fade" style="animation-delay:{.1 + i * .12}s">
<rect x="{x + .5}" y=".5" width="{cw - 1}" height="{H - 1}" rx="14" fill="{PANEL}" stroke="{LINE}"/>
{mark(x + 22, 26, 10)}
<text x="{x + 22}" y="66" class="sans" font-size="16" font-weight="700" fill="{WHITE}">{esc(t)}</text>
{text}
{chips}
</g>""")
    return svg(W, H, "".join(cols), "", "Toolkit")


def experience():
    row = 64
    W, H = 1000, 40 + row * len(EXPERIENCE)
    items = []
    for i, (period, role, org) in enumerate(EXPERIENCE):
        y = 44 + i * row
        current = i == 0
        node = (
            f'<circle cx="36" cy="{y - 5}" r="9" fill="{ORANGE}" opacity=".25" class="halo"/>'
            f'<circle cx="36" cy="{y - 5}" r="5" fill="{ORANGE}"/>'
            if current else
            f'<circle cx="36" cy="{y - 5}" r="5" fill="{BG}" stroke="{ORANGE}" stroke-width="1.5"/>'
        )
        items.append(f"""
<g class="fade" style="animation-delay:{.1 + i * .1}s">
{node}
<text x="68" y="{y}" class="mono" font-size="12" letter-spacing="1" fill="{ORANGE if current else DIM}">{esc(period)}</text>
<text x="300" y="{y}" class="sans" font-size="17" font-weight="700" fill="{WHITE}">{esc(role)}</text>
<text x="300" y="{y + 20}" class="sans" font-size="13" fill="{MUTED}">{esc(org)}</text>
</g>""")
    css = """
      .halo { animation: pulse 2s ease-in-out infinite; }
    """
    body = f"""
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{BG}" stroke="{LINE}"/>
<line x1="36" y1="39" x2="36" y2="{44 + row * (len(EXPERIENCE) - 1) - 5}" stroke="{LINE}" stroke-width="1.5"/>
{''.join(items)}
"""
    return svg(W, H, body, css, "Experience")


def contact():
    W, H = 1000, 170
    body = f"""
{grid_pattern("c")}
<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#c)"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{LINE}"/>
<text x="56" y="76" class="sans" font-size="32" font-weight="800" letter-spacing="-1" fill="{WHITE}">Tell me what you're <tspan fill="{ORANGE}">building.</tspan></text>
<text x="56" y="112" class="sans" font-size="15" fill="{MUTED}">Open to full-time, contract, and consulting work. I'll get back to you promptly.</text>
{mark(W - 74, 56, 18)}
<rect x="{W - 102}" y="84" width="18" height="18" rx="2" fill="none" stroke="{ORANGE}" stroke-opacity=".5"/>
<rect x="{W - 130}" y="112" width="18" height="18" rx="2" fill="none" stroke="{ORANGE}" stroke-opacity=".25"/>
"""
    return svg(W, H, body, "", "Get in touch")


def button(label, primary):
    W, H = 160, 44
    fill = ORANGE if primary else BG
    stroke = ORANGE if primary else "#3a3a3a"
    color = "#0d0d0d" if primary else WHITE
    body = f"""
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>
<text x="{W / 2}" y="27" text-anchor="middle" class="mono" font-size="12.5" font-weight="700" letter-spacing="2" fill="{color}">{esc(label)}</text>
"""
    return svg(W, H, body, "", label)


def main():
    OUT.mkdir(exist_ok=True)
    files = {"header.svg": header(), "principles.svg": principles(), "toolkit.svg": toolkit(),
             "experience.svg": experience(), "contact.svg": contact()}
    for num, title in SECTIONS:
        files[f"section-{num}.svg"] = section(num, title)
    for p in PROJECTS:
        files[f"project-{p[0]}.svg"] = project(*p)
    for slug, label, primary in BUTTONS:
        files[f"btn-{slug}.svg"] = button(label, primary)
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
    print(f"wrote {len(files)} files to {OUT}")


if __name__ == "__main__":
    main()
