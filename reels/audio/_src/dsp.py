"""Biblioteca DSP mínima para sintetizar la música y los SFX de Morishita.

Todo se genera desde cero con numpy/scipy (osciladores, ruido, Karplus-Strong,
filtros, reverb por convolución con IR sintética). No se usa ninguna muestra
grabada ni ningún banco de sonidos: el audio resultante es obra original.
"""
import numpy as np
from scipy import signal

SR = 48000
RNG = np.random.default_rng(1985)


def n_of(sec):
    return int(round(sec * SR))


def tvec(dur):
    return np.arange(n_of(dur)) / SR


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)


# ---------------------------------------------------------------- filtros
def _sos(kind, f, order=2):
    if isinstance(f, (list, tuple)):
        f = [min(max(x, 10), SR / 2 - 100) for x in f]
    else:
        f = min(max(f, 10), SR / 2 - 100)
    return signal.butter(order, f, btype=kind, fs=SR, output="sos")


def lp(x, f, order=2):
    return signal.sosfilt(_sos("lowpass", f, order), x, axis=0)


def hp(x, f, order=2):
    return signal.sosfilt(_sos("highpass", f, order), x, axis=0)


def bp(x, f1, f2, order=2):
    return signal.sosfilt(_sos("bandpass", [f1, f2], order), x, axis=0)


def peak_eq(x, f, gain_db, q=1.0):
    """Peaking EQ (RBJ)."""
    A = 10 ** (gain_db / 40)
    w0 = 2 * np.pi * f / SR
    al = np.sin(w0) / (2 * q)
    b = [1 + al * A, -2 * np.cos(w0), 1 - al * A]
    a = [1 + al / A, -2 * np.cos(w0), 1 - al / A]
    return signal.lfilter(np.array(b) / a[0], np.array(a) / a[0], x, axis=0)


def svf_sweep(x, f_curve, q=0.7, mode="bp"):
    """Filtro de estado variable (Chamberlin) con frecuencia variable por muestra."""
    y = np.zeros_like(x)
    lo = bd = 0.0
    damp = 1.0 / q
    fc = 2 * np.sin(np.pi * np.clip(f_curve, 20, SR / 6) / SR)
    xs = x.tolist()
    out = [0.0] * len(xs)
    fl = fc.tolist()
    for i, v in enumerate(xs):
        f = fl[i]
        lo += f * bd
        hi = v - lo - damp * bd
        bd += f * hi
        out[i] = bd if mode == "bp" else (lo if mode == "lp" else hi)
    y[:] = out
    return y


# ---------------------------------------------------------------- utilidades
def env_exp(n, tau, attack=0.002):
    t = np.arange(n) / SR
    e = np.exp(-t / tau)
    na = max(1, n_of(attack))
    e[:na] *= np.linspace(0, 1, na)
    return e


def adsr(n, a, d, s, r, hold=None):
    """Envolvente ADSR de longitud n; release al final."""
    na, nd, nr = n_of(a), n_of(d), n_of(r)
    ns = max(0, n - na - nd - nr)
    e = np.concatenate([
        np.linspace(0, 1, na, endpoint=False) if na else [],
        np.linspace(1, s, nd, endpoint=False) if nd else [],
        np.full(ns, s),
        np.linspace(s, 0, nr) if nr else [],
    ])
    if len(e) < n:
        e = np.pad(e, (0, n - len(e)))
    return e[:n]


def fade(x, fin=0.002, fout=0.01):
    x = x.copy()
    a, b = n_of(fin), n_of(fout)
    if a:
        x[:a] *= np.linspace(0, 1, a)[:, None] if x.ndim == 2 else np.linspace(0, 1, a)
    if b:
        x[-b:] *= np.linspace(1, 0, b)[:, None] if x.ndim == 2 else np.linspace(1, 0, b)
    return x


def pan_st(x, pan=0.0):
    th = (pan + 1) * np.pi / 4
    return np.stack([x * np.cos(th), x * np.sin(th)], axis=1) * np.sqrt(2)


def place(buf, sig, t, gain=1.0, pan=0.0):
    if sig.ndim == 1:
        sig = pan_st(sig, pan)
    i = n_of(t)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    if i < 0:
        sig = sig[-i:]
        j = min(len(buf), len(sig))
        i = 0
    buf[i:j] += sig[: j - i] * gain


def db(x):
    return 10 ** (x / 20)


def noise(n, rng=RNG):
    return rng.standard_normal(n)


def pink(n, rng=RNG):
    w = rng.standard_normal(n)
    f = np.fft.rfftfreq(n, 1 / SR)
    W = np.fft.rfft(w)
    W[1:] /= np.sqrt(f[1:])
    W[0] = 0
    p = np.fft.irfft(W, n)
    return p / (np.max(np.abs(p)) + 1e-12)


def normalize(x, peak=1.0):
    m = np.max(np.abs(x)) + 1e-12
    return x * (peak / m)


# ---------------------------------------------------------------- reverb
def make_ir(t60=2.2, predelay=0.02, damp_hz=5500, width=1.0, seed=7, er=True):
    rng = np.random.default_rng(seed)
    n = n_of(t60 * 1.1)
    t = np.arange(n) / SR
    env = 10 ** (-3 * t / t60)
    L = rng.standard_normal(n) * env
    R = rng.standard_normal(n) * env
    # amortiguación de agudos: el final es más oscuro que el principio
    Lb, Rb = lp(L, damp_hz), lp(R, damp_hz)
    Ld, Rd = lp(L, damp_hz / 4), lp(R, damp_hz / 4)
    mix = np.clip(t / (t60 * 0.6), 0, 1)
    L = Lb * (1 - mix) + Ld * mix
    R = Rb * (1 - mix) + Rd * mix
    R = width * R + (1 - width) * L
    ir = np.stack([L, R], 1)
    if er:  # reflexiones tempranas
        for k, (dt, g) in enumerate([(0.011, .5), (0.017, .4), (0.023, .35), (0.031, .3), (0.043, .25)]):
            i = n_of(dt)
            ir[i, k % 2] += g * 3
    ir = np.concatenate([np.zeros((n_of(predelay), 2)), ir])
    ir = hp(ir, 180)
    return ir / np.sqrt(np.sum(ir ** 2) / 2)


def reverb(x, ir, wet=0.25):
    if x.ndim == 1:
        x = pan_st(x)
    mono = x.mean(1)
    yl = signal.fftconvolve(mono, ir[:, 0])[: len(x)]
    yr = signal.fftconvolve(mono, ir[:, 1])[: len(x)]
    return np.stack([yl, yr], 1) * wet


# ---------------------------------------------------------------- instrumentos
_ks_cache = {}


def koto(midi, dur=2.0, vel=1.0, bright=0.6, t60=None, bend=None, seed=0):
    """Pluck tipo koto por Karplus-Strong. bend: (t_inicio, semitonos, t_rampa) = oshide."""
    f = mtof(midi)
    key = (round(midi, 2), round(dur, 2), round(bright, 2), bend, seed % 4)
    if key in _ks_cache:
        return _ks_cache[key] * vel
    if t60 is None:
        t60 = float(np.clip(3.2 - (midi - 55) * 0.05, 1.2, 3.6))
    P = SR / f
    N = int(np.floor(P - 0.5))
    f0 = SR / (N + 0.5)
    rng = np.random.default_rng(1000 + seed)
    total = n_of(dur * 1.06 * 2 ** (2.5 / 12)) + N + 4
    exc = rng.uniform(-1, 1, N)
    # brillo del ataque (uña/plectro tsume): filtro de un polo
    a = 1 - bright
    exc = signal.lfilter([1 - a], [1, -a], exc)
    # posición del punteo (comb) -> timbre nasal del koto
    k = max(1, int(N * 0.12))
    exc = exc - np.roll(exc, k) * 0.9
    exc -= exc.mean()
    y = np.zeros(total)
    y[:N] = exc
    g = 10 ** (-3 / (t60 * f0))
    blend = 0.5 + 0.08 * bright  # >0.5 = más armónicos sostenidos
    for s in range(N, total, N):
        e = min(s + N, total)
        idx = np.arange(s, e)
        y[s:e] = g * (blend * y[idx - N] + (1 - blend) * y[idx - N - 1])
    # afinación exacta + oshide (doblar la cuerda tras el punteo)
    n = n_of(dur)
    t = np.arange(n) / SR
    semis = np.zeros(n)
    if bend is not None:
        tb, st, tr = bend
        semis = st * np.clip((t - tb) / tr, 0, 1) ** 0.7
    # leve inestabilidad de afinación de cuerda de seda
    semis += 0.04 * np.exp(-t / 0.08)
    rate = (f / f0) * 2 ** (semis / 12)
    pos = np.concatenate([[0], np.cumsum(rate)[:-1]])
    out = np.interp(pos, np.arange(total), y)
    # cuerpo de madera de paulownia (resonancias) + presencia del ataque
    out = out + 0.35 * peak_eq(out, 240, 4, 1.2) - 0.35 * out
    out = peak_eq(out, 2600, 3, 1.0)
    click = noise(n_of(0.006), rng) * np.linspace(1, 0, n_of(0.006)) * 0.15 * bright
    out[: len(click)] += hp(click, 2500)
    out = fade(out, 0.0005, 0.03)
    out = out / (np.max(np.abs(out)) + 1e-9)
    _ks_cache[key] = out
    return out * vel


def shakuhachi(midi, dur, vel=1.0, scoop=-0.7, vib=0.22, breath=0.35, seed=0, fade_out=0.35):
    """Flauta tipo shakuhachi: tono casi senoidal + aire (muraiki) + meri al inicio + vibrato tardío."""
    rng = np.random.default_rng(300 + seed)
    n = n_of(dur)
    t = np.arange(n) / SR
    f = mtof(midi)
    semis = scoop * np.exp(-t / 0.09)
    vdepth = vib * np.clip((t - 0.45) / 0.6, 0, 1)
    vrate = 4.6 + 0.8 * np.clip((t - 0.5) / 2, 0, 1)
    semis = semis + vdepth * np.sin(2 * np.pi * np.cumsum(vrate) / SR)
    semis += 0.03 * lp(rng.standard_normal(n), 3) * 30  # deriva lenta
    ph = 2 * np.pi * np.cumsum(f * 2 ** (semis / 12)) / SR
    tone = np.sin(ph) + 0.18 * np.sin(2 * ph + 0.3) + 0.10 * np.sin(3 * ph + 1.1) + 0.03 * np.sin(4 * ph)
    amp = adsr(n, 0.12, 0.25, 0.85, fade_out)
    swell = 1 + 0.12 * np.sin(2 * np.pi * 0.35 * t)
    nz = rng.standard_normal(n)
    air = bp(nz, 1800, 7000) * 0.5 + bp(nz, f * 0.8, f * 1.6) * 1.2
    burst = np.exp(-t / 0.07) * 1.6  # golpe de aire del ataque
    out = amp * swell * (tone * (1 - breath) + air * breath * (0.6 + burst)) * vel
    return fade(out, 0.002, 0.05)


def pad_chord(midis, dur, bright=2600, voices=3, detune=8, seed=0):
    """Pad cálido: sierras aditivas desafinadas, estéreo."""
    rng = np.random.default_rng(500 + seed)
    n = n_of(dur)
    t = np.arange(n) / SR
    L = np.zeros(n)
    R = np.zeros(n)
    for m in midis:
        f = mtof(m)
        for v in range(voices):
            cents = (v - (voices - 1) / 2) * detune + rng.uniform(-2, 2)
            fv = f * 2 ** (cents / 1200)
            kmax = int(min(40, 9000 / fv))
            ph0 = rng.uniform(0, 2 * np.pi, kmax + 1)
            w = np.zeros(n)
            for k in range(1, kmax + 1):
                amp = (1 / k) * np.exp(-(k * fv) / bright)
                w += amp * np.sin(2 * np.pi * k * fv * t + ph0[k])
            p = (v - (voices - 1) / 2) / max(1, (voices - 1) / 2) * 0.7
            th = (p + 1) * np.pi / 4
            L += w * np.cos(th)
            R += w * np.sin(th)
    st = np.stack([L, R], 1)
    return st / (np.max(np.abs(st)) + 1e-9)


# ---------------------------------------------------------------- percusión
def kick(dur=0.45, f_end=46, f_start=170, tau_p=0.028, tau_a=0.32, click=0.35, drive=1.4):
    n = n_of(dur)
    t = np.arange(n) / SR
    f = f_end + (f_start - f_end) * np.exp(-t / tau_p)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * env_exp(n, tau_a, 0.001)
    body = np.tanh(drive * body) / np.tanh(drive)
    c = hp(noise(n_of(0.004)), 3000) * click
    body[: len(c)] += c * np.linspace(1, 0, len(c))
    return fade(body, 0.0003, 0.02)


def sub_boom(dur=2.2, f_end=38, f_start=90, seed=0):
    n = n_of(dur)
    t = np.arange(n) / SR
    f = f_end + (f_start - f_end) * np.exp(-t / 0.12)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * env_exp(n, 0.65, 0.002)
    body = np.tanh(1.8 * body)
    rng = np.random.default_rng(40 + seed)
    nz = lp(rng.standard_normal(n), 600) * env_exp(n, 0.09) * 2.5
    out = body + nz + 0.4 * np.sin(2 * ph) * env_exp(n, 0.25)
    return fade(out / np.max(np.abs(out)), 0.0005, 0.2)


def taiko(f=68, dur=1.6, vel=1.0, seed=0):
    """O-daiko: modos inharmónicos de membrana + golpe de baqueta (bachi)."""
    rng = np.random.default_rng(60 + seed)
    n = n_of(dur)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for ratio, amp, tau in [(1.0, 1.0, 0.55), (1.59, 0.45, 0.22), (2.14, 0.30, 0.14), (2.30, 0.22, 0.11), (2.65, 0.15, 0.08), (3.16, 0.08, 0.05)]:
        fr = f * ratio * (1 + 0.35 * np.exp(-t / 0.04))
        out += amp * np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / tau)
    hit = lp(rng.standard_normal(n), 900) * np.exp(-t / 0.018) * 1.2
    skin = bp(rng.standard_normal(n), 150, 600) * np.exp(-t / 0.12) * 0.5
    out = out + hit + skin
    out = np.tanh(1.3 * out)
    return fade(out / np.max(np.abs(out)), 0.0003, 0.1) * vel


def shime(f=330, dur=0.25, vel=1.0, seed=0):
    """Shime-daiko: tambor agudo y tenso para redobles."""
    rng = np.random.default_rng(80 + seed)
    n = n_of(dur)
    t = np.arange(n) / SR
    tone = np.sin(2 * np.pi * f * t * (1 + 0.2 * np.exp(-t / 0.01))) * np.exp(-t / 0.05)
    tone += 0.4 * np.sin(2 * np.pi * f * 1.62 * t) * np.exp(-t / 0.03)
    nz = bp(rng.standard_normal(n), 800, 5000) * np.exp(-t / 0.015)
    return fade((tone + 0.8 * nz) / 2, 0.0002, 0.02) * vel


def clap(dur=0.35, seed=0, tone=1400):
    rng = np.random.default_rng(90 + seed)
    n = n_of(dur)
    t = np.arange(n) / SR
    nz = rng.standard_normal(n)
    e = np.zeros(n)
    for k, dt in enumerate([0, 0.009, 0.019, 0.027]):
        e += (t >= dt) * np.exp(-np.clip(t - dt, 0, None) / (0.006 if k < 3 else 0.11))
    out = bp(nz, tone * 0.6, tone * 3.2) * e
    out = peak_eq(out, tone, 4, 1.5)
    return fade(out / np.max(np.abs(out)), 0.0002, 0.03)


def rim(dur=0.12, f=1750, seed=0):
    rng = np.random.default_rng(95 + seed)
    n = n_of(dur)
    t = np.arange(n) / SR
    out = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.012) + 0.6 * np.sin(2 * np.pi * 520 * t) * np.exp(-t / 0.02)
    out += hp(rng.standard_normal(n), 2000) * np.exp(-t / 0.003) * 0.8
    return fade(out / np.max(np.abs(out)), 0.0001, 0.01)


_hat_cache = {}


def hat(open_=False, seed=0):
    key = (open_, seed % 6)
    if key in _hat_cache:
        return _hat_cache[key]
    rng = np.random.default_rng(120 + seed % 6)
    dur = 0.45 if open_ else 0.09
    n = n_of(dur)
    t = np.arange(n) / SR
    metal = np.zeros(n)
    for fr in [205.3, 304.4, 369.6, 522.7, 540.0, 800.0]:
        metal += np.sign(np.sin(2 * np.pi * fr * 1.6 * t + rng.uniform(0, 6)))
    nz = rng.standard_normal(n)
    out = hp(0.6 * metal / 6 + nz, 7000, 4)
    out = peak_eq(out, 10500, 3, 1)
    out *= np.exp(-t / (0.16 if open_ else 0.018))
    out = fade(out / np.max(np.abs(out)), 0.0002, 0.01)
    _hat_cache[key] = out
    return out


def noise_riser(dur, f0=300, f1=9000, seed=0, q=1.4):
    rng = np.random.default_rng(140 + seed)
    n = n_of(dur)
    t = np.arange(n) / SR
    x = rng.standard_normal(n)
    fc = f0 * (f1 / f0) ** ((t / dur) ** 1.6)
    y = svf_sweep(x, fc, q=q, mode="bp")
    amp = (t / dur) ** 2.2
    y = y * amp
    return y / (np.max(np.abs(y)) + 1e-9)


def reverse_swell(dur=1.2, seed=0):
    """Platillo invertido sintético (ruido metálico con envolvente creciente)."""
    rng = np.random.default_rng(160 + seed)
    n = n_of(dur)
    t = np.arange(n) / SR
    x = hp(rng.standard_normal(n), 4000, 2) + 0.4 * bp(rng.standard_normal(n), 1500, 4000)
    e = np.exp((t - dur) / (dur * 0.28))
    y = x * e
    y[-n_of(0.004):] *= np.linspace(1, 0, n_of(0.004))
    return y / np.max(np.abs(y))


def crash(dur=2.5, seed=0):
    rng = np.random.default_rng(170 + seed)
    n = n_of(dur)
    t = np.arange(n) / SR
    x = hp(rng.standard_normal(n), 3500, 2)
    x = peak_eq(x, 6000, 4, 0.8)
    y = x * np.exp(-t / 0.7)
    return fade(y / np.max(np.abs(y)), 0.0005, 0.3)


# ---------------------------------------------------------------- master / medición
def true_peak(x, os=4):
    up = signal.resample_poly(x, os, 1, axis=0)
    return float(np.max(np.abs(up)))


def limiter_gain(x, ceiling_lin, look=0.004, smooth=0.003):
    """Ganancia de limitador lookahead (min-filter + suavizado), sin bucles."""
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    os = 4
    up = np.abs(signal.resample_poly(x, os, 1, axis=0)).max(1)
    pk = up.reshape(-1, os).max(1) if len(up) % os == 0 else np.pad(up, (0, os - len(up) % os)).reshape(-1, os).max(1)
    pk = pk[: len(x)]
    g = np.minimum(1.0, ceiling_lin / (pk + 1e-12))
    w = n_of(look) * 2 + 1
    g = minimum_filter1d(g, w, mode="nearest")
    g = uniform_filter1d(g, n_of(smooth) * 2 + 1, mode="nearest")
    return g


def master_to(x_stems, target_lufs=-14.0, ceiling_dbtp=-1.0, hp_hz=28):
    """Devuelve (mix, stems_procesados, ganancia_curva). Mismas ganancias para mezcla y stems."""
    import pyloudnorm as pyln
    meter = pyln.Meter(SR)
    stems = {k: hp(v, hp_hz, 2) for k, v in x_stems.items()}
    mix = sum(stems.values())
    ceiling = db(ceiling_dbtp - 0.25)
    gain_total = 1.0
    gcurve = np.ones(len(mix))
    for _ in range(8):
        cur = mix * gain_total
        g = limiter_gain(cur, ceiling)
        lim = cur * g[:, None]
        L = meter.integrated_loudness(lim)
        if abs(L - target_lufs) < 0.05:
            break
        gain_total *= db(target_lufs - L)
    gcurve = g * gain_total
    out = mix * gcurve[:, None]
    tp = true_peak(out)
    if tp > db(ceiling_dbtp):
        s = db(ceiling_dbtp - 0.05) / tp
        gcurve *= s
        out *= s
    stems = {k: v * gcurve[:, None] for k, v in stems.items()}
    return out, stems, gcurve
