import re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT = Path(sys.argv[1])
with sync_playwright() as pw:
    b = pw.chromium.launch(headless=True, executable_path="/opt/pw-browsers/chromium")
    for theme in ("light", "dark"):
        ctx = b.new_context(viewport={"width": 412, "height": 915}, device_scale_factor=2.625, is_mobile=True, has_touch=True, locale="es-MX")
        ctx.route(re.compile(r".*posthog\.com.*"), lambda r: r.abort())
        ctx.add_init_script(f"try{{localStorage.setItem('theme','{theme}')}}catch(e){{}}")
        pg = ctx.new_page(); pg.goto("https://www.morishitajapanesecuisine.com/", wait_until="networkidle"); pg.wait_for_timeout(2000)
        pg.add_style_tag(content=".sakura-bg,.petal,#themeToggle,.theme-toggle,.topbar{display:none!important}")
        el = pg.locator(".reserve-cta-section"); el.scroll_into_view_if_needed(); pg.wait_for_timeout(800)
        el.screenshot(path=str(OUT / f"home-reservar-resumen-{theme}-limpia.png"))
        ctx.close()
    b.close()
print("ok")
