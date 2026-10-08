#!/tmp/claude-0/venv/bin/python
"""Voz en off gratuita con edge-tts (Microsoft) para los reels de Morishita.

Salidas en --out:
  <id>.mp3            audio final (48 kHz mono, 192 kbps)
  <id>.wav            audio final PCM 16 bits, 48 kHz mono (para HyperFrames)
  <id>.words.json     [{"word","start","end"}] en segundos (eventos WordBoundary)
  <id>.meta.json      voz, rate, pitch, volume, modo, duración, frases y pausas
  <id>.transcript.json (solo con --verify) transcripción faster-whisper + diff

Uso:
  # texto directo o archivo, una sola síntesis
  tts.py --text "Cuatro asientos. Sábado y domingo." --voice es-MX-JorgeNeural \
         --rate +8% --pitch -2Hz --id prueba --out voz/muestras --verify
  tts.py --file guion.txt --voice es-MX-JorgeNeural --id r01 --out voz

  # por frases: una frase por línea; pausas exactas con "[pausa 0.4]"
  # (líneas vacías se ignoran; "#" al inicio = comentario)
  tts.py --file guion-frases.txt --por-frases --pausa-default 0.25 \
         --voice es-MX-JorgeNeural --rate +8% --id r01 --out voz --verify

Notas:
  - Requiere red por el proxy (HTTPS_PROXY); edge-tts 7.2.8.
  - En --por-frases se recorta el silencio inicial/final de cada frase
    (umbral -55 dBFS, margen 80 ms; protege fricativas suaves como la F inicial) para que las pausas sean exactas,
    y los timestamps se recalculan con el offset de cada frase.
  - Glosario por defecto: voz/pronuncia.json (p. ej. nigiri -> niguiri). Se
    desactiva con --sin-glosario. --pronuncia "palabra=variante" (repetible)
    agrega reglas. Solo cambian el texto enviado al TTS; words.json conserva la
    palabra del guion original.
"""
from __future__ import annotations

import argparse
import asyncio
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np
import soundfile as sf

SR = 48000
PAUSA_RE = re.compile(r"^\[\s*pausa\s+([0-9]*\.?[0-9]+)\s*s?\s*\]$", re.I)


# ----------------------------------------------------------------- síntesis
async def _sintetiza(texto: str, voice: str, rate: str, pitch: str, volume: str,
                     reintentos: int = 3):
    import edge_tts

    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    ultimo = None
    for intento in range(reintentos):
        try:
            com = edge_tts.Communicate(texto, voice, rate=rate, pitch=pitch,
                                       volume=volume, boundary="WordBoundary",
                                       proxy=proxy)
            audio = bytearray()
            palabras = []
            async for ev in com.stream():
                if ev["type"] == "audio":
                    audio.extend(ev["data"])
                elif ev["type"] == "WordBoundary":
                    ini = ev["offset"] / 1e7  # unidades de 100 ns
                    palabras.append({"word": ev["text"], "start": ini,
                                     "end": ini + ev["duration"] / 1e7})
            if not audio:
                raise RuntimeError("edge-tts no devolvió audio")
            return bytes(audio), palabras
        except Exception as e:  # red inestable: reintenta
            ultimo = e
            await asyncio.sleep(1.5 * (intento + 1))
    raise RuntimeError(f"edge-tts falló tras {reintentos} intentos: {ultimo}")


def _mp3_a_array(mp3: bytes) -> np.ndarray:
    """Decodifica MP3 a float32 mono 48 kHz con ffmpeg."""
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", "pipe:0", "-ac", "1",
                        "-ar", str(SR), "-f", "f32le", "pipe:1"],
                       input=mp3, capture_output=True, check=True)
    return np.frombuffer(p.stdout, dtype=np.float32).copy()


def _recorta(x: np.ndarray, umbral_db: float = -55.0, margen: float = 0.08):
    """Recorta silencio al inicio y al final. Devuelve (audio, segundos quitados al inicio)."""
    if x.size == 0:
        return x, 0.0
    win = int(0.01 * SR)
    n = len(x) // win
    if n == 0:
        return x, 0.0
    rms = np.sqrt(np.mean(x[: n * win].reshape(n, win) ** 2, axis=1) + 1e-12)
    activo = np.where(20 * np.log10(rms) > umbral_db)[0]
    if activo.size == 0:
        return x, 0.0
    a = max(0, activo[0] * win - int(margen * SR))
    b = min(len(x), (activo[-1] + 1) * win + int(margen * SR))
    return x[a:b], a / SR


def _guarda(x: np.ndarray, base: Path):
    sf.write(str(base) + ".wav", x, SR, subtype="PCM_16")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(base) + ".wav",
                    "-ac", "1", "-ar", str(SR), "-c:a", "libmp3lame", "-b:a", "192k",
                    str(base) + ".mp3"], check=True)


# --------------------------------------------------------- texto y guiones
def _aplica_pronuncia(texto: str, reglas: dict[str, str]) -> str:
    for orig, var in reglas.items():
        texto = re.sub(rf"(?<!\w){re.escape(orig)}(?!\w)", var, texto, flags=re.I)
    return texto


def _tokens(texto: str) -> list[str]:
    return re.findall(r"[\w%$’'+]+", texto, flags=re.UNICODE)


def _restaura_palabras(palabras: list[dict], texto_original: str) -> list[dict]:
    """Si se usaron variantes de pronunciación, mapea las palabras del TTS al guion original."""
    orig = _tokens(texto_original)
    if len(orig) == len(palabras):
        for p, o in zip(palabras, orig):
            if _norm(p["word"]) != _norm(o):
                p["tts"] = p["word"]
                p["word"] = o
    return palabras


def _lee_frases(texto: str, pausa_default: float):
    """Devuelve lista de ('frase', str) y ('pausa', seg). Entre frases sin pausa explícita
    se inserta pausa_default."""
    items = []
    for linea in texto.splitlines():
        l = linea.strip()
        if not l or l.startswith("#"):
            continue
        m = PAUSA_RE.match(l)
        if m:
            items.append(("pausa", float(m.group(1))))
        else:
            if items and items[-1][0] == "frase":
                items.append(("pausa", pausa_default))
            items.append(("frase", l))
    return items


# ------------------------------------------------------------- verificación
def _fon(s: str) -> str:
    """Clave fonética aproximada del español de México (para no penalizar grafías
    equivalentes como omacase/omakase o morisita/morishita en el reporte)."""
    s = _norm(s)
    for a, b in (("sh", "s"), ("ss", "s"), ("qu", "k"), ("gui", "gi"), ("gue", "ge"),
                 ("ce", "se"), ("ci", "si"), ("z", "s"), ("c", "k"), ("v", "b"),
                 ("h", ""), ("ll", "y")):
        s = s.replace(a, b)
    return s


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^\w%]", "", s)


def verifica(wav: Path, guion: str, salida: Path, modelo: str = "small"):
    from faster_whisper import WhisperModel

    m = WhisperModel(modelo, device="cpu", compute_type="int8")
    # Se pasa un array 16 kHz (evita la decodificación con PyAV, incompatible
    # en el venv compartido: open() got an unexpected keyword 'metadata_errors').
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(wav), "-ac", "1", "-ar",
                          "16000", "-f", "f32le", "pipe:1"], capture_output=True,
                         check=True).stdout
    audio16 = np.frombuffer(pcm, dtype=np.float32).copy()
    segs, info = m.transcribe(audio16, language="es", word_timestamps=True,
                              beam_size=5, vad_filter=False,
                              initial_prompt=None, condition_on_previous_text=False)
    palabras, texto = [], []
    for s in segs:
        texto.append(s.text.strip())
        for w in s.words or []:
            palabras.append({"word": w.word.strip(), "start": round(w.start, 3),
                             "end": round(w.end, 3), "prob": round(w.probability, 3)})
    ref = [_norm(t) for t in _tokens(guion) if _norm(t)]
    hyp = [_norm(p["word"]) for p in palabras if _norm(p["word"])]
    sm = SequenceMatcher(a=ref, b=hyp, autojunk=False)
    diffs = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "equal":
            diffs.append({"op": op, "guion": " ".join(ref[i1:i2]),
                          "whisper": " ".join(hyp[j1:j2])})
    aciertos = sum(b.size for b in sm.get_matching_blocks())
    precision = aciertos / max(1, len(ref))
    smf = SequenceMatcher(a=[_fon(t) for t in ref], b=[_fon(t) for t in hyp], autojunk=False)
    precision_fon = sum(b.size for b in smf.get_matching_blocks()) / max(1, len(ref))
    dur = sf.info(str(wav)).duration
    rep = {"modelo": modelo, "texto": " ".join(texto), "palabras": palabras,
           "duracion_s": round(dur, 3), "palabras_guion": len(ref),
           "palabras_por_seg": round(len(ref) / dur, 2) if dur else None,
           "precision_palabras": round(precision, 4),
           "precision_fonetica": round(precision_fon, 4), "diferencias": diffs,
           "baja_confianza": [p for p in palabras if p["prob"] < 0.6]}
    salida.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    return rep


# --------------------------------------------------------------------- main
def genera(texto: str, voice: str, rate: str, pitch: str, volume: str, id_: str,
           out: Path, por_frases: bool = False, pausa_default: float = 0.25,
           pronuncia: dict | None = None, recortar: bool = True, cola: float = 0.15):
    pronuncia = pronuncia or {}
    out.mkdir(parents=True, exist_ok=True)
    base = out / id_
    palabras_tot, partes, cursor = [], [], 0.0
    plan = []
    if por_frases:
        items = _lee_frases(texto, pausa_default)
    else:
        items = [("frase", " ".join(l.strip() for l in texto.splitlines() if l.strip()))]

    for tipo, val in items:
        if tipo == "pausa":
            n = int(round(val * SR))
            partes.append(np.zeros(n, dtype=np.float32))
            plan.append({"pausa": val, "start": round(cursor, 3)})
            cursor += n / SR
            continue
        mp3, pals = asyncio.run(_sintetiza(_aplica_pronuncia(val, pronuncia), voice,
                                           rate, pitch, volume))
        pals = _restaura_palabras(pals, val) if pronuncia else pals
        x = _mp3_a_array(mp3)
        quitado = 0.0
        if por_frases and recortar:
            x, quitado = _recorta(x)
        for p in pals:
            # los WordBoundary pueden caer unos ms antes del recorte: se acotan a la frase
            ini = min(max(0.0, p["start"] - quitado), len(x) / SR)
            fin = min(max(ini, p["end"] - quitado), len(x) / SR)
            palabras_tot.append({**p, "start": round(ini + cursor, 3),
                                 "end": round(fin + cursor, 3)})
        plan.append({"frase": val, "start": round(cursor, 3),
                     "end": round(cursor + len(x) / SR, 3)})
        partes.append(x)
        cursor += len(x) / SR
    if cola > 0:
        partes.append(np.zeros(int(cola * SR), dtype=np.float32))
    audio = np.concatenate(partes)
    pico = float(np.max(np.abs(audio))) if audio.size else 0
    if pico > 0.98:
        audio = audio * (0.98 / pico)
    _guarda(audio, base)
    (Path(str(base) + ".words.json")).write_text(
        json.dumps(palabras_tot, ensure_ascii=False, indent=1), encoding="utf-8")
    meta = {"id": id_, "proveedor": "edge-tts (Microsoft Edge Read Aloud, gratis)",
            "voice": voice, "rate": rate, "pitch": pitch, "volume": volume,
            "modo": "por-frases" if por_frases else "texto",
            "pronuncia": pronuncia, "duracion_s": round(len(audio) / SR, 3),
            "sample_rate": SR, "plan": plan, "texto": texto}
    (Path(str(base) + ".meta.json")).write_text(
        json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    return meta


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--text", help="texto a sintetizar")
    g.add_argument("--file", help="archivo de texto (UTF-8)")
    ap.add_argument("--voice", default="es-MX-JorgeNeural")
    ap.add_argument("--rate", default="+0%")
    ap.add_argument("--pitch", default="+0Hz")
    ap.add_argument("--volume", default="+0%")
    ap.add_argument("--id", required=True)
    ap.add_argument("--out", default=".")
    ap.add_argument("--por-frases", action="store_true")
    ap.add_argument("--pausa-default", type=float, default=0.25,
                    help="pausa entre frases sin [pausa] explícita (s)")
    ap.add_argument("--sin-recorte", action="store_true",
                    help="no recortar silencios de cada frase en --por-frases")
    ap.add_argument("--cola", type=float, default=0.15, help="silencio final (s)")
    ap.add_argument("--pronuncia", action="append", default=[],
                    help='"palabra=variante" solo para el TTS (repetible)')
    ap.add_argument("--sin-glosario", action="store_true",
                    help="no aplicar voz/pronuncia.json")
    ap.add_argument("--verify", action="store_true",
                    help="transcribe con faster-whisper small (es, int8) y compara")
    a = ap.parse_args()

    texto = a.text if a.text is not None else Path(a.file).read_text(encoding="utf-8")
    pron = {}
    glos = Path(__file__).with_name("pronuncia.json")
    if not a.sin_glosario and glos.exists():
        pron.update({k: v for k, v in json.loads(glos.read_text(encoding="utf-8")).items()
                     if not k.startswith("_")})
    pron.update(dict(p.split("=", 1) for p in a.pronuncia))
    out = Path(a.out)
    meta = genera(texto, a.voice, a.rate, a.pitch, a.volume, a.id, out,
                  por_frases=a.por_frases, pausa_default=a.pausa_default,
                  pronuncia=pron, recortar=not a.sin_recorte, cola=a.cola)
    print(f"{a.id}: {meta['duracion_s']} s · {a.voice} rate {a.rate} pitch {a.pitch}")
    if a.verify:
        guion = "\n".join(l for l in texto.splitlines()
                          if not PAUSA_RE.match(l.strip()) and not l.strip().startswith("#"))
        rep = verifica(out / f"{a.id}.wav", guion, out / f"{a.id}.transcript.json")
        print(f"  whisper: {rep['texto']}")
        print(f"  precisión {rep['precision_palabras']:.1%} (fonética "
              f"{rep['precision_fonetica']:.1%}) · "
              f"{rep['palabras_por_seg']} pal/s · diffs: {rep['diferencias']}")


if __name__ == "__main__":
    sys.exit(main())
