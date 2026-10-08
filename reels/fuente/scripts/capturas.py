"""Capturas de la web en vivo para reels (solo lectura: no reserva, no paga,
no llena datos personales). PostHog bloqueado para no ensuciar analíticas."""
import re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
BASE = "https://www.morishitajapanesecuisine.com"

def ctx_for(browser, theme):
    ctx = browser.new_context(viewport={"width": 412, "height": 915}, device_scale_factor=2.625,
                              is_mobile=True, has_touch=True, locale="es-MX", timezone_id="America/Tijuana")
    ctx.route(re.compile(r".*posthog\.com.*"), lambda r: r.abort())
    ctx.add_init_script(f"try{{localStorage.setItem('theme','{theme}')}}catch(e){{}}")
    return ctx

def settle(page, ms=1800):
    page.wait_for_load_state("networkidle")
    try:
        page.wait_for_selector("#page-loader.hide", timeout=8000, state="attached")
    except Exception:
        pass
    page.wait_for_timeout(ms)

def shot(page, name):
    p = OUT / name
    page.screenshot(path=str(p))
    print("ok", p.name)

with sync_playwright() as pw:
    b = pw.chromium.launch(headless=True, executable_path="/opt/pw-browsers/chromium")
    for theme in ("light", "dark"):
        ctx = ctx_for(b, theme)
        page = ctx.new_page()
        # 1) HOME · hero
        page.goto(BASE + "/", wait_until="domcontentloaded"); settle(page)
        shot(page, f"home-hero-{theme}.png")
        # 2) reseñas: encabezado de la sección y cada testimonio
        sec = page.locator(".social-section")
        sec.scroll_into_view_if_needed(); page.wait_for_timeout(600)
        page.evaluate("()=>{const s=document.querySelector('.social-section');window.scrollTo(0,s.getBoundingClientRect().top+window.scrollY-64)}")
        page.wait_for_timeout(900)
        shot(page, f"resenas-{theme}-1.png")
        page.evaluate("()=>window.scrollBy(0,700)"); page.wait_for_timeout(700)
        shot(page, f"resenas-{theme}-2.png")
        page.evaluate("()=>window.scrollBy(0,700)"); page.wait_for_timeout(700)
        shot(page, f"resenas-{theme}-3.png")
        sec.screenshot(path=str(OUT / f"resenas-{theme}-seccion-completa.png")); print("ok seccion completa")
        for i in (1, 2, 3):
            page.locator(f'.testimonial[data-card-id="t{i}"]').screenshot(path=str(OUT / f"resena-t{i}-{theme}.png"))
        # 3) reservar: info de la sección reservar
        page.evaluate("()=>{const s=document.querySelector('.reserve-cta-section');window.scrollTo(0,s.getBoundingClientRect().top+window.scrollY-64)}")
        page.wait_for_timeout(900)
        shot(page, f"home-reservar-{theme}.png")
        # 4) flujo de reserva: comensales
        page.goto(BASE + "/?reservar=1", wait_until="domcontentloaded"); settle(page, 2200)
        shot(page, f"reserva-1-comensales-{theme}.png")
        # 5) un clic: "Ver fechas disponibles" -> calendario
        page.locator("#gNext").click(); page.wait_for_timeout(3500)
        page.wait_for_load_state("networkidle"); page.wait_for_timeout(800)
        shot(page, f"reserva-2-fechas-{theme}.png")
        ctx.close()
    b.close()
