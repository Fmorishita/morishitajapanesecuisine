"""Renderiza la web en vivo y extrae, por cada clave data-ck, el texto estático
(HTML) y el texto final renderizado (tras aplicar /api/content)."""
import json, re, sys, html as htmlmod
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(sys.argv[1])
STATIC_HTML = Path(sys.argv[2]).read_text(encoding="utf-8")
API = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))

# texto estático por clave (desde el HTML descargado)
static = {}
for m in re.finditer(r'data-ck(?:-html)?="([^"]+)"[^>]*>(.*?)</(?:div|p|h1|h2|span|a|dt|dd|h4|text)>', STATIC_HTML, re.S):
    key, inner = m.group(1), m.group(2)
    txt = re.sub(r"<em>", " | ", inner)
    txt = re.sub(r"<[^>]+>", "", txt)
    static.setdefault(key, htmlmod.unescape(txt).strip())

JS = r"""
() => {
  const out = {};
  const vis = el => { const s = getComputedStyle(el); return s.display !== 'none' && s.visibility !== 'hidden' && el.offsetParent !== null; };
  document.querySelectorAll('[data-ck],[data-ck-html]').forEach(el => {
    const key = el.dataset.ck || el.dataset.ckHtml;
    let t = el.innerHTML.replace(/<em>/g, ' | ').replace(/<br\s*\/?>/g, ' / ').replace(/<[^>]+>/g, '');
    const ta = document.createElement('textarea'); ta.innerHTML = t; t = ta.value.trim();
    // visibilidad: el propio elemento o su contenedor data-ck-show
    let shown = true; let p = el;
    while (p) { if (p.dataset && p.dataset.ckShow) { const s = getComputedStyle(p); if (s.display === 'none') shown = false; } p = p.parentElement; }
    if (!(key in out)) out[key] = { text: t, shown };
  });
  const srcs = {};
  document.querySelectorAll('[data-ck-src]').forEach(el => srcs[el.dataset.ckSrc] = el.getAttribute('src'));
  const hrefs = {};
  document.querySelectorAll('[data-ck-href]').forEach(el => hrefs[el.dataset.ckHref] = el.getAttribute('href'));
  const custom = [];
  document.querySelectorAll('#custom-sections-mount > *').forEach(sec => custom.push({ id: sec.id || sec.dataset.sectionId || '', text: sec.innerText }));
  const order = [];
  document.querySelectorAll('#screen-home > [data-section-id], #screen-home > div, #custom-sections-mount > *').forEach(s => order.push(s.dataset.sectionId || s.id || s.className));
  return { out, srcs, hrefs, custom, order,
           homeText: document.querySelector('#screen-home').innerText,
           footerText: document.querySelector('footer').innerText,
           title: document.title };
}
"""

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path="/opt/pw-browsers/chromium")
    ctx = b.new_context(viewport={"width": 412, "height": 915}, device_scale_factor=1, is_mobile=True, has_touch=True, locale="es-MX")
    ctx.route(re.compile(r".*posthog\.com.*"), lambda r: r.abort())
    page = ctx.new_page()
    page.goto("https://www.morishitajapanesecuisine.com/", wait_until="networkidle")
    page.wait_for_timeout(2500)
    data = page.evaluate(JS)
    b.close()

data["static"] = static
data["api_keys_applied"] = sorted(k for k in API if k in data["out"])
OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print("keys rendered:", len(data["out"]), "static:", len(static), "custom sections:", len(data["custom"]))
print("order:", data["order"])
