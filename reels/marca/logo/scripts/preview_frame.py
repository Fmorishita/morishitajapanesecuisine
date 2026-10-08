import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

MARCA = Path(sys.argv[1]); F = MARCA / "fonts"; L = MARCA / "logo"
svg = (L / "logo-vertical-fondo-oscuro-dorado.svg").read_text(encoding="utf-8")
svg2 = (L / "logo-vertical-fondo-claro.svg").read_text(encoding="utf-8")
CSS = f"""
@font-face{{font-family:'Zen Antique Soft';src:url('file://{F}/zen-antique-soft/ZenAntiqueSoft-Regular.ttf')}}
@font-face{{font-family:'Cormorant';src:url('file://{F}/cormorant/Cormorant[wght].ttf');font-weight:300 700}}
@font-face{{font-family:'Cormorant';font-style:italic;src:url('file://{F}/cormorant/Cormorant-Italic[wght].ttf');font-weight:300 700}}
@font-face{{font-family:'DM Mono';src:url('file://{F}/dm-mono/DMMono-Regular.ttf');font-weight:400}}
@font-face{{font-family:'DM Mono';src:url('file://{F}/dm-mono/DMMono-Medium.ttf');font-weight:500}}
*{{margin:0;box-sizing:border-box}}
.f{{position:relative;width:1080px;height:1920px;overflow:hidden}}
.safe{{position:absolute;left:65px;top:270px;width:950px;height:978px;outline:3px dashed rgba(232,160,176,.85)}}
.lbl{{position:absolute;font:500 22px 'DM Mono';letter-spacing:.12em;color:rgba(232,160,176,.95)}}
.ui{{position:absolute;left:0;right:0;background:rgba(232,160,176,.10)}}
.eyebrow{{font:400 30px 'DM Mono';letter-spacing:.32em;text-transform:uppercase}}
.h1{{font-family:'Zen Antique Soft';font-size:150px;line-height:.95;letter-spacing:-.02em}}
.em{{font-family:'Cormorant';font-style:italic;font-weight:300;font-size:96px;line-height:1.05}}
.sub{{position:absolute;left:65px;right:65px;text-align:center;font-family:'Zen Antique Soft';font-size:96px;line-height:1.05}}
.kw{{display:inline-block;transform:scale(1.2);transform-origin:center bottom;padding:0 .12em}}
"""
def frame(bg, ink, accent, inner):
    return f"<div class='f' style='background:{bg};color:{ink}'>{inner}" \
           f"<div class='ui' style='top:0;height:270px'></div><div class='ui' style='top:1248px;height:672px'></div>" \
           f"<div class='safe'></div><div class='lbl' style='left:75px;top:232px'>ÁREA ÚTIL x65–1015 · y270–1248</div>" \
           f"<div class='lbl' style='left:75px;top:1262px'>UI de Instagram (caption, botones) — nada importante aquí</div></div>"

dark = frame("#0a0908", "#f5f0e8", "#d4af6a",
  "<div style='position:absolute;left:65px;right:65px;top:330px;text-align:center'>"
  "<div class='eyebrow' style='color:#d4af6a'>Ensenada · Baja California</div></div>"
  "<div class='sub' style='top:520px'>Solo <span class='kw' style='color:#d4af6a'>4</span> asientos</div>"
  "<div class='sub' style='top:660px;font-family:Cormorant;font-style:italic;font-weight:300;color:#d4af6a'>por sesión</div>"
  f"<div style='position:absolute;left:240px;width:600px;top:860px'>{svg.replace('<svg ','<svg style=\"width:600px;height:auto\" ',1)}</div>")
light = frame("#faf8f4", "#0d0d0b", "#c4607a",
  "<div style='position:absolute;left:65px;right:65px;top:330px;text-align:center'>"
  "<div class='eyebrow' style='color:#c4607a'>Omakase · 14 tiempos</div>"
  "<div class='h1' style='margin-top:40px'>Omakase</div><div class='em' style='color:#c4607a'>Catorce tiempos.</div></div>"
  "<div class='sub' style='top:740px;font-size:84px'>Reserva en el <span class='kw' style='color:#c4607a'>link</span></div>"
  f"<div style='position:absolute;left:330px;width:420px;top:900px'>{svg2.replace('<svg ','<svg style=\"width:420px;height:auto\" ',1)}</div>")
html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body style='margin:0;display:flex;gap:40px;background:#777'>{dark}{light}</body></html>"
tmp = Path(sys.argv[2]); tmp.write_text(html, encoding="utf-8")
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path="/opt/pw-browsers/chromium", args=["--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 2200, "height": 1920})
    pg.goto("file://" + str(tmp)); pg.wait_for_timeout(1000)
    pg.screenshot(path=str(MARCA / "logo" / "preview-frame-1080x1920.png"))
    b.close()
print("ok")
