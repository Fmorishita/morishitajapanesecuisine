"""Genera las bases musicales originales de Morishita (A 112 BPM / B 120 BPM).

Uso:  /tmp/claude-0/venv/bin/python reels/audio/_src/gen_musica.py [A|B|A40|B40 ...]
Todo es síntesis propia (ver dsp.py). Determinista: mismas semillas -> mismo audio.
"""
import json
import os
import sys

import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.dirname(__file__))
from dsp import *  # noqa

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "musica"))
STEMS = os.path.join(OUT, "stems")

# ------------------------------------------------------------------ variantes
VARIANTS = {
    "A": dict(
        name="morishita-bed-A-112", bpm=112, style="trap", dur=64.0,
        root=62, scale=[0, 2, 3, 7, 8], scale_name="Hirajoshi en Re (D E F A Bb)",
        chords=[[50, 53, 57, 60, 64], [46, 53, 57, 60, 62], [43, 50, 53, 58, 62], [45, 52, 55, 62, 64]],
        chord_names=["Dm9", "Bbmaj9", "Gm(add9)", "A7sus4"],
        bass=[38, 34, 31, 33], final_chord=[50, 53, 57, 60, 64, 69], final_bass=38,
        arp=[[0, 3, 5, 6], [-1, 2, 4, 5], [-1, 2, 5, 4], [-2, 1, 3, 5]],
        sections=[("intro", 1), ("build", 8), ("drop", 6), ("respiro", 4), ("rebuild", 3), ("drop2", 4), ("salida", None)],
        taiko_f=64,
    ),
    "B": dict(
        name="morishita-bed-B-120", bpm=120, style="house", dur=64.0,
        root=64, scale=[0, 1, 5, 7, 8], scale_name="Miyako-bushi en Mi (E F A B C)",
        chords=[[45, 52, 60, 64, 67, 71], [41, 48, 52, 55, 57], [38, 45, 53, 57, 60, 64], [40, 47, 57, 62, 65]],
        chord_names=["Am9", "Fmaj9", "Dm9", "E7sus4(b9)"],
        bass=[33, 29, 38, 40], final_chord=[45, 52, 60, 64, 67, 71], final_bass=33,
        arp=[[-3, 0, 2, 4], [-4, -1, 0, 2], [-3, -1, 1, 2], [-5, -2, 1, 2]],
        sections=[("intro", 1), ("build", 9), ("drop", 6), ("respiro", 4), ("rebuild", 3), ("drop2", 5), ("salida", None)],
        taiko_f=70,
    ),
}
# Cortes de ~40 s (extra) para reels de 35–45 s: mismo material, forma corta.
VARIANTS["A40"] = dict(VARIANTS["A"], name="morishita-bed-A-112-corte40", dur=40.7,
                       sections=[("intro", 1), ("build", 4), ("drop", 5), ("respiro", 4), ("rebuild", 2), ("salida", None)])
VARIANTS["B40"] = dict(VARIANTS["B"], name="morishita-bed-B-120-corte40", dur=40.0,
                       sections=[("intro", 1), ("build", 4), ("drop", 6), ("respiro", 4), ("rebuild", 2), ("salida", None)])

# melodías (tiempo en beats, grado de escala, duración en beats, vel, bend)
HOOK = {
    "A": [  # 4 compases, medio tiempo, aire entre frases
        (0, 8, .75, 1.0, None), (.75, 7, .75, .8, None), (1.5, 6, .5, .75, None), (2, 5, 1.0, .9, None),
        (3, 3, .5, .7, None), (3.5, 4, .5, .75, None),
        (4, 5, 1.5, .95, (0.22, 2, 0.12)), (6, 3, .5, .7, None), (6.5, 2, .5, .7, None), (7, 3, 1, .8, None),
        (8, 8, .75, 1.0, None), (8.75, 9, .75, .85, None), (9.5, 8, .5, .8, None), (10, 7, 1, .9, None),
        (11, 6, .5, .7, None), (11.5, 5, .5, .75, None),
        (12, 6, 2, .9, (0.25, 1, 0.1)), (14, 5, .5, .7, None), (14.5, 3, .5, .6, None), (15, 5, 1, .8, None),
    ],
    "B": [
        (0, 7, .5, 1.0, None), (.5, 6, .25, .75, None), (.75, 5, .75, .85, None), (1.5, 3, .5, .75, None),
        (2, 4, 1, .9, None), (3, 5, .5, .8, None), (3.5, 6, .5, .8, None),
        (4, 5, 1.5, .95, (0.2, 1, 0.08)), (5.5, 3, .5, .7, None), (6, 2, 1, .8, None), (7, 3, 1, .8, None),
        (8, 7, .5, 1.0, None), (8.5, 8, .25, .8, None), (8.75, 7, .75, .85, None), (9.5, 5, .5, .8, None),
        (10, 6, 1, .9, None), (11, 5, .5, .75, None), (11.5, 4, .5, .75, None),
        (12, 3, 2, .9, (0.25, 1, 0.1)), (14, 2, .5, .7, None), (14.5, 1, .5, .7, None), (15, 0, 1, .8, None),
    ],
}
# shakuhachi: (beat, midi, dur_beats, vel)
SHAKU_BREATH = {
    "A": [(0, 69, 3, .9), (3.5, 70, 1, .7), (4.5, 69, 1.5, .8), (6, 65, 2, .85), (8.5, 64, 1, .7), (9.5, 62, 3.5, .9), (13.5, 65, 1, .7), (14.5, 64, 1.5, .75)],
    "B": [(0, 71, 3, .9), (3.5, 72, 1, .7), (4.5, 71, 1.5, .8), (6, 69, 2, .85), (8.5, 65, 1, .7), (9.5, 64, 3.5, .9), (13.5, 69, 1, .7), (14.5, 71, 1.5, .75)],
}
SHAKU_ANSWER = {
    "A": [(0, 74, 1.5, .8), (1.5, 76, .5, .65), (2, 77, 2, .8), (4.5, 76, 1, .7), (5.5, 74, 2.5, .8)],
    "B": [(0, 76, 1.5, .8), (1.5, 77, .5, .65), (2, 76, 2, .8), (4.5, 72, 1, .7), (5.5, 71, 2.5, .8)],
}
SHAKU_FINAL = {"A": 74, "B": 76}


def deg2midi(v, d):
    sc = v["scale"]
    o, i = divmod(d, len(sc))
    return v["root"] + 12 * o + sc[i]


def render(key):
    v = VARIANTS[key]
    base = key[0]
    bpm = v["bpm"]
    spb = 60.0 / bpm
    bar = 4 * spb
    dur = v["dur"]
    N = n_of(dur)
    rng = np.random.default_rng({"A": 11, "B": 22}[base])

    # secciones en compases
    secs, b = [], 0
    for name, nb in v["sections"]:
        if nb is None:
            nb = int(np.ceil((dur - b * bar) / bar))
        secs.append((name, b, b + nb))
        b += nb
    out_bar = [s for s in secs if s[0] == "salida"][0][1]

    def T(barn, beat=0.0):
        return barn * bar + beat * spb

    def sec_of(barn):
        for name, s0, s1 in secs:
            if s0 <= barn < s1:
                return name, barn - s0, s1 - s0
        return "salida", 0, 1

    st = {k: np.zeros((N + n_of(4), 2)) for k in ["drums", "bass", "melodic", "pad", "fx"]}
    kick_times = []

    # ---------------------------------------------------- golpe de entrada (0 s)
    place(st["fx"], sub_boom(2.6, f_end=40), 0.0, db(-6))
    place(st["drums"], taiko(v["taiko_f"], 2.0, seed=1), 0.0, db(-2))
    place(st["drums"], taiko(v["taiko_f"] * 1.5, 1.2, seed=2), 0.0, db(-9), pan=0.2)
    place(st["fx"], crash(2.8, seed=1), 0.0, db(-16))
    # sararin: glissando ascendente de koto sobre la escala
    for i, d in enumerate(range(0, 11)):
        place(st["melodic"], koto(deg2midi(v, d), 2.6, bright=.7, seed=i), 0.012 + i * 0.028, db(-9 + i * 0.3), pan=-0.4 + i * 0.08)

    # ---------------------------------------------------- recorrido por compases
    nbars = int(np.ceil(dur / bar))
    for bn in range(nbars):
        name, k, L = sec_of(bn)
        prog = k / max(1, L - 1)
        ci = bn % 4
        chord = v["chords"][ci]
        broot = v["bass"][ci]
        last_bar = (k == L - 1)
        nxt = sec_of(bn + 1)[0] if bn + 1 < nbars else None
        gap = last_bar and nxt in ("drop", "drop2")  # silencio antes del drop
        t0 = T(bn)

        # ---------- PAD
        if name != "salida":
            g = {"intro": -7, "build": -6 + 1.5 * prog, "drop": -10, "respiro": -11, "rebuild": -9, "drop2": -9}[name]
            pc = pad_chord([m + 12 if m < 52 else m for m in chord], bar + 1.2, bright=2000 if name in ("build", "intro", "respiro") else 3400, seed=bn % 4)
            pc = pc * adsr(len(pc), 0.35 if name != "drop" else 0.05, 0.3, 0.85, 1.0)[:, None]
            place(st["pad"], pc, t0, db(g))

        # ---------- KOTO arpegio (build/respiro/rebuild) e hook (drops)
        arp = v["arp"][ci]
        if name in ("build", "rebuild") or (name == "intro"):
            if name != "intro" or k >= 0:
                patt = [0, 1, 2, 1, 3, 1, 2, 1] if v["style"] == "trap" else [0, 2, 1, 3, 2, 1, 3, 2]
                steps = 8 if (name == "build" and prog < 0.5) or name == "intro" else 16
                for s in range(steps):
                    if name == "intro" and s < 4:
                        continue
                    beat = s * (4 / steps)
                    if gap and beat >= 3.0:
                        break
                    d = arp[patt[s % 8]] + (5 if (s // 8) % 2 and steps == 16 else 0)
                    vel = (0.55 if s % 2 == 0 else 0.4) * (0.75 + 0.25 * prog)
                    jit = rng.uniform(-0.004, 0.004)
                    place(st["melodic"], koto(deg2midi(v, d), 1.4, bright=.45 + .2 * prog, seed=s), t0 + beat * spb + jit,
                          db(-9) * vel, pan=0.35 if s % 2 else -0.25)
        if name in ("drop", "drop2"):
            hook = HOOK[base]
            ph = (k % 4)
            for (bt, d, du, vel, bend) in hook:
                if not (ph * 4 <= bt < ph * 4 + 4):
                    continue
                if gap and bt - ph * 4 >= 3.0:
                    continue
                tt = t0 + (bt - ph * 4) * spb + rng.uniform(-0.003, 0.003)
                m = deg2midi(v, d)
                place(st["melodic"], koto(m, max(1.2, du * spb + 1.0), bright=.8, bend=bend, seed=int(bt * 4)), tt, db(-8) * vel, pan=0.1)
                if name == "drop2":
                    place(st["melodic"], koto(m - 12, max(1.2, du * spb + 1.0), bright=.5, seed=int(bt * 4) + 1), tt + 0.006, db(-15) * vel, pan=-0.35)
            # contra-arpegio suave de fondo
            for s in range(8):
                beat = s * 0.5 + 0.25
                if gap and beat >= 3.0:
                    break
                d = arp[[0, 2, 1, 3][s % 4]]
                place(st["melodic"], koto(deg2midi(v, d), 0.9, bright=.35, seed=s + 7), t0 + beat * spb, db(-24), pan=-0.5 if s % 2 else 0.5)
        if name == "respiro":
            # notas sueltas de koto, muy espaciadas
            for (bt, d) in [(0, arp[3] + 5), (2.5, arp[2] + 5), (3.0, arp[1] + 5)]:
                place(st["melodic"], koto(deg2midi(v, d), 2.4, bright=.4, seed=int(bt)), t0 + bt * spb, db(-15), pan=0.3)
            if k == 0:  # frase de shakuhachi de 4 compases
                for (bt, m, du, vel) in SHAKU_BREATH[base]:
                    place(st["melodic"], shakuhachi(m, du * spb + 0.25, vel, seed=int(bt)), t0 + bt * spb, db(-12), pan=-0.1)
        if name == "drop" and k == 2:
            for (bt, m, du, vel) in SHAKU_ANSWER[base]:
                place(st["melodic"], shakuhachi(m, du * spb + 0.2, vel, breath=0.3, seed=int(bt) + 20), t0 + bt * spb, db(-11), pan=-0.25)

        # ---------- BAJO
        if name in ("drop", "drop2", "rebuild") or (name == "build" and prog >= 0.5) or name == "respiro":
            if v["style"] == "trap":
                hits = [0, 1.5, 2.75] if bn % 2 == 0 else [0, 0.75, 1.5, 3.5]
                if name in ("build", "respiro", "rebuild"):
                    hits = [0]
                for j, hb in enumerate(hits):
                    if gap and hb >= 3.0:
                        continue
                    nb_ = hits[j + 1] if j + 1 < len(hits) else 4
                    du = (nb_ - hb) * spb
                    if name in ("build", "respiro", "rebuild"):
                        du = bar * 0.95
                    nn = n_of(du)
                    tt = np.arange(nn) / SR
                    f = mtof(broot + (12 if (hb == 3.5) else 0))
                    fr = f * (1 + 0.5 * np.exp(-tt / 0.02))
                    ph_ = 2 * np.pi * np.cumsum(fr) / SR
                    s = np.tanh(2.2 * np.sin(ph_)) * adsr(nn, 0.004, 0.2, 0.75, min(0.08, du * 0.3))
                    s = lp(s, 900)
                    place(st["bass"], s, t0 + hb * spb, db(-6 if name != "respiro" else -12))
            else:
                if name in ("build", "respiro"):
                    offs = [0]
                elif name == "rebuild":
                    offs = [0, 1, 2, 3]
                else:
                    offs = [0.5, 1.5, 2.5, 3.5, 3.75] if k % 2 else [0.5, 1.5, 2.5, 3.5]
                for hb in offs:
                    if gap and hb >= 3.0:
                        continue
                    du = (bar * 0.95) if name in ("build", "respiro") else (0.42 * spb if hb != 3.75 else 0.2 * spb)
                    nn = n_of(du)
                    oct_ = 12 if hb == 3.75 else 0
                    f = mtof(broot + 12 + oct_)
                    tt = np.arange(nn) / SR
                    ph_ = 2 * np.pi * f * tt
                    s = np.sin(ph_) + 0.35 * np.sin(2 * ph_) + 0.5 * np.sin(0.5 * ph_ * 1.0)
                    s = np.tanh(1.6 * s) * adsr(nn, 0.003, 0.08, 0.6, min(0.05, du * 0.3))
                    s = lp(s, 1200)
                    place(st["bass"], s, t0 + hb * spb, db(-5 if name != "respiro" else -11))

        # ---------- BATERÍA
        def K(beat, g=0.0, kk=None):
            if gap and beat >= 3.0:
                return
            tt = t0 + beat * spb
            place(st["drums"], kk if kk is not None else KICK, tt, db(-3 + g))
            kick_times.append(tt)

        def H(beat, g=-15.0, open_=False, pan=0.25):
            if gap and beat >= 3.0:
                return
            place(st["drums"], hat(open_, seed=int(beat * 4) + bn), t0 + beat * spb + rng.uniform(-0.002, 0.002), db(g + 5), pan=pan)

        def C(beat, g=-6.0):
            if gap and beat >= 3.0:
                return
            place(st["drums"], CLAP, t0 + beat * spb, db(g))

        def R(beat, g=-14.0, pan=-0.2):
            if gap and beat >= 3.0:
                return
            place(st["drums"], RIM, t0 + beat * spb, db(g), pan=pan)

        def TK(beat, g=-6.0, f=None, seed=0, pan=0.0):
            if gap and beat >= 3.0:
                return
            place(st["drums"], taiko(f or v["taiko_f"], 1.4, seed=seed), t0 + beat * spb, db(g - 2), pan=pan)

        if name == "intro":
            R(2, -16); R(3, -18)
        elif name == "build":
            if v["style"] == "trap":
                if bn % 2 == 1:
                    TK(0, -9, seed=bn)
                R(2, -13)
                if prog >= 0.3:
                    for s in range(8):
                        H(s * 0.5, -21 + 3 * prog + (2 if s % 2 == 0 else 0))
                if prog >= 0.5:
                    K(0, -3); K(2.5, -5)
                if prog >= 0.75:
                    C(2, -10)
            else:
                if bn % 2 == 1:
                    TK(0, -9, seed=bn)
                R(1.5, -15); R(3.25, -17, pan=0.3)
                if prog >= 0.25:
                    for s in range(4):
                        H(s + 0.5, -18 + 3 * prog, open_=False)
                if prog >= 0.45:
                    for s in range(4):
                        K(s, -6 + 3 * prog)
                if prog >= 0.7:
                    C(1, -10); C(3, -10)
                    for s in range(16):
                        if s % 4 != 2:
                            H(s * 0.25, -24)
            if last_bar:  # redoble de shime-daiko acelerando
                times = 4 - 4 * np.linspace(1, 0, 14) ** 1.6
                for i, bt in enumerate(times):
                    if bt >= 3.0:
                        break
                    place(st["drums"], shime(330 + 4 * i, seed=i), t0 + bt * spb, db(-15 + i * 0.6), pan=(-1) ** i * 0.3)
        elif name in ("drop", "drop2"):
            if v["style"] == "trap":
                for hb in ([0, 1.5, 2.75] if bn % 2 == 0 else [0, 0.75, 1.5, 3.5]):
                    K(hb, 0 if hb == 0 else -2)
                C(2, -5)
                R(3.75, -16) if bn % 2 else None
                for s in range(8):
                    H(s * 0.5, -14 if s % 2 == 0 else -17)
                if bn % 2 == 1:
                    for s in [3.25, 3.75]:
                        H(s, -19)
                if k % 4 == 3:
                    for s in [3, 3 + 1 / 3, 3 + 2 / 3]:
                        H(s, -17)
                if k % 2 == 0:
                    TK(0, -8, seed=bn)
                if k % 4 == 3:
                    TK(3.5, -10, f=v["taiko_f"] * 1.25, seed=bn + 50, pan=0.3)
                if name == "drop2":
                    H(1.5, -20, open_=True, pan=-0.3); H(3.5, -20, open_=True, pan=-0.3)
            else:
                for s in range(4):
                    K(s, 0 if s == 0 else -1)
                C(1, -5); C(3, -5)
                for s in range(4):
                    H(s + 0.5, -15, open_=True, pan=-0.25)
                for s in range(16):
                    if s % 2 == 1:
                        H(s * 0.25, -21, pan=0.35)
                R(2.75, -15); R(3.25, -17, pan=0.3) if k % 2 else None
                if k % 4 == 0:
                    TK(0, -8, seed=bn)
                if k % 4 == 3:
                    TK(3.5, -11, f=v["taiko_f"] * 1.25, seed=bn + 50, pan=0.3)
        if name in ("drop", "drop2"):
            for s16 in range(16):
                if gap and s16 >= 12:
                    break
                place(st["drums"], SHAKER, t0 + s16 * spb / 4 + rng.uniform(-0.003, 0.003), db(-17 if s16 % 4 == 2 else -22), pan=-0.4)
        if name == "respiro":
            if k % 2 == 0:
                TK(0, -11, seed=bn)
            R(2, -18)
            if k == L - 1:  # vuelve el pulso suave al final del respiro
                for s in range(4):
                    H(s + 0.5, -24)
        elif name == "rebuild":
            ks = 4 if prog < 0.6 else 8
            for s in range(ks):
                K(s * 4 / ks, -6 + 4 * prog)
            for s in range(16):
                H(s * 0.25, -24 + 6 * prog)
            C(1, -10); C(3, -10)
            if prog >= 0.6:
                times = np.linspace(0, 3, 13)[:-1]
                for i, bt in enumerate(times):
                    place(st["drums"], shime(340 + 5 * i, seed=i + 5), t0 + bt * spb, db(-16 + i * 0.5), pan=(-1) ** i * 0.3)

        # ---------- FX de transición
        if last_bar and nxt in ("drop", "drop2"):
            rlen = min(bar * (2 if L >= 3 else 1), 4.2)
            place(st["fx"], noise_riser(rlen - spb, seed=bn), T(bn + 1) - rlen, db(-15))
            place(st["fx"], reverse_swell(1.0, seed=bn), T(bn + 1) - 1.0, db(-17))
        if last_bar and name == "rebuild" and nxt == "salida":
            place(st["fx"], noise_riser(bar - spb * 0.5, seed=bn), T(bn + 1) - bar, db(-16))
            place(st["fx"], reverse_swell(1.0, seed=bn), T(bn + 1) - 1.0, db(-18))
        if name in ("drop", "drop2") and k == 0:
            place(st["fx"], sub_boom(1.8), t0, db(-10))
            place(st["fx"], crash(2.4, seed=bn), t0, db(-15))
            place(st["drums"], taiko(v["taiko_f"], 1.8, seed=bn + 9), t0, db(-4))
        if name == "respiro" and k == 0:
            place(st["fx"], crash(3.0, seed=bn), t0, db(-19))

    # ---------------------------------------------------- salida (nota sostenida para el CTA)
    ts = T(out_bar)
    tail = dur - ts
    place(st["drums"], taiko(v["taiko_f"], 2.2, seed=77), ts, db(-4))
    place(st["fx"], sub_boom(2.4, f_end=36), ts, db(-9))
    place(st["fx"], crash(3.2, seed=9), ts, db(-17))
    # sararin descendente que se asienta
    for i, d in enumerate(range(10, 2, -1)):
        place(st["melodic"], koto(deg2midi(v, d), 3.0, bright=.6, seed=i + 30), ts + 0.015 + i * 0.035, db(-12), pan=0.4 - i * 0.1)
    # acorde final sostenido + raíz del koto que se repite muy suave (sin cambios bruscos)
    pc = pad_chord(v["final_chord"], tail + 0.5, bright=1800, seed=99)
    env = np.interp(np.arange(len(pc)) / SR, [0, 0.4, tail - 3.2, tail], [0, 1, 0.9, 0])
    place(st["pad"], pc * env[:, None], ts, db(-11))
    bn_ = n_of(tail)
    tt = np.arange(bn_) / SR
    f = mtof(v["final_bass"])
    s = np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)
    s *= np.interp(tt, [0, 0.05, tail - 3.5, tail], [0, 1, 0.75, 0])
    place(st["bass"], s, ts, db(-15))
    place(st["melodic"], shakuhachi(SHAKU_FINAL[base], tail - 0.6, 0.85, vib=0.15, breath=0.32, seed=5, fade_out=3.4), ts + 0.6, db(-13), pan=-0.1)
    for j, bt in enumerate([4, 10]):
        tk = ts + bt * spb
        if tk < dur - 3.5:
            place(st["melodic"], koto(deg2midi(v, 5), 3.0, bright=.35, seed=j + 60), tk, db(-19), pan=0.3)

    # ---------------------------------------------------- reverb, sidechain, stems
    ir_hall = make_ir(2.6 if base == "A" else 2.0, 0.025, 5000, seed=3)
    ir_room = make_ir(1.1, 0.01, 7000, seed=4)
    st["melodic"] = peak_eq(st["melodic"], 7000, 4, 0.6)
    st["pad"] = hp(st["pad"], 160, 2)
    st["melodic"] = st["melodic"] + reverb(st["melodic"], ir_hall, 0.38)
    st["pad"] = st["pad"] + reverb(st["pad"], ir_hall, 0.25)
    drums_dry = st["drums"].copy()
    st["drums"] = st["drums"] + reverb(hp(drums_dry, 250), ir_room, 0.16)
    st["fx"] = st["fx"] + reverb(st["fx"], ir_hall, 0.2)

    tt = np.arange(len(st["pad"])) / SR
    duck = np.ones(len(tt))
    depth = 0.45 if base == "B" else 0.28
    for tk in kick_times:
        i = n_of(tk)
        j = min(len(duck), i + n_of(0.35))
        x = np.arange(j - i) / SR
        duck[i:j] = np.minimum(duck[i:j], 1 - depth * np.exp(-x / 0.11))
    st["pad"] *= duck[:, None]
    st["bass"] *= (1 - (1 - duck) * 0.8)[:, None]

    # fx de transición se reporta dentro del stem de batería (4 stems pedidos)
    stems = {"drums": st["drums"] + st["fx"], "bass": st["bass"], "melodic": st["melodic"], "pad": st["pad"]}
    stems = {k: x[:N] for k, x in stems.items()}
    # balance de stems por loudness (relativo, antes del master)
    import pyloudnorm as pyln
    meter = pyln.Meter(SR)
    target = {"drums": -17.0, "bass": -19.5, "melodic": -18.0, "pad": -23.5}
    if base == "A":
        target.update(drums=-17.5, melodic=-17.5, pad=-23.0, bass=-21.0)
    for k_ in stems:
        Lk = meter.integrated_loudness(stems[k_])
        stems[k_] = stems[k_] * db(target[k_] - Lk)
    # final limpio: fade-out de los últimos 1.2 s y 0.3 s de silencio
    fo = np.interp(np.arange(N) / SR, [0, dur - 1.5, dur - 0.3, dur], [1, 1, 0, 0])
    stems = {k_: x * fo[:, None] for k_, x in stems.items()}
    mix, stems, gcurve = master_to(stems, -14.0, -1.0)

    os.makedirs(STEMS, exist_ok=True)
    sf.write(os.path.join(OUT, v["name"] + ".wav"), mix.astype(np.float32), SR, subtype="PCM_24")
    for k_, x in stems.items():
        sf.write(os.path.join(STEMS, f"{v['name']}_{k_}.wav"), x.astype(np.float32), SR, subtype="PCM_24")

    # ---------------------------------------------------- beat grid
    beats = [round(i * spb, 4) for i in range(int(dur / spb) + 1) if i * spb < dur]
    downs = [round(i * bar, 4) for i in range(int(dur / bar) + 1) if i * bar < dur]
    sections = []
    for name, s0, s1 in secs:
        sections.append(dict(nombre=name, compas_inicio=s0, compas_fin=min(s1, dur / bar), inicio_s=round(T(s0), 3),
                             fin_s=round(min(T(s1), dur), 3)))
    grid = dict(
        archivo=v["name"] + ".wav", bpm=bpm, compas="4/4", duracion_s=dur, sample_rate=SR,
        escala=v["scale_name"], acordes=v["chord_names"],
        segundos_por_beat=round(spb, 6), segundos_por_compas=round(bar, 6),
        beats=beats, inicios_de_compas=downs, secciones=sections,
        golpes_clave_s=dict(
            golpe_entrada=0.0,
            drops=[round(T(s0), 3) for n_, s0, _ in secs if n_ in ("drop", "drop2")],
            silencio_pre_drop=[round(T(s0) - spb, 3) for n_, s0, _ in secs if n_ in ("drop", "drop2")],
            golpe_salida=round(ts, 3),
            nota_sostenida_desde=round(ts + 0.6, 3),
            fade_final_desde=round(dur - 1.5, 3),
        ),
        licencia="Original, sintetizada internamente con numpy/scipy (sin muestras de terceros).",
    )
    with open(os.path.join(OUT, v["name"] + ".beats.json"), "w") as fh:
        json.dump(grid, fh, ensure_ascii=False, indent=1)
    print("ok", v["name"], "kicks", len(kick_times))
    return v["name"]


KICK = None
SHAKER = None
CLAP = None
RIM = None


if __name__ == "__main__":
    keys = sys.argv[1:] or ["A", "B", "A40", "B40"]
    for key in keys:
        if key.startswith("A"):
            KICK = kick(0.5, f_end=50, tau_a=0.26, click=0.45)
            CLAP = clap(0.4, tone=1300)
        else:
            KICK = kick(0.40, f_end=52, tau_a=0.2, click=0.5)
            CLAP = clap(0.3, tone=1500)
        RIM = rim()
        _r = np.random.default_rng(5)
        _n = n_of(0.06)
        SHAKER = fade(bp(_r.standard_normal(_n), 5000, 14000) * env_exp(_n, 0.012, 0.004), 0.003, 0.01)
        SHAKER /= np.abs(SHAKER).max()
        render(key)
