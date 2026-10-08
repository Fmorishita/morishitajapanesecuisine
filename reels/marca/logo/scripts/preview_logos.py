import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

LOGO = Path(sys.argv[1]); FONTS = Path(sys.argv[2])
inline = lambda n: (LOGO / n).read_text(encoding="utf-8")
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:'Zen Antique Soft';src:url('file://{FONTS}/zen-antique-soft/ZenAntiqueSoft-Regular.ttf')}}
@font-face{{font-family:'DM Mono';src:url('file://{FONTS}/dm-mono/DMMono-Regular.ttf')}}
body{{margin:0;font-family:'DM Mono',monospace;font-size:13px;background:#888}}
.row{{display:flex}} .cell{{flex:1;padding:28px;display:flex;flex-direction:column;align-items:center;gap:10px}}
.c{{background:#faf8f4;color:#6b6760}} .d{{background:#0a0908;color:#9a9285}}
.h svg{{width:540px;height:auto}} .v svg{{width:330px;height:auto}} .s svg{{width:150px;height:150px}}
</style></head><body>
<div class="row h"><div class="cell c">{inline('logo-horizontal-fondo-claro.svg')}<span>logo-horizontal-fondo-claro (trazos)</span></div>
<div class="cell d">{inline('logo-horizontal-fondo-oscuro.svg')}<span>logo-horizontal-fondo-oscuro (trazos)</span></div></div>
<div class="row h"><div class="cell c">{inline('logo-web-original-texto.svg').replace('viewBox="0 0 360 72"','viewBox="0 0 368 72"')}<span>ORIGINAL web (texto vivo, mismas fuentes)</span></div>
<div class="cell d">{inline('logo-horizontal-fondo-oscuro-dorado.svg')}<span>logo-horizontal-fondo-oscuro-dorado (PROPUESTA)</span></div></div>
<div class="row v"><div class="cell c">{inline('logo-vertical-fondo-claro.svg')}<span>vertical fondo-claro</span></div>
<div class="cell d">{inline('logo-vertical-fondo-oscuro.svg')}<span>vertical fondo-oscuro</span></div>
<div class="cell d">{inline('logo-vertical-fondo-oscuro-dorado.svg')}<span>vertical oscuro-dorado (PROPUESTA)</span></div></div>
<div class="row s"><div class="cell d">{inline('sello-morishita-dorado-fondo-negro.svg')}<span>sello SVG</span></div>
<div class="cell d"><img src="file://{LOGO}/favicon.png" width="150" height="150"><span>favicon.png (web)</span></div>
<div class="cell c">{inline('sello-morishita-tinta-transparente.svg')}<span>sello tinta</span></div></div>
</body></html>"""
tmp = Path(sys.argv[3]); tmp.write_text(html, encoding="utf-8")
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path="/opt/pw-browsers/chromium", args=["--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1300, "height": 800}, device_scale_factor=1)
    pg.goto("file://" + str(tmp)); pg.wait_for_timeout(800)
    pg.screenshot(path=str(LOGO / "preview-logos.png"), full_page=True)
    # PNG transparentes para video
    for name, w in [("logo-vertical-fondo-oscuro", 900), ("logo-vertical-fondo-claro", 900), ("logo-vertical-fondo-oscuro-dorado", 900),
                    ("logo-horizontal-fondo-oscuro", 1104), ("logo-horizontal-fondo-claro", 1104), ("sello-morishita-dorado-transparente", 512)]:
        svgtxt = inline(name + ".svg")
        pg2 = b.new_page(viewport={"width": w, "height": 200}, device_scale_factor=1)
        pg2.set_content(f"<html><body style='margin:0;background:transparent'>{svgtxt.replace('<svg ', '<svg id=L style=\"display:block;width:'+str(w)+'px;height:auto\" ',1)}</body></html>")
        pg2.locator("#L").screenshot(path=str(LOGO / f"{name}.png"), omit_background=True)
        pg2.close()
    b.close()
print("ok")
