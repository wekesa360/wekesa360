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
    ("cpims", "CPIMS", "Kenya's national child protection system.",
     ["flutter", "dart", "django", "postgresql"], "national · 1,000+ daily users"),
    ("pona", "Pona", "Private HD video consults for clinicians.",
     ["typescript", "webrtc", "react", "laravel"], "health · realtime"),
]

# title, short line, glyph
PRINCIPLES = [
    ("Build for the worst day", "Peak traffic, flaky networks.", "spike"),
    ("Latency is a feature", "Close to users, works offline.", "bolt"),
    ("Trust is built in", "Security from line one.", "shield"),
    ("Own the outcome", "Does it help the user?", "target"),
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
    ("2022 — 23", "Chapter Lead", "Google Developer Group, Kabarak"),
]

SECTIONS = [("01", "WORK"), ("02", "HOW I WORK"), ("03", "STACK"), ("04", "EXPERIENCE"), ("05", "GET IN TOUCH")]

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


def art_cpims(W, H):
    """A field worker's phone with a case list, for projects without a screenshot."""
    px, py, pw, ph = W / 2 - 70, 40, 140, 270
    rows = "".join(
        f'<rect x="{px + 16}" y="{py + 70 + i * 38}" width="{pw - 32}" height="28" rx="6" fill="{PANEL}" stroke="{LINE}"/>'
        f'<circle cx="{px + 30}" cy="{py + 84 + i * 38}" r="5" fill="{ORANGE if i == 0 else DIM}"/>'
        f'<rect x="{px + 42}" y="{py + 80 + i * 38}" width="{60 - i * 8}" height="4" rx="2" fill="{MUTED}"/>'
        f'<rect x="{px + 42}" y="{py + 88 + i * 38}" width="{36 + i * 5}" height="3" rx="1.5" fill="{DIM}"/>'
        for i in range(5)
    )
    side = "".join(
        f'<rect x="{x}" y="{y}" width="72" height="46" rx="8" fill="{PANEL}" stroke="{LINE}"/>'
        f'<rect x="{x + 10}" y="{y + 12}" width="{w}" height="5" rx="2.5" fill="{c}"/>'
        f'<rect x="{x + 10}" y="{y + 26}" width="38" height="4" rx="2" fill="{DIM}"/>'
        for x, y, w, c in [(56, 90, 44, ORANGE), (56, 170, 30, MUTED), (W - 128, 120, 50, MUTED), (W - 128, 200, 34, ORANGE)]
    )
    return f"""
{grid_pattern("gc", 24)}<rect width="{W}" height="{H}" fill="url(#gc)"/>
{side}
<path d="M100 113 H{px}" stroke="{LINE}" stroke-dasharray="3 4"/><path d="M{px + pw} 143 H{W - 128}" stroke="{LINE}" stroke-dasharray="3 4"/>
<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="22" fill="{BG}" stroke="#3a3a3a" stroke-width="2"/>
<rect x="{px + pw / 2 - 18}" y="{py + 10}" width="36" height="6" rx="3" fill="#2a2a2a"/>
<rect x="{px + 16}" y="{py + 32}" width="70" height="8" rx="4" fill="{WHITE}"/>
<rect x="{px + 16}" y="{py + 46}" width="44" height="4" rx="2" fill="{ORANGE}"/>
{rows}"""


def art_pona(W, H):
    """Two video tiles on a call, for projects without a screenshot."""
    def person(cx, cy, c):
        return (f'<circle cx="{cx}" cy="{cy - 22}" r="22" fill="{c}"/>'
                f'<path d="M{cx - 44} {cy + 44} a44 40 0 0 1 88 0 z" fill="{c}"/>')
    tw, th, y = 180, 150, 56
    x1, x2 = W / 2 - tw - 10, W / 2 + 10
    return f"""
{grid_pattern("gp", 24)}<rect width="{W}" height="{H}" fill="url(#gp)"/>
<clipPath id="t1"><rect x="{x1}" y="{y}" width="{tw}" height="{th}" rx="12"/></clipPath>
<clipPath id="t2"><rect x="{x2}" y="{y}" width="{tw}" height="{th}" rx="12"/></clipPath>
<rect x="{x1}" y="{y}" width="{tw}" height="{th}" rx="12" fill="{PANEL}" stroke="{LINE}"/>
<g clip-path="url(#t1)">{person(x1 + tw / 2, y + 86, "#2a2a2a")}</g>
<rect x="{x2}" y="{y}" width="{tw}" height="{th}" rx="12" fill="{PANEL}" stroke="{ORANGE}" stroke-width="1.5"/>
<g clip-path="url(#t2)">{person(x2 + tw / 2, y + 86, "#3a2418")}</g>
<rect x="{x1 + 10}" y="{y + 10}" width="38" height="16" rx="4" fill="{BG}"/><circle cx="{x1 + 20}" cy="{y + 18}" r="3" fill="{ORANGE}"/>
<text x="{x1 + 27}" y="{y + 22}" class="mono" font-size="9" fill="{MUTED}">HD</text>
<g transform="translate({W / 2 - 78} {y + th + 26})">
  <rect width="156" height="40" rx="20" fill="{PANEL}" stroke="{LINE}"/>
  <circle cx="34" cy="20" r="12" fill="#2a2a2a"/><circle cx="78" cy="20" r="12" fill="#2a2a2a"/>
  <circle cx="122" cy="20" r="12" fill="{ORANGE}"/>
  <path d="M116 20h12" stroke="{BG}" stroke-width="2.5" stroke-linecap="round"/>
  <rect x="29" y="13" width="10" height="14" rx="5" fill="none" stroke="{ICON}" stroke-width="1.5"/>
  <rect x="71" y="15" width="11" height="10" rx="2" fill="none" stroke="{ICON}" stroke-width="1.5"/><path d="M82 18l4-2v8l-4-2" fill="none" stroke="{ICON}" stroke-width="1.5"/>
</g>"""


ART = {"cpims": art_cpims, "pona": art_pona}


def art(slug, W, H):
    if slug in ART:
        return ART[slug](W, H)
    return f'<image href="{screenshot(slug)}" width="{W}" height="{H}" preserveAspectRatio="xMidYMin slice"/>'


def glyph(kind, x, y):
    """28px line glyphs for the principle tiles."""
    st = f'fill="none" stroke="{ORANGE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    shapes = {
        "spike": f'<path d="M0 20 h7 l4 -14 l5 22 l4 -8 h8" {st}/>',
        "bolt": f'<path d="M16 2 L5 16 h8 l-2 10 L22 12 h-8 z" {st}/>',
        "shield": f'<path d="M14 2 L25 6 v8 c0 7 -5 11 -11 13 c-6 -2 -11 -6 -11 -13 v-8 z" {st}/><path d="M9 14 l4 4 l6 -7" {st}/>',
        "target": f'<circle cx="14" cy="14" r="12" {st}/><circle cx="14" cy="14" r="6" {st}/><circle cx="14" cy="14" r="1.8" fill="{ORANGE}"/>',
    }
    return f'<g transform="translate({x} {y})">{shapes[kind]}</g>'


def principles():
    W, H, gap = 1000, 150, 16
    tw = (W - 3 * gap) / 4
    tiles = "".join(f"""
<g class="fade" style="animation-delay:{.1 + i * .1}s">
<rect x="{i * (tw + gap) + .5}" y=".5" width="{tw - 1}" height="{H - 1}" rx="14" fill="{PANEL}" stroke="{LINE}"/>
{glyph(g, i * (tw + gap) + 22, 24)}
<text x="{i * (tw + gap) + 22}" y="96" class="sans" font-size="16" font-weight="700" fill="{WHITE}">{esc(t)}</text>
<text x="{i * (tw + gap) + 22}" y="120" class="sans" font-size="13" fill="{MUTED}">{esc(d)}</text>
</g>""" for i, (t, d, g) in enumerate(PRINCIPLES))
    return svg(W, H, tiles, "", "How I work: " + ", ".join(t for t, _, _ in PRINCIPLES))


def contact():
    W, H = 1000, 130
    body = f"""
{grid_pattern("gk")}
<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#gk)"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{LINE}"/>
<text x="52" y="64" class="sans" font-size="30" font-weight="800" letter-spacing="-1" fill="{WHITE}">Tell me what you're <tspan fill="{ORANGE}">building.</tspan></text>
<text x="52" y="94" class="sans" font-size="14.5" fill="{MUTED}">Open to full-time, contract and consulting work.</text>
{mark(W - 76, 34, 18)}
<rect x="{W - 104}" y="62" width="18" height="18" rx="2" fill="none" stroke="{ORANGE}" stroke-opacity=".5"/>
<rect x="{W - 132}" y="90" width="18" height="18" rx="2" fill="none" stroke="{ORANGE}" stroke-opacity=".25"/>
"""
    return svg(W, H, body, "", "Tell me what you're building.")


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
  {art(slug, W, IH)}
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
    files = {"header.svg": header(), "stack.svg": stack(), "experience.svg": experience(),
             "principles.svg": principles(), "contact.svg": contact()}
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
