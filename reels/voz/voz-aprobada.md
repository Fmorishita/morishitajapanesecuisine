# Voz en off: PROPUESTA (no aprobada)

> **Estado:** PROPUESTA del 2026-10-08. **No está aprobada por el dueño.** Hasta que escribas "voz aprobada", nada de esto es regla.
> **Nota clara:** es la **mejor opción gratuita disponible aquí** (sin keys de ElevenLabs ni HeyGen; Kokoro descartado por CLAUDE.md). Las voces es-MX de Microsoft suenan a **español mexicano estándar (centro)**, no a norteño. Para un acento más norteño, en el orden de CLAUDE.md:
> - **(A)** grabar tu voz o la de alguien del equipo con el guion (gratis, la más creíble; con un celular en un cuarto sin eco basta; el script ya alinea palabras con `--verify`).
> - **(B)** ElevenLabs Voice Design o HeyGen con key: **tiene costo; te aviso el monto antes de generar nada**.

## Ajustes propuestos

| Campo | Valor |
|---|---|
| Proveedor | edge-tts 7.2.8 (voces neuronales de Microsoft Edge "Read Aloud"; gratis, sin cuenta; requiere red por `HTTPS_PROXY`) |
| Voz (ID) | **`es-MX-JorgeNeural`** (hombre, México) |
| Rate | **`+8%`** (rango útil +5 % a +10 %; +12 % ya emborrona "arma tu omakase") |
| Pitch | **`+0Hz`** (−2 Hz baja la F0 solo ~2–3 Hz: imperceptible; si quieres más grave, probar −5 Hz) |
| Volume | `+0%` (normalizar en la mezcla final a −14 LUFS; el crudo sale en ~−19.6 LUFS, pico ~−2 dBFS) |
| Modo | **`--por-frases`**: una oración por línea, pausas explícitas `[pausa X]` |
| Pausas | 0.15–0.25 s entre ideas encadenadas · 0.3–0.4 s antes de un cambio de tramo · 0.4 s antes del CTA |
| Ritmo resultante | ~2.4 palabras/s totales (~3.15 pal/s sin contar pausas). Gancho de ≤ 8 palabras ≈ 2.5–3 s |
| Alternativa mujer | `es-MX-DaliaNeural` +5 % / +10 %: la más limpia en la transcripción (100 % fonética) y la "sh" la hace más sibilante. Útil si el reel habla en voz de "la chef" |
| No recomendada | `es-US-AlonsoNeural`: acento latino de EE. UU., más "doblaje neutro"; en +5 % se le oyó "nigidis" |

Muestra de referencia: `voz/muestras/jorge-r8-p0-v2.mp3` (guion `voz/guiones/prueba-15s-v2.txt`).

## Cómo generar (comando de referencia)

```bash
cd reels/voz
/tmp/claude-0/venv/bin/python tts.py --file guiones/<id>.txt --por-frases \
  --voice es-MX-JorgeNeural --rate=+8% --pitch=+0Hz \
  --id <id> --out . --verify
```

Salidas: `<id>.mp3`, `<id>.wav` (48 kHz mono, PCM 16), `<id>.words.json` (`[{word,start,end}]` en s, de WordBoundary, ya con el offset de cada frase y de las pausas), `<id>.meta.json` (ajustes y plan de frases) y, con `--verify`, `<id>.transcript.json` (faster-whisper small, es, int8: palabras con tiempos y probabilidad, precisión literal y fonética, diferencias contra el guion).
Ojo: usa `--rate=+8%` y `--pitch=-2Hz` con `=` (si no, argparse toma el `-2Hz` como opción).
Los timestamps de edge-tts coinciden con los de whisper con ±0.1 s, sin deriva (comprobado en 19 s de audio).

## Glosario de pronunciación (edge-tts, voces es-MX / es-US)

Método: prueba acústica de la consonante (duración y centroide espectral de la fricativa en una frase portadora) + transcripción con faster-whisper. Whisper solo no basta: escribe la palabra que conoce aunque se pronuncie distinto.

| Palabra | Qué hace el TTS | Variante que funciona | Estado |
|---|---|---|---|
| **nigiri / nigiris** | Lo lee con **jota** ("nijiri"): fricativa de ~107 ms, idéntica a escribir "nijiri" | **`niguiri` / `niguiris`** (g suave, ~11 ms) | **Aplicado por defecto** en `voz/pronuncia.json` (solo al texto del TTS; subtítulos y words.json dicen "Nigiris") |
| **Morishita** | La "sh" sale como **s** ("Morisita"), igual que si se escribe "Morisita". Ninguna grafía da /ʃ/: "Mori-shita", "Morishíta", "Morixita" también dan s | "Morichita" da **ch** (/tʃ/, más cerca de "sh" pero suena forzado) | Se deja **"Morisita"** (natural en México). Si quieres "sh" real: (A) voz grabada o (B) ElevenLabs. En pantalla siempre "MORISHITA" |
| **sashimi(s)** | "sasimi" (s en vez de sh). En lista rápida ("nigiris, sashimis, …") se emborrona: whisper oye "sasinis" en 6 de 10 muestras | Ponerla **en su propia línea** ("Nigiris." / "Sashimis." con 0.12 s) o en singular | Escribir así en los guiones |
| **omakase** | Bien: "o-ma-ká-se" con k (whisper escribe "omacase" u "omakase"). A +12 % y pegado a "tu" se oyó "armató macase" | Rate ≤ +10 %; si se pega, "tu omakase" → "el omakase" o pausa corta antes | OK |
| **chef + Vero** | "La chef Vero Morishita" de corrido: la f se cae y se oye "chat/check pero morisita" | **"La chef, Vero Morishita, …"** con comas (whisper lo transcribe bien) | Escribir con comas. Nombre "Chef Vero Morishita" aún pendiente de tu OK (hechos.md D6) |
| **Ensenada** | Bien en las 12 muestras | — | OK |
| **catorce** | Bien en las 12 muestras | Escribir cifras con letra ("catorce", "cuatro") | OK |
| **sábado y domingo** | Bien | — | OK |
| **link** | Bien ("link") | — | OK |
| sushi, Shakira | El TTS sí hace /ʃ/ (están en su diccionario) | No sirve como truco para Morishita | Referencia |

## Muestras (2026-10-08)

Texto de prueba (`voz/guiones/prueba-15s.txt`, solo datos de `fuente/hechos.md` sección (a): A6, A1, A11, A18, A10, A12, A17, A7, A25; sin wagyu ni kobe):

> Una barra. Cuatro asientos. Catorce tiempos. Sin carta. La chef, Vero Morishita, arma tu omakase frente a ti. Nigiris, sashimis, platillos calientes. Aquí en Ensenada. Solo sábado y domingo. Reserva tu lugar en el link de mi perfil.

(38 palabras. v2 = mismo texto con "Nigiris." / "Sashimis." / "Platillos calientes." en líneas separadas.)

| Muestra (`voz/muestras/`) | Voz | Rate | Pitch | Dur. (s) | Pal/s | Pal/s sin pausas | Precisión literal | Precisión fonética | F0 mediana | Diferencias que oyó whisper |
|---|---|---|---|---|---|---|---|---|---|---|
| **jorge-r8-p0-v2** ★ | Jorge | +8 % | 0 Hz | 15.61 | 2.43 | 3.15 | 92 % | **100 %** | 115 Hz | morishita→morisita · omakase→omacase · sashimis→sasimis |
| jorge-r8-pm2-v2 | Jorge | +8 % | −2 Hz | 15.56 | 2.44 | 3.15 | 92 % | **100 %** | 112 Hz | igual que la anterior |
| jorge-r0-p0 | Jorge | +0 % | 0 Hz | 16.73 | 2.27 | 2.96 | 95 % | 97 % | 112 Hz | morisita · sashimis→sasinis |
| jorge-r0-pm2 | Jorge | +0 % | −2 Hz | 16.65 | 2.28 | 2.97 | 92 % | 100 % | 110 Hz | morisita · omacase · sasimis |
| jorge-r8-p0 | Jorge | +8 % | 0 Hz | 15.70 | 2.42 | 3.18 | 95 % | 97 % | 114 Hz | morisita · sashimis→sasinis |
| jorge-r8-pm2 | Jorge | +8 % | −2 Hz | 15.65 | 2.43 | 3.19 | 89 % | 95 % | 113 Hz | morisita · omacase · **"ni guidis sacinis"** |
| jorge-r12-p0 | Jorge | +12 % | 0 Hz | 15.21 | 2.50 | 3.31 | 87 % | 92 % | 114 Hz | **"arma tu omakase"→"armató macase"** · sassimis |
| jorge-r12-pm2 | Jorge | +12 % | −2 Hz | 15.23 | 2.50 | 3.30 | 92 % | 97 % | 113 Hz | morisita · omacase · sasinis |
| alonso-r5-p0 | Alonso (es-US) | +5 % | 0 Hz | 16.72 | 2.27 | 2.95 | 89 % | 95 % | 107 Hz | morisita · omacase · **"nigidis sasinis"** |
| alonso-r10-p0 | Alonso (es-US) | +10 % | 0 Hz | 16.11 | 2.36 | 3.09 | 95 % | 97 % | 108 Hz | morisita · sassinis |
| dalia-r5-p0 | Dalia | +5 % | 0 Hz | 17.01 | 2.23 | 2.92 | 95 % | **100 %** | 208 Hz | morisita · sasimis |
| dalia-r10-p0 | Dalia | +10 % | 0 Hz | 16.29 | 2.33 | 3.07 | 92 % | **100 %** | 208 Hz | morisita · omacase · sacimis |

- "Precisión fonética" = coincidencia tras igualar grafías que suenan igual en México (sh/s, k/c, v/b, gui/gi…). Es la que importa para saber si se entiende.
- Todas las muestras: mp3 + wav + words.json + meta.json + transcript.json. El glosario (`niguiri`) se aplicó en todas.
- **Falta tu oído:** las métricas dicen claridad y ritmo, no si "suena norteño" ni si suena premium. Escucha en este orden: `jorge-r8-p0-v2`, `jorge-r8-pm2-v2`, `dalia-r10-p0`, `jorge-r0-p0`.

## Reglas de escritura para esta voz (propuesta)

1. Una oración por línea en el archivo del guion; el ritmo lo ponen las `[pausa]`, no el TTS (dos oraciones en una línea dejan ~0.9 s de silencio entre ellas).
2. Cifras con letra ("catorce tiempos", "cuatro asientos", "mil ochocientos cincuenta pesos").
3. Listas de palabras japonesas: una por línea.
4. Nombres propios con comas alrededor ("La chef, Vero Morishita, …").
5. Rate entre +5 % y +10 %; nunca +12 % con palabras japonesas.
6. Siempre `--verify` y revisar `diferencias` y `baja_confianza` en el transcript antes de montar.

## Pendiente del dueño

- [ ] Escuchar las muestras y aprobar voz, rate y pitch (o pedir (A) grabación propia / (B) ElevenLabs-HeyGen con costo).
- [ ] ¿"Morisita" (s) es aceptable o quieres "sh" real? (solo se logra con (A) o (B)).
- [ ] Nombre del chef para la voz (hechos.md D6).
