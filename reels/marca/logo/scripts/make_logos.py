"""Genera los SVG del logo de Morishita con texto convertido a trazos.
Geometría del horizontal = la del header de la web (index.html, svg.logo-svg viewBox 0 0 360 72)."""
import sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FONTS = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
ZEN = TTFont(FONTS / "zen-antique-soft/ZenAntiqueSoft-Regular.ttf")
MONO = TTFont(FONTS / "dm-mono/DMMono-Regular.ttf")

def run(font, text, size, x, y, spacing=0.0):
    """Devuelve (path_d, ancho_visual, bbox) de un texto en línea base y, empezando en x.
    letter-spacing como en CSS/SVG (se suma después de cada carácter)."""
    gs = font.getGlyphSet(); cmap = font.getBestCmap(); upm = font["head"].unitsPerEm
    s = size / upm
    pen = SVGPathPen(gs, ntos=lambda v: (f"{v:.2f}").rstrip("0").rstrip("."))
    bpen = BoundsPen(gs)
    cx = x
    for ch in text:
        gname = cmap.get(ord(ch))
        if gname is None:
            raise SystemExit(f"glifo faltante {ch!r}")
        t = (s, 0, 0, -s, cx, y)
        gs[gname].draw(TransformPen(pen, t))
        gs[gname].draw(TransformPen(bpen, t))
        cx += gs[gname].width * s + spacing
    adv = cx - x - spacing  # ancho sin el espaciado final
    return pen.getCommands(), adv, bpen.bounds

def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{title}">\n'
            f'<title>{title}</title>\n{body}\n</svg>\n')

PALETTES = {
    # web modo claro (header): texto --ink, tagline --ink-soft, divisor --line
    "fondo-claro": dict(kanji="#0d0d0b", name="#0d0d0b", tag="#6b6760", line="#ddd5c8"),
    # web modo oscuro: .topbar svg text{fill:#f5f0e8} / svg line{stroke:#2e2a23}
    "fondo-oscuro": dict(kanji="#f5f0e8", name="#f5f0e8", tag="#f5f0e8", line="#2e2a23"),
    # PROPUESTA: kanji en el dorado del favicon (#d4af6a), resto crema
    "fondo-oscuro-dorado": dict(kanji="#d4af6a", name="#f5f0e8", tag="#d8d0c2", line="#d4af6a"),
}

# ---------- 1) Horizontal: réplica del header de la web ----------
def horizontal(p):
    k, kw, kb = run(ZEN, "森下", 60, 8, 58, 1)
    n, nw, nb = run(MONO, "MORISHITA", 19.5, 147, 44, 4)
    t, tw, tb = run(MONO, "AUTHENTIC JAPANESE CUISINE", 8.5, 147, 60, 3.2)
    w = max(147 + nw, 147 + tw) + 8
    body = (f'<path fill="{p["kanji"]}" d="{k}"/>\n'
            f'<line x1="135" y1="8" x2="135" y2="64" stroke="{p["line"]}" stroke-width="1"/>\n'
            f'<path fill="{p["name"]}" d="{n}"/>\n<path fill="{p["tag"]}" d="{t}"/>')
    return svg(w, 72, body, "森下 Morishita · Authentic Japanese Cuisine")

# ---------- 2) Vertical (para cierre/CTA 9:16) ----------
def vertical(p, W=900):
    ks, ns, ts = 260, 68, 28
    # medir
    _, kw, kb = run(ZEN, "森下", ks, 0, 0, ks * 0.0167)
    _, nw, _ = run(MONO, "MORISHITA", ns, 0, 0, ns * 0.205)
    _, tw, _ = run(MONO, "AUTHENTIC JAPANESE CUISINE", ts, 0, 0, ts * 0.30)
    top = 40
    k_base = top - kb[1]  # kb[1] es negativo (sobre la línea base)
    k, _, kb2 = run(ZEN, "森下", ks, (W - kw) / 2, k_base, ks * 0.0167)
    y_line = kb2[3] + 46
    n_base = y_line + 46 + ns * 0.72
    n, _, nb = run(MONO, "MORISHITA", ns, (W - nw) / 2, n_base, ns * 0.205)
    t_base = n_base + 30 + ts * 1.2
    t, _, tb = run(MONO, "AUTHENTIC JAPANESE CUISINE", ts, (W - tw) / 2, t_base, ts * 0.30)
    H = tb[3] + 40
    body = (f'<path fill="{p["kanji"]}" d="{k}"/>\n'
            f'<line x1="{W/2-60:.1f}" y1="{y_line:.1f}" x2="{W/2+60:.1f}" y2="{y_line:.1f}" stroke="{p["line"]}" stroke-width="2"/>\n'
            f'<path fill="{p["name"]}" d="{n}"/>\n<path fill="{p["tag"]}" d="{t}"/>')
    return svg(W, H, body, "森下 Morishita · Authentic Japanese Cuisine")

# ---------- 3) Sello vertical (como favicon.png: 森 sobre 下, dorado sobre negro) ----------
def sello(bg=True, color="#d4af6a", S=512):
    size = 230
    _, w1, b1 = run(ZEN, "森", size, 0, 0)
    _, w2, b2 = run(ZEN, "下", size, 0, 0)
    gap = 18
    h1 = b1[3] - b1[1]; h2 = b2[3] - b2[1]
    total = h1 + gap + h2
    y0 = (S - total) / 2
    p1, _, _ = run(ZEN, "森", size, (S - w1) / 2, y0 - b1[1])
    p2, _, _ = run(ZEN, "下", size, (S - w2) / 2, y0 + h1 + gap - b2[1])
    rect = '<rect width="100%" height="100%" fill="#0a0908"/>\n' if bg else ""
    return svg(S, S, f'{rect}<path fill="{color}" d="{p1}"/>\n<path fill="{color}" d="{p2}"/>', "森下")

for name, p in PALETTES.items():
    (OUT / f"logo-horizontal-{name}.svg").write_text(horizontal(p), encoding="utf-8")
    (OUT / f"logo-vertical-{name}.svg").write_text(vertical(p), encoding="utf-8")
(OUT / "sello-morishita-dorado-fondo-negro.svg").write_text(sello(True), encoding="utf-8")
(OUT / "sello-morishita-dorado-transparente.svg").write_text(sello(False), encoding="utf-8")
(OUT / "sello-morishita-tinta-transparente.svg").write_text(sello(False, "#0d0d0b"), encoding="utf-8")

# Original de la web tal cual (texto vivo; requiere las fuentes instaladas)
(OUT / "logo-web-original-texto.svg").write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 72" fill="none">\n'
    ' <text x="8" y="58" font-family="\'Zen Antique Soft\',serif" font-size="60" fill="#0d0d0b" letter-spacing="1">森下</text>\n'
    ' <line x1="135" y1="8" x2="135" y2="64" stroke="#ddd5c8" stroke-width="1"/>\n'
    ' <text x="147" y="44" font-family="\'DM Mono\',\'Courier New\',monospace" font-size="19.5" fill="#0d0d0b" letter-spacing="4">MORISHITA</text>\n'
    ' <text x="147" y="60" font-family="\'DM Mono\',\'Courier New\',monospace" font-size="8.5" fill="#6b6760" letter-spacing="3.2">AUTHENTIC JAPANESE CUISINE</text>\n'
    '</svg>\n', encoding="utf-8")
print("\n".join(sorted(p.name for p in OUT.iterdir())))
