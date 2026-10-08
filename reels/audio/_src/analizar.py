"""Mide y dibuja (forma de onda + espectrograma) una mezcla con su beat grid.

Uso: python analizar.py ruta.wav [ruta.beats.json]
Imprime JSON de métricas y escribe ruta.png junto al wav.
"""
import glob
import json
import os
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont
from scipy import signal

SEC_COL = {"intro": (212, 175, 106), "build": (120, 140, 170), "drop": (196, 96, 122), "drop2": (196, 96, 122),
           "respiro": (110, 160, 130), "rebuild": (120, 140, 170), "salida": (212, 175, 106)}


def font(sz):
    for p in glob.glob("/usr/share/fonts/**/DejaVuSans.ttf", recursive=True) + glob.glob(
            os.path.join(os.path.dirname(__file__), "..", "..", "marca", "fonts", "*.ttf")):
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def true_peak(x):
    return float(np.max(np.abs(signal.resample_poly(x, 4, 1, axis=0))))


def dbv(x):
    return 20 * np.log10(max(x, 1e-12))


def bands(x, sr):
    m = x.mean(1) if x.ndim == 2 else x
    f, P = signal.welch(m, sr, nperseg=8192)
    tot = P.sum()
    out = {}
    for name, a, b in [("sub <60", 0, 60), ("graves 60-250", 60, 250), ("medios 250-2k", 250, 2000),
                       ("medios-altos 2k-6k", 2000, 6000), ("aire >6k", 6000, sr / 2)]:
        out[name] = round(100 * P[(f >= a) & (f < b)].sum() / tot, 1)
    return out


def analyze(path, grid_path=None):
    x, sr = sf.read(path, always_2d=True)
    meter = pyln.Meter(sr)
    res = dict(archivo=os.path.basename(path), duracion_s=round(len(x) / sr, 3), sr=sr, canales=x.shape[1])
    res["lufs_integrado"] = round(meter.integrated_loudness(x), 2)
    res["true_peak_dbtp"] = round(dbv(true_peak(x)), 2)
    res["sample_peak_dbfs"] = round(dbv(np.max(np.abs(x))), 2)
    rms = np.sqrt(np.mean(x ** 2))
    res["crest_factor_db"] = round(dbv(np.max(np.abs(x))) - dbv(rms), 2)
    res["muestras_>=0dBFS"] = int(np.sum(np.abs(x) >= 0.9999))
    res["correlacion_LR"] = round(float(np.corrcoef(x[:, 0], x[:, 1])[0, 1]), 3)
    res["bandas_%energia"] = bands(x, sr)
    try:
        res["rango_loudness_LRA_aprox"] = None
    except Exception:
        pass
    grid = None
    if grid_path and os.path.exists(grid_path):
        grid = json.load(open(grid_path))
        secs = []
        for s in grid["secciones"]:
            a, b = int(s["inicio_s"] * sr), int(s["fin_s"] * sr)
            seg = x[a:b]
            if len(seg) < 0.5 * sr:
                continue
            r = np.sqrt(np.mean(seg ** 2))
            secs.append(dict(seccion=s["nombre"], desde=s["inicio_s"], hasta=s["fin_s"],
                             lufs=round(meter.integrated_loudness(seg), 1),
                             crest_db=round(dbv(np.max(np.abs(seg))) - dbv(r), 1),
                             bandas=bands(seg, sr)))
        res["por_seccion"] = secs
    # loudness de corto plazo (3 s, paso 1 s) para ver la curva y los últimos 6 s
    st = []
    for t in np.arange(0, len(x) / sr - 3 + 1e-6, 1.0):
        seg = x[int(t * sr): int((t + 3) * sr)]
        st.append(round(meter.integrated_loudness(seg), 1) if np.any(seg) else -70)
    res["short_term_3s_cada_1s"] = st
    last = x[-6 * sr:]
    rr = [dbv(np.sqrt(np.mean(last[i * sr // 2:(i + 1) * sr // 2] ** 2)) + 1e-12) for i in range(12)]
    res["ultimos_6s_rms_cada_0.5s_db"] = [round(v, 1) for v in rr]
    res["ultimos_6s_max_salto_db"] = round(float(np.max(np.diff(rr))), 2)
    draw(x, sr, path[:-4] + ".png", grid, res)
    return res


def cmap(v):
    # negro -> violeta -> rosa -> oro -> crema
    stops = np.array([[10, 9, 8], [60, 30, 80], [196, 96, 122], [212, 175, 106], [245, 240, 232]], float)
    pos = np.linspace(0, 1, len(stops))
    return np.stack([np.interp(v, pos, stops[:, c]) for c in range(3)], -1).astype(np.uint8)


def draw(x, sr, out, grid, res):
    W, H = 1800, 1000
    top, wh, sh = 70, 280, 560
    img = Image.new("RGB", (W, H), (10, 9, 8))
    d = ImageDraw.Draw(img)
    m = x.mean(1)
    dur = len(m) / sr
    x0, x1 = 70, W - 30
    pw = x1 - x0
    # secciones
    if grid:
        for s in grid["secciones"]:
            a = x0 + pw * s["inicio_s"] / dur
            b = x0 + pw * min(s["fin_s"], dur) / dur
            c = SEC_COL.get(s["nombre"], (90, 90, 90))
            d.rectangle([a, top, b, top + wh], fill=tuple(int(v * 0.22) for v in c))
            d.text((a + 4, top + 4), f'{s["nombre"]} {s["inicio_s"]:.1f}s', fill=c, font=font(15))
        for t in grid["inicios_de_compas"]:
            xx = x0 + pw * t / dur
            d.line([xx, top + wh - 8, xx, top + wh], fill=(80, 76, 70))
    # forma de onda
    cols = np.array_split(m, pw)
    mid = top + wh / 2
    for i, c in enumerate(cols):
        if len(c) == 0:
            continue
        hi, lo = c.max(), c.min()
        r = np.sqrt(np.mean(c ** 2))
        d.line([x0 + i, mid - hi * wh / 2, x0 + i, mid - lo * wh / 2], fill=(150, 140, 125))
        d.line([x0 + i, mid - r * wh / 2, x0 + i, mid + r * wh / 2], fill=(245, 240, 232))
    # espectrograma log
    f, t, Z = signal.stft(m, sr, nperseg=4096, noverlap=4096 - 1024)
    S = 20 * np.log10(np.abs(Z) + 1e-9)
    S = np.clip((S - (S.max() - 90)) / 90, 0, 1)
    fy = np.geomspace(30, 16000, sh)
    rows = np.searchsorted(f, fy)
    rows = np.clip(rows, 0, len(f) - 1)
    Sx = S[rows][::-1]
    tx = np.linspace(0, Sx.shape[1] - 1, pw).astype(int)
    Sx = Sx[:, tx]
    spec = Image.fromarray(cmap(Sx))
    sy = top + wh + 40
    img.paste(spec, (x0, sy))
    for fr in [50, 100, 250, 500, 1000, 2000, 4000, 8000, 16000]:
        yy = sy + sh - 1 - np.searchsorted(fy, fr) * 1.0
        d.line([x0 - 6, yy, x0, yy], fill=(200, 200, 200))
        d.text((4, yy - 8), f"{fr if fr < 1000 else str(fr // 1000) + 'k'}", fill=(200, 190, 175), font=font(13))
    for s in range(0, int(dur) + 1, 4):
        xx = x0 + pw * s / dur
        d.line([xx, sy + sh, xx, sy + sh + 6], fill=(200, 200, 200))
        d.text((xx - 8, sy + sh + 8), f"{s}s", fill=(200, 190, 175), font=font(13))
    if grid:
        for s in grid["secciones"]:
            xx = x0 + pw * s["inicio_s"] / dur
            d.line([xx, sy, xx, sy + sh], fill=(212, 175, 106))
    d.text((x0, 18), f'{res["archivo"]}  ·  {res["lufs_integrado"]} LUFS  ·  {res["true_peak_dbtp"]} dBTP  ·  crest {res["crest_factor_db"]} dB',
           fill=(245, 240, 232), font=font(22))
    img.save(out)


if __name__ == "__main__":
    p = sys.argv[1]
    g = sys.argv[2] if len(sys.argv) > 2 else p[:-4] + ".beats.json"
    r = analyze(p, g)
    print(json.dumps(r, ensure_ascii=False, indent=1))
