#!/usr/bin/env python3
"""Generate the SVG assets for the GitHub profile README.

Run from the repo root:  python3 scripts/generate.py   (needs Pillow)
Edit the CONTENT section and re-run. Logos in scripts/icons/ come from
Simple Icons (CC0); screenshots in scripts/previews/ are from the portfolio.
"""

import base64
import io
import math
import re
from html import escape
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "assets"

BG = "#0d0d0d"
PANEL = "#141414"
LINE = "#232323"
GRID = "#161616"
ORANGE = "#FF4D00"
WHITE = "#f5f5f5"
MUTED = "#8a8a8a"
DIM = "#5c5c5c"
ICON = "#cfcfcf"

SANS = "Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

BASE_CSS = f"""
  .sans {{ font-family: {SANS}; }}
  .mono {{ font-family: {MONO}; }}
  .fade {{ animation: fade .8s cubic-bezier(.22,1,.36,1) both; }}
  @keyframes fade {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
"""

# ---------------------------------------------------------------- CONTENT
STATS = [("4+", "YEARS"), ("1,000+", "DAILY USERS"), ("<200ms", "P95 GLOBAL")]

# slug, name, one line, icons, footer
PROJECTS = [
    ("qura", "Qura", "Elections you can vote in over USSD.",
     ["typescript", "react"], "qura.co.ke"),
    ("zaria", "Zaria", "Skill diagnostics and training for teams.",
     ["react", "typescript", "sqlite"], "pds-landing.pages.dev"),
    ("ploracs", "Ploracs", "Offline-first wellness app on the edge.",
     ["flutter", "dart", "hono", "cloudflareworkers", "sqlite"], "ploracs.com"),
    ("csms", "Nakuru CSMS", "Official statistics for Nakuru County.",
     ["django", "postgresql", "react", "celery"], "statistics.nakuru.go.ke"),
    ("clarivue", "Clarivue", "Messy data in, auditable decisions out.",
     ["react", "typescript"], "clarivue.duckdns.org"),
    ("elimisha", "Elimisha", "Donations and members, handled in-house.",
     ["react", "typescript", "vite"], "elimishacharity.org"),
]

STACK = [
    ("react", "React"), ("typescript", "TypeScript"), ("flutter", "Flutter"), ("dart", "Dart"),
    ("python", "Python"), ("django", "Django"), ("nodedotjs", "Node"), ("laravel", "Laravel"),
    ("postgresql", "Postgres"), ("celery", "Celery"), ("hono", "Hono"), ("googlegemini", "Gemini"),
    ("cloudflare", "Cloudflare"), ("amazonwebservices", "AWS"), ("docker", "Docker"), ("githubactions", "CI/CD"),
]

EXPERIENCE = [
    ("2026 —", "Consultant", "County Government of Nakuru"),
    ("2025 — 26", "Full-Stack Engineer", "GoWriters Publishers"),
    ("2025", "Consultant", "Ministry of Health · KMHFR"),
    ("2024 — 25", "Software Engineer", "Pona"),
    ("2022 — 24", "Lead Developer, EVIS", "Kabarak University"),
]

SECTIONS = [("01", "WORK"), ("02", "STACK"), ("03", "EXPERIENCE")]

BUTTONS = [
    ("portfolio", "Portfolio", "mark", True),
    ("linkedin", "LinkedIn", "linkedin", False),
    ("resume", "Resume", "doc", False),
]


# ---------------------------------------------------------------- helpers
def esc(s):
    return escape(s, quote=True)


def svg(w, h, body, css="", title=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{esc(title)}">\n<title>{esc(title)}</title>\n'
        f"<style>{BASE_CSS}{css}</style>\n{body}\n</svg>\n"
    )


def icon_path(slug):
    src = (ROOT / "icons" / f"{slug}.svg").read_text()
    return re.search(r'<path d="([^"]+)"', src).group(1)


def icon(slug, x, y, size, fill=ICON):
    s = size / 24
    return f'<path transform="translate({x} {y}) scale({s})" d="{icon_path(slug)}" fill="{fill}"/>'


def screenshot(slug, width=960):
    im = Image.open(ROOT / "previews" / f"{slug}.webp").convert("RGB")
    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=72, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def mark(x, y, s=18):
    return f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="2" fill="{ORANGE}"/>'


def grid_pattern(pid, size=32):
    return (
        f'<defs><pattern id="{pid}" width="{size}" height="{size}" patternUnits="userSpaceOnUse">'
        f'<path d="M {size} 0 L 0 0 0 {size}" fill="none" stroke="{GRID}"/></pattern></defs>'
    )


# ---------------------------------------------------------------- builders
def header():
    W, H = 1000, 300
    pts, x = [], 0
    while x <= W:
        y = 214 + math.sin(x / 23) * 3 + math.sin(x / 7) * 1.5
        if 700 < x < 740:
            y -= (1 - abs(x - 720) / 20) * 40
        pts.append(f"{x},{y:.1f}")
        x += 4
    stats = "".join(
        f'<g class="fade" style="animation-delay:{1.2 + i * .15}s">'
        f'<text x="{64 + i * 170}" y="266" class="sans" font-size="22" font-weight="700" fill="{WHITE}">{esc(v)}</text>'
        f'<text x="{64 + i * 170}" y="284" class="mono" font-size="10" letter-spacing="1.5" fill="{DIM}">{esc(k)}</text></g>'
        for i, (v, k) in enumerate(STATS)
    )
    css = """
      .trace { stroke-dasharray: 2200; stroke-dashoffset: 2200; animation: draw 2.6s ease-out .5s forwards; }
      @keyframes draw { to { stroke-dashoffset: 0; } }
      @media (prefers-reduced-motion: reduce) { .trace { stroke-dashoffset: 0; } }
    """
    body = f"""
{grid_pattern("g")}
<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#g)"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{LINE}"/>
{mark(64, 46)}
<text x="94" y="60" class="mono" font-size="13" fill="{MUTED}">wekesa360</text>
<text x="{W - 64}" y="60" text-anchor="end" class="mono" font-size="12" fill="{DIM}">Kenya</text>
<text x="64" y="134" class="sans fade" style="animation-delay:.1s" font-size="60" font-weight="800" letter-spacing="-2" fill="{WHITE}">Michael Wekesa</text>
<text x="64" y="176" class="sans fade" style="animation-delay:.3s" font-size="26" font-weight="700" letter-spacing="-.5" fill="{WHITE}">Software Engineer. <tspan fill="{ORANGE}">Systems Built to Last.</tspan></text>
<polyline class="trace" points="{' '.join(pts)}" fill="none" stroke="{ORANGE}" stroke-width="1.6" stroke-opacity=".85"/>
<line x1="64" y1="236" x2="{W - 64}" y2="236" stroke="{LINE}"/>
{stats}
"""
    return svg(W, H, body, css, "Michael Wekesa, Software Engineer")


def section(num, title):
    W, H = 1000, 56
    tw = len(title) * 11 + 110
    body = f"""
<text x="0" y="36" class="mono" font-size="14" fill="{ORANGE}">{num}</text>
<text x="34" y="36" class="sans" font-size="15" font-weight="700" letter-spacing="3" fill="#8b949e">{esc(title)}</text>
<line x1="{tw}" y1="31" x2="{W - 16}" y2="31" stroke="#8b949e" stroke-opacity=".35"/>
<rect x="{W - 8}" y="27" width="8" height="8" rx="1" fill="{ORANGE}"/>
"""
    return svg(W, H, body, "", f"{num} {title}")


def project(slug, name, line, icons, foot):
    W, IH = 488, 290
    H = IH + 118
    icons_svg = "".join(icon(s, 24 + i * 30, H - 40, 18) for i, s in enumerate(icons))
    body = f"""
<defs>
  <clipPath id="c{slug}"><rect width="{W}" height="{H}" rx="16"/></clipPath>
  <linearGradient id="f{slug}" x1="0" y1="0" x2="0" y2="1">
    <stop offset=".55" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}"/>
  </linearGradient>
</defs>
<g clip-path="url(#c{slug})">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <image href="{screenshot(slug)}" width="{W}" height="{IH}" preserveAspectRatio="xMidYMin slice"/>
  <rect width="{W}" height="{IH}" fill="url(#f{slug})"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{LINE}"/>
<text x="24" y="{IH + 20}" class="sans" font-size="22" font-weight="700" letter-spacing="-.3" fill="{WHITE}">{esc(name)}</text>
<text x="{W - 24}" y="{IH + 20}" text-anchor="end" class="sans" font-size="18" fill="{ORANGE}">↗</text>
<text x="24" y="{IH + 46}" class="sans" font-size="14.5" fill="{MUTED}">{esc(line)}</text>
{icons_svg}
<text x="{W - 24}" y="{H - 26}" text-anchor="end" class="mono" font-size="11" fill="{DIM}">{esc(foot)}</text>
"""
    return svg(W, H, body, "", f"{name}: {line}")


def stack():
    cols, tw, th, gap = 8, 112, 104, 13
    rows = math.ceil(len(STACK) / cols)
    W, H = 1000, rows * th + (rows - 1) * gap
    tiles = []
    for i, (slug, label) in enumerate(STACK):
        x = (i % cols) * (tw + gap) + 4
        y = (i // cols) * (th + gap)
        tiles.append(f"""
<g class="fade" style="animation-delay:{.05 * i:.2f}s">
<rect x="{x + .5}" y="{y + .5}" width="{tw - 1}" height="{th - 1}" rx="14" fill="{PANEL}" stroke="{LINE}"/>
{icon(slug, x + tw / 2 - 16, y + 22, 32)}
<text x="{x + tw / 2}" y="{y + 84}" text-anchor="middle" class="mono" font-size="11.5" fill="{MUTED}">{esc(label)}</text>
</g>""")
    return svg(W, H, "".join(tiles), "", "Stack: " + ", ".join(l for _, l in STACK))


def experience():
    row = 58
    W, H = 1000, 34 + row * len(EXPERIENCE)
    items = []
    for i, (period, role, org) in enumerate(EXPERIENCE):
        y = 44 + i * row
        current = i == 0
        node = (f'<circle cx="36" cy="{y - 5}" r="10" fill="{ORANGE}" opacity=".22"/>'
                f'<circle cx="36" cy="{y - 5}" r="5" fill="{ORANGE}"/>' if current else
                f'<circle cx="36" cy="{y - 5}" r="5" fill="{BG}" stroke="{ORANGE}" stroke-width="1.5"/>')
        items.append(f"""
<g class="fade" style="animation-delay:{.1 + i * .1}s">
{node}
<text x="68" y="{y}" class="mono" font-size="12" letter-spacing="1" fill="{ORANGE if current else DIM}">{esc(period)}</text>
<text x="200" y="{y}" class="sans" font-size="17" font-weight="700" fill="{WHITE}">{esc(role)}</text>
<text x="{W - 32}" y="{y}" text-anchor="end" class="sans" font-size="14" fill="{MUTED}">{esc(org)}</text>
</g>""")
    body = f"""
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{BG}" stroke="{LINE}"/>
<line x1="36" y1="39" x2="36" y2="{44 + row * (len(EXPERIENCE) - 1) - 5}" stroke="{LINE}" stroke-width="1.5"/>
{''.join(items)}
"""
    return svg(W, H, body, "", "Experience")


def button(label, glyph, primary):
    W, H = 164, 46
    fg = BG if primary else WHITE
    if glyph == "mark":
        g = f'<rect x="22" y="16" width="14" height="14" rx="2" fill="{fg}"/>'
    elif glyph == "doc":
        g = (f'<path d="M22 13h10l5 5v15H22z" fill="none" stroke="{fg}" stroke-width="1.6" stroke-linejoin="round"/>'
             f'<path d="M26 22h7M26 26h7" stroke="{fg}" stroke-width="1.6"/>')
    else:
        g = icon(glyph, 21, 14, 18, fg)
    body = f"""
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="10" fill="{ORANGE if primary else BG}" stroke="{ORANGE if primary else '#3a3a3a'}" stroke-width="1.5"/>
{g}
<text x="50" y="28.5" class="sans" font-size="15" font-weight="600" fill="{fg}">{esc(label)}</text>
"""
    return svg(W, H, body, "", label)


def main():
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    files = {"header.svg": header(), "stack.svg": stack(), "experience.svg": experience()}
    for num, title in SECTIONS:
        files[f"section-{num}.svg"] = section(num, title)
    for p in PROJECTS:
        files[f"project-{p[0]}.svg"] = project(*p)
    for slug, label, glyph, primary in BUTTONS:
        files[f"btn-{slug}.svg"] = button(label, glyph, primary)
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
    print(f"wrote {len(files)} files to {OUT}")


if __name__ == "__main__":
    main()
