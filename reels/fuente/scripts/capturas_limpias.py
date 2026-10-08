"""Variantes limpias para CTA: oculta solo los pétalos animados y el botón de tema.
Solo lectura: no se llena ningún dato ni se paga."""
import re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
BASE = "https://www.morishitajapanesecuisine.com"
CLEAN_CSS = ".sakura-bg,.petal,#themeToggle,.theme-toggle{display:none!important}"

def settle(page, ms=2000):
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(ms)

with sync_playwright() as pw:
    b = pw.chromium.launch(headless=True, executable_path="/opt/pw-browsers/chromium")
    for theme in ("light", "dark"):
        ctx = b.new_context(viewport={"width": 412, "height": 915}, device_scale_factor=2.625,
                            is_mobile=True, has_touch=True, locale="es-MX", timezone_id="America/Tijuana")
        ctx.route(re.compile(r".*posthog\.com.*"), lambda r: r.abort())
        ctx.add_init_script(f"try{{localStorage.setItem('theme','{theme}')}}catch(e){{}}")
        page = ctx.new_page()
        page.goto(BASE + "/?reservar=1", wait_until="domcontentloaded"); settle(page)
        page.add_style_tag(content=CLEAN_CSS); page.wait_for_timeout(400)
        page.screenshot(path=str(OUT / f"reserva-1-comensales-{theme}-limpia.png"))
        page.locator("#gNext").click(); page.wait_for_timeout(3000); settle(page, 800)
        page.screenshot(path=str(OUT / f"reserva-2-fechas-{theme}-limpia.png"))
        page.locator(".cal-card").screenshot(path=str(OUT / f"reserva-2-calendario-{theme}-recorte.png"))
        # clic en el primer día disponible -> pantalla de horarios (no reserva nada)
        day = page.locator(".cal-grid .cday.avail")
        try:
            day.first.click(timeout=4000); page.wait_for_timeout(2500); settle(page, 600)
            page.screenshot(path=str(OUT / f"reserva-3-horarios-{theme}-limpia.png"))
            print("horarios ok", theme, page.locator("#slotsGrid").inner_text()[:400].replace("\n", " | "))
        except Exception as e:
            print("no se pudo abrir horarios:", e)
        ctx.close()
    b.close()
