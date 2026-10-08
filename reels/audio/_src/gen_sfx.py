"""Kit de SFX originales para los reels de Morishita (síntesis propia, 48 kHz, pico -3 dBFS)."""
import json
import os
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf

sys.path.insert(0, os.path.dirname(__file__))
from dsp import *  # noqa

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sfx", "synth"))
os.makedirs(OUT, exist_ok=True)
ROOM = make_ir(0.9, 0.008, 7000, seed=21)
HALL = make_ir(2.2, 0.02, 6000, seed=22)


def finish(x, peak_db=-3.0, tail=0.0):
    if x.ndim == 1:
        x = pan_st(x)
    if tail:
        x = np.concatenate([x, np.zeros((n_of(tail), 2))])
    x = x - x.mean(0)
    x = fade(x, 0.0005, 0.01)
    return x * (db(peak_db) / np.max(np.abs(x)))


def whoosh(dur, f0, f1, seed, peak_at=0.6):
    rng = np.random.default_rng(seed)
    n = n_of(dur)
    t = np.arange(n) / SR
    u = t / dur
    fc = np.where(u < peak_at, f0 * (f1 / f0) ** (u / peak_at), f1 * (f0 * 1.5 / f1) ** ((u - peak_at) / (1 - peak_at)))
    x = rng.standard_normal(n)
    y = svf_sweep(x, fc, q=0.9, mode="bp") + 0.3 * svf_sweep(rng.standard_normal(n), fc * 2.2, q=1.5, mode="bp")
    amp = np.where(u < peak_at, (u / peak_at) ** 2.2, (1 - (u - peak_at) / (1 - peak_at)) ** 1.6)
    y *= amp
    p = np.clip(u * 1.6 - 0.8, -0.8, 0.8)  # paneo izq -> der
    st = np.stack([y * np.cos((p + 1) * np.pi / 4), y * np.sin((p + 1) * np.pi / 4)], 1) * np.sqrt(2)
    return st + reverb(st, ROOM, 0.12)


def pop(f_start, f_end, tau=0.05, click=0.2, dur=0.18, body=1.0):
    n = n_of(dur)
    t = np.arange(n) / SR
    f = f_end + (f_start - f_end) * np.exp(-t / 0.012)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, tau, 0.0015) * body
    c = hp(noise(n_of(0.003)), 2500) * click
    y[: len(c)] += c * np.linspace(1, 0, len(c))
    return lp(y, 6000)


def wood_hit(f0, seed, bright=1.0):
    rng = np.random.default_rng(seed)
    n = n_of(0.6)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for r, a, tau in [(1.0, 1.0, 0.075), (2.32, 0.55, 0.04), (3.96, 0.35 * bright, 0.025), (5.6, 0.2 * bright, 0.015), (7.1, 0.1 * bright, 0.01)]:
        y += a * np.sin(2 * np.pi * f0 * r * t + rng.uniform(0, 6)) * np.exp(-t / tau)
    y += hp(rng.standard_normal(n), 1500) * np.exp(-t / 0.0025) * 0.9
    return y


def bell(f0, partials, dur, seed, mallet=0.004):
    rng = np.random.default_rng(seed)
    n = n_of(dur)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for r, a, tau in partials:
        for det, w in ((-0.6, 0.72), (0.6, 0.28)):  # pares desafinados -> batido suave (wah-wah) del rin
            y += w * a * np.sin(2 * np.pi * (f0 * r + det * r) * t + rng.uniform(0, 6)) * np.exp(-t / tau)
    att = np.clip(t / mallet, 0, 1)
    return y * att


SFX = []


def save(name, x, uso, peak_db=-3.0):
    x = finish(x, peak_db)
    path = os.path.join(OUT, name + ".wav")
    sf.write(path, x.astype(np.float32), SR, subtype="PCM_24")
    m = pyln.Meter(SR, block_size=min(0.4, len(x) / SR * 0.99))
    try:
        L = round(m.integrated_loudness(x), 1)
    except Exception:
        L = None
    env = np.abs(x).max(1)
    SFX.append(dict(archivo=name + ".wav", duracion_s=round(len(x) / SR, 3), pico_en_s=round(float(np.argmax(env)) / SR, 3),
                    pico_dbfs=round(20 * np.log10(env.max()), 2), lufs=L, uso=uso))


# --- whooshes
save("whoosh-corto-01", whoosh(0.25, 500, 6000, 1, 0.55), "Transición rápida (corte, punch-in). Golpe a 0.14 s: arráncalo 0.14 s antes del corte.")
save("whoosh-medio-02", whoosh(0.36, 350, 5000, 2, 0.6), "Whip pan / cambio de bloque. Golpe ~0.22 s.")
save("whoosh-suave-03", whoosh(0.5, 250, 3500, 3, 0.65), "Transición elegante y más oscura (entrada a la reseña, al plato estrella).")

# --- pops / clicks para texto
save("pop-texto-suave-01", pop(1100, 380, tau=0.045, click=0.15), "Aparece una palabra clave del subtítulo. Suave, no tapa la voz.")
save("pop-texto-agudo-02", pop(1700, 700, tau=0.03, click=0.25, dur=0.14), "Cifra o palabra resaltada (más brillante).")
_c = pop(2600, 1900, tau=0.008, click=0.6, dur=0.08) + 0.5 * wood_hit(1900, 5, 0.5)[: n_of(0.08)]
save("click-texto-madera-03", _c, "Click seco, tipo madera, para listas o texto que entra en ritmo.")

# --- booms
b1 = sub_boom(2.2, f_end=40, f_start=110, seed=1)
save("boom-grave-01", pan_st(b1) + reverb(b1, HALL, 0.10), "Golpe grave del gancho y de la revelación (cifra '14', '4 lugares'). Golpe a 0 s.")
b2 = sub_boom(2.6, f_end=36, f_start=95, seed=2) * 0.8 + taiko(62, 2.6, seed=3) * 0.7
save("boom-taiko-02", pan_st(b2) + reverb(b2, HALL, 0.22), "Impacto grave con cuerpo de taiko: revelación, cambio de sección, inicio del CTA.")

# --- risers (terminan en su punto más alto: el golpe va justo al final)
for dur, nm in [(1.5, "riser-1-5s"), (2.5, "riser-2-5s")]:
    n = n_of(dur)
    t = np.arange(n) / SR
    nz = noise_riser(dur, 400, 10000, seed=int(dur * 10))
    f = 180 * (8) ** ((t / dur) ** 1.4)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.5 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR)
    trem = 0.6 + 0.4 * np.sin(2 * np.pi * np.cumsum(4 + 20 * (t / dur) ** 2) / SR)
    y = nz * 0.8 + tone * trem * (t / dur) ** 2 * 0.35
    y[-n_of(0.01):] *= np.linspace(1, 0, n_of(0.01))
    st = pan_st(y)
    save(nm, st + reverb(st, HALL, 0.15)[: len(st)], f"Sube durante {dur} s y corta en seco: el final cae en el golpe (arráncalo {dur} s antes de la revelación).")

# --- glitch zap
rng = np.random.default_rng(9)
n = n_of(0.16)
t = np.arange(n) / SR
f = 2400 * np.exp(-t / 0.05) + 120
sq = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR))
gate = (np.floor(t / 0.011) % 3 != 1).astype(float)
crush = np.round(sq * gate * 6) / 6
z = crush * env_exp(n, 0.07, 0.001) * 0.6 + hp(rng.standard_normal(n), 3000) * gate * np.exp(-t / 0.03) * 0.4
z = lp(z, 9000)
zl, zr = z, np.roll(z, n_of(0.004))
save("glitch-zap", np.stack([zl, zr], 1), "Glitch corto SOLO sobre texto/gráfico (≤ 3 frames de efecto visual), nunca sobre comida.")

# --- tick obturador
n = n_of(0.12)
y = np.zeros(n)
for k, (dt, g) in enumerate([(0.0, 1.0), (0.028, 0.75)]):
    i = n_of(dt)
    m = n_of(0.03)
    tt = np.arange(m) / SR
    h = hp(noise(m), 1800) * np.exp(-tt / 0.004) + 0.5 * np.sin(2 * np.pi * (3200 - 600 * k) * tt) * np.exp(-tt / 0.006)
    y[i:i + m] += h * g
save("tick-obturador", pan_st(y) + reverb(y, ROOM, 0.08), "Tick de cámara: aparece una captura de pantalla o un 'foto fija'.")

# --- hyoshigi (2 golpes)
h1 = wood_hit(1320, 31)
h2 = wood_hit(1290, 32) * 0.92
n = n_of(1.3)
y = np.zeros(n)
y[: len(h1)] += h1
i = n_of(0.42)
y[i:i + len(h2)] += h2[: n - i]
st = pan_st(y, -0.05)
save("hyoshigi-2-golpes", st + reverb(st, HALL, 0.28), "Claves de madera japonesas (2 golpes, el 2º a 0.42 s): apertura, 'empieza el servicio', marcar el CTA. Firma sonora de la marca.")

# --- shing metálico sintético
n = n_of(2.2)
t = np.arange(n) / SR
y = np.zeros(n)
for r, a, tau in [(1.0, 1.0, 0.55), (1.47, 0.7, 0.45), (2.09, 0.5, 0.35), (2.76, 0.35, 0.25), (3.41, 0.25, 0.18)]:
    y += a * np.sin(2 * np.pi * 2650 * r * t * (1 + 0.004 * (1 - np.exp(-t / 0.15)))) * np.exp(-t / tau)
scrape = svf_sweep(noise(n), 2000 + 9000 * np.clip(t / 0.18, 0, 1), q=3, mode="bp") * np.exp(-np.clip(t - 0.12, 0, None) / 0.04) * np.clip(t / 0.15, 0, 1)
y = y * np.clip(t / 0.12, 0, 1) ** 0.5 + 1.2 * scrape
st = np.stack([y, np.roll(y, n_of(0.0007))], 1)
save("shing-metal", st + reverb(st, HALL, 0.2), "Destello metálico sintético (no es sonido real de cuchillo): brillo sobre un título o el sello del cierre.")

# --- rin (campanita budista suave)
r = bell(1046, [(1.0, 1.0, 1.0), (2.71, 0.45, 0.6), (5.15, 0.18, 0.3), (8.1, 0.06, 0.15)], 4.0, 41, mallet=0.006)
st = pan_st(r, 0.1)
save("rin-resena", st + reverb(st, HALL, 0.25), "Campanita suave al aparecer una reseña de Google (estrellas). Volumen 0.3–0.5 bajo la voz.")

# --- tap de teléfono / UI para el CTA
n = n_of(0.09)
t = np.arange(n) / SR
y = np.sin(2 * np.pi * (220 + 300 * np.exp(-t / 0.006)) * t) * np.exp(-t / 0.022) + 0.35 * np.sin(2 * np.pi * 1450 * t) * np.exp(-t / 0.008)
y += hp(noise(n), 3000) * np.exp(-t / 0.0015) * 0.3
save("tap-cta", lp(y, 7000), "Toque de dedo en pantalla/botón: 'Reservar', link del perfil, captura del flujo de reserva.")

with open(os.path.join(OUT, "manifest.json"), "w") as fh:
    json.dump(SFX, fh, ensure_ascii=False, indent=1)
for s in SFX:
    print(s)
