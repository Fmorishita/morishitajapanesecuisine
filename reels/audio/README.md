# Audio de los reels de Morishita: fuente y licencia de cada pista

Qué hay en esta carpeta, de dónde sale y bajo qué licencia. Antes de publicar, revisa la regla de CLAUDE.md: *"Música y SFX con licencia de uso comercial (catálogo de HeyGen vía /media-use u otra que yo indique); anota la fuente de cada pista."* La música y los SFX de `musica/` y `sfx/synth/` son **otra fuente**: originales, sintetizados aquí. **Falta que el dueño apruebe esta fuente** (ver "Pendiente" al final).

## 1. Música (`musica/`): original, sintetizada internamente

| Pista | BPM / tonalidad | Duración | Fuente | Licencia |
|---|---|---|---|---|
| `morishita-bed-A-112.wav` | 112 · Hirajoshi en Re (D E F A Bb); acordes Dm9, Bbmaj9, Gm(add9), A7sus4 | 64.0 s | `_src/gen_musica.py A` | Original, generada internamente (sin muestras ni terceros) |
| `morishita-bed-B-120.wav` | 120 · Miyako-bushi en Mi (E F A B C); acordes Am9, Fmaj9, Dm9, E7sus4(b9) | 64.0 s | `_src/gen_musica.py B` | Original, generada internamente |
| `morishita-bed-A-112-corte40.wav` (extra) | igual que A, forma corta | 40.7 s | `_src/gen_musica.py A40` | Original, generada internamente |
| `morishita-bed-B-120-corte40.wav` (extra) | igual que B, forma corta | 40.0 s | `_src/gen_musica.py B40` | Original, generada internamente |
| `stems/<pista>_{drums,bass,melodic,pad}.wav` | stems de cada pista | igual | mismo script | Original. `drums` incluye también los FX de transición (risers, booms, platillos). La suma de los 4 stems es la mezcla, con error < 0.000001. |

- Cómo se hizo: todo con numpy/scipy (`_src/dsp.py`): koto por Karplus-Strong con *oshide* (doblar la cuerda tras el punteo) y glissando *sararin*; shakuhachi de seno con aire filtrado, *meri* al inicio y vibrato tardío; o-daiko y shime-daiko por modos de membrana; kick con sub, clap, rim, hats metálicos, shaker; pad de sierras aditivas desafinadas; bajo 808 (A) y bajo house a contratiempo (B); reverb por convolución con IR sintética. Semillas fijas: el script reproduce exactamente el mismo audio.
- Formato: WAV 48 kHz, estéreo, 24 bits. Master con limitador *lookahead* sobre picos sobremuestreados ×4, la misma curva de ganancia aplicada a la mezcla y a los stems.
- Por pista: `<pista>.beats.json` (bpm, tiempo de cada beat, inicios de compás, secciones en segundos, golpes clave) y `<pista>.png` (forma de onda + espectrograma con las secciones marcadas). Todas las métricas están en `musica/metricas.json`.

### Métricas medidas (pyloudnorm, true peak ×4)

| Pista | LUFS int. | True peak | Crest | Correlación L/R | Sub <60 / 60–250 / 250–2k / 2–6k / >6k (% energía) |
|---|---|---|---|---|---|
| A-112 | −14.0 | −1.25 dBTP | 14.1 dB | 0.85 | 40 / 31 / 25 / 3.5 / 1.0 |
| B-120 | −14.0 | −1.25 dBTP | 14.6 dB | 0.87 | 22 / 49 / 23 / 4.5 / 1.7 |
| A-112-corte40 | −14.0 | −1.25 dBTP | 14.2 dB | 0.84 | 37 / 31 / 28 / 3.0 / 0.9 |
| B-120-corte40 | −14.0 | −1.25 dBTP | 14.6 dB | 0.86 | 22 / 48 / 25 / 3.9 / 1.5 |

Ninguna muestra llega a 0 dBFS (sin clipping). Loudness por sección (LUFS integrado del tramo):

| Sección | A-112 (s) | LUFS | B-120 (s) | LUFS |
|---|---|---|---|---|
| intro: golpe de entrada (taiko + sub + sararin) | 0–2.14 | −13.4 | 0–2.0 | −13.7 |
| build: arpegio de koto, entran hats/kick/bajo, redoble de shime | 2.14–19.29 | −16.0 | 2.0–20.0 | −15.1 |
| **drop** (1/3): hook de koto, batería completa | 19.29–32.14 | −12.2 | 20.0–32.0 | −12.3 |
| respiro: shakuhachi solo, taiko suave | 32.14–40.71 | −15.0 | 32.0–40.0 | −15.0 |
| rebuild: kicks a negras y luego corcheas, redoble | 40.71–47.14 | −14.5 | 40.0–46.0 | −15.3 |
| drop2: hook con octava grave, hats abiertos | 47.14–55.71 | −12.9 | 46.0–56.0 | −12.7 |
| salida: golpe final y acorde + shakuhachi sostenidos, fade de 1.5 s | 55.71–64.0 | −14.7 | 56.0–64.0 | −16.5 |

En los últimos 6 s de cada pista el nivel solo va bajando: no hay cambios bruscos debajo del CTA. El mayor salto entre medios segundos es de +0.5 a +0.7 dB en A, B y B-corte40, y de +1.3 dB en A-corte40 (una nota suave de koto). Un beat antes de cada drop hay un silencio de batería y bajo (A: 18.75 s y 46.61 s; B: 19.5 s y 45.5 s), y los risers terminan justo en el drop.

### Cómo deberían sonar (descripción honesta)

- **A-112, "elegante / moody":** trap-lite a medio tiempo (se siente a 56). Clap en el 3, 808 con caída de tono y hats a corcheas con redobles cortos. El koto en Hirajoshi lleva el hook y el shakuhachi responde. Oscuro y con mucho grave: **40–50 % de la energía está por debajo de 60 Hz en los drops**. En el celular ese grave casi no se oye (el 808 está saturado para que sus armónicos sí se oigan); con audífonos puede sentirse pesado. Si estorba, baja el stem `bass` 2–3 dB.
- **B-120, "más enérgica":** house-lite, *four-on-the-floor*, clap en 2 y 4, hat abierto a contratiempo, bajo a contratiempo y *sidechain* (el pad "respira" con el kick). Koto en Miyako-bushi, más brillante y con más pulso. Graves más contenidos y más medios-altos que A.
- **Lo que hay que saber:** es síntesis hecha por código, sin producción en DAW. Lo validé con métricas y espectrogramas; **nadie la ha escuchado todavía con oídos humanos**. Por diseño, lo más convincente es la percusión (taiko, kick, clap), el koto Karplus-Strong (afinación medida a ±2 cents) y el pad. El shakuhachi es el timbre más sintético: puede sonar más a "flauta de seno con aire" que a bambú real. Hay que escucharlo antes de publicar y, si suena barato, quitar el shakuhachi (está en el stem `melodic`; o se regenera sin él).
- **Bajo la voz:** el reel necesita el *carve* de /hyperframes-audio (bajar la música 8–12 dB mientras habla la voz). El koto y el shakuhachi viven entre 250 Hz y 2 kHz, la misma zona que la voz.

### Recomendación para un reel de 35–45 s (prueba social / experiencia)

**`morishita-bed-B-120-corte40.wav` (40.0 s).** A 120 BPM y 30 fps, un beat dura exactamente 15 frames: los cortes caen siempre en un frame entero, sin deriva. A 112 BPM son 16.07 frames por beat y se va desfasando. Las secciones cuadran con la estructura de CLAUDE.md:

| Tramo del reel | Música (B-120-corte40) |
|---|---|
| Gancho 0–3 s | golpe de entrada en 0.0 s; intro 0–2 s; arranca el build en 2.0 s |
| Experiencia 3–20 s | build 2–10 s (cortes cada 1 s = 2 beats); silencio en 9.5 s; **drop en 10.0 s** (la revelación); drop 10–22 s (cortes cada 0.5–1 s) |
| Prueba / reseña 20–28 s | **respiro 22–30 s**: shakuhachi y taiko suave. Ahí va la reseña textual de Google con `rin-resena.wav` |
| Mini-rebuild | rebuild 30–34 s, con riser hacia el cierre |
| CTA (últimos 6 s) | **salida 34–40 s**: golpe en 34.0 s y luego acorde sostenido; nota de shakuhachi desde 34.6 s; fade desde 38.5 s |

Beats: cada 0.5 s; compases en 0, 2, 4… s. Grid completo en `musica/morishita-bed-B-120-corte40.beats.json`. Si el reel dura menos de 40 s, recorta la música dentro del build (entre 2 y 10 s) en múltiplos de 2 s (1 compás) y deja intactos el drop y la salida.

## 2. SFX

| Carpeta | Fuente | Licencia |
|---|---|---|
| `sfx/synth/` (16 sonidos) | Sintetizados internamente con `_src/gen_sfx.py` (2026-10-08) | Original, generada internamente; sin terceros. Detalle, duración, "pico en" y uso de cada uno en `sfx/synth/README.md` |
| `sfx/bundled/` | Biblioteca que trae HyperFrames `media-use` 0.8.141 (Pixabay) | Pixabay Content License (ver `sfx/bundled/README.md`; la copió otro agente) |

## 3. Scripts (`_src/`)

- `dsp.py`: osciladores, filtros, instrumentos, reverb, limitador y medición.
- `gen_musica.py [A|B|A40|B40]`: genera mezcla, stems y beat grid. Tarda ~1 min por pista con 1 núcleo.
- `gen_sfx.py`: genera el kit de SFX y su `manifest.json`.
- `analizar.py <wav> [beats.json]`: métricas y PNG.
- Ejecuta con `/tmp/claude-0/venv/bin/python` (numpy, scipy, soundfile, pyloudnorm, pillow).

## Pendiente (decide el dueño)

1. **Aprobar como fuente válida** la música y los SFX "originales, generados internamente" (CLAUDE.md solo nombra el catálogo de HeyGen u otra fuente que indique el dueño).
2. Escuchar A y B (con audífonos y en el celular) y elegir una. Si el shakuhachi suena barato, se quita.
3. Los WAV pesan ~290 MB en total (stems a 24 bits). Antes de un commit, decide si van a git, a Git LFS o se regeneran con los scripts.
