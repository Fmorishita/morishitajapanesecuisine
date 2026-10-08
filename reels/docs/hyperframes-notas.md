# HyperFrames 0.8.141: notas prácticas y verificadas para los reels de Morishita

> Escrito el 2026-10-08 probando todo en esta máquina (Linux x64, 4 núcleos, sin GPU, Node 22.22, ffmpeg 6.1).
> **[VERIFICADO]** = lo corrí y vi el resultado. **[DOCS]** = sale de las skills o del CLI, sin probarlo aquí.
> Ejemplo funcional: `videos/_prueba-6s/` → `renders/prueba-6s-borrador-v01.mp4` (su código completo está al final).
> Reglas del reel (ritmo, zonas, CTA, voz): `CLAUDE.md`. Look (color, tipos, movimiento): `marca/frame.md`. Esta guía es solo el "cómo" técnico.

## 0. Lo accionable en 10 líneas

1. Todo se corre desde `reels/` o desde la carpeta del proyecto: `npx hyperframes …` usa `reels/node_modules/hyperframes` (0.8.141, fijado en `reels/package.json`).
2. Proyecto nuevo: `cd videos && HYPERFRAMES_SKIP_SKILLS=1 npx hyperframes init <id> --example blank --resolution portrait --non-interactive`.
3. **Todos los assets van DENTRO del proyecto** (`videos/<id>/assets/…`, `vendor/`). Rutas con `../` dan error de lint `invalid_parent_traversal_in_asset_path`: las rutas `../../marca/fonts/…` que sugiere `marca/frame.md` **no sirven**; copia los archivos.
4. GSAP local: `vendor/gsap.min.js` (copia del 3.14.2). El scaffold y los bloques del catálogo lo cargan del CDN; cámbialo por `vendor/gsap.min.js` (ruta desde la raíz del proyecto, también dentro de `compositions/`).
5. Estructura recomendada: `index.html` delgado + una sub-composición por escena en `compositions/` (si no, lint avisa `nested_structure_needs_subcomposition`).
6. Antes de programar un efecto: `npx hyperframes catalog --query "<en inglés>" --json` y `npx hyperframes add <id>` (sección 5).
7. Gate: `npx hyperframes check` (incluye lint; ~12 s) → 0 errores. `lint` solo (~1 s) mientras editas.
8. Mirar sin renderizar: `npx hyperframes snapshot --at 0,2.4,3.6 --no-end -o /tmp/claude-0/<algo>` (~10 s; deja `contact-sheet.jpg`).
9. Borrador: `npx hyperframes render --quality draft --fps 30 --output ../../renders/<id>-borrador-vNN.mp4` (6 s de video ≈ 15 s de render).
10. QA: `ffprobe`, `ffmpeg … ebur128`, y fotogramas extraídos (sección 12).

## 1. Instalación y navegador [VERIFICADO]

```bash
cd reels
npm install                                  # instala hyperframes@0.8.141 (6 s, 75 paquetes)
npx hyperframes browser ensure               # descargó Chrome Headless Shell 152.0.7977.30 (114 MB) SIN problema por el proxy
npx hyperframes browser path                 # → ~/.cache/hyperframes/chrome/chrome-headless-shell/linux-152.0.7977.30/…/chrome-headless-shell
npx hyperframes doctor --json | python3 -c "import json,sys;[print(c['ok'],c['name'],c.get('detail')) for c in json.load(sys.stdin)['checks']]"
```

- `doctor`: **Chrome ok** (caché propia de HyperFrames), FFmpeg/FFprobe ok, `whisper-cpp` ok después del primer `transcribe` (sección 9). Fallan solo cosas opcionales: Kokoro TTS, MusicGen, "Docker running". `doctor --json` siempre sale con código 0: hay que leer `.ok` o cada check.
- **Plan B si la descarga falla** (no hizo falta, pero lo probé): el código (`findFromEnv` en `dist/chunk-*.js`) acepta la variable `HYPERFRAMES_BROWSER_PATH` (alias `PRODUCER_HEADLESS_SHELL_PATH`). Con
  `HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell npx hyperframes doctor --json`
  el check sale `Chrome ok · env: /opt/pw-browsers/…/headless_shell`. Ojo: el binario es `chrome-linux/headless_shell` (no `chrome-headless-shell`). Con un Chrome normal (`/opt/pw-browsers/chromium`) funciona pero cae al modo `screenshot`, más lento que `beginframe`.
- En esta máquina el render usa **`beginframe capture · software gpu`** (no hay WebGL/GPU). Va bien para reels de 15–35 s.
- Telemetría anónima: la apagué en mis comandos con `HYPERFRAMES_NO_TELEMETRY=1` (opcional). `HYPERFRAMES_SKIP_SKILLS=1` evita que `init` vuelva a revisar skills en GitHub.
- No usar: `npx hyperframes usage` (lee credenciales del harness), `auth`, `cloud`, `publish`, `feedback` (envía datos fuera). Nada de eso hace falta.

## 2. Skills instaladas [VERIFICADO]

`npx hyperframes skills` (12 s) instaló 21 skills **globales** en `~/.claude/skills/<nombre>/` y copia en `~/.agents/skills/<nombre>/` (no en el repo). `npx hyperframes skills check` → "21 current". `skills update <nombre>` instala/actualiza una.
Para el agente quedan disponibles como `/hyperframes`, `/hyperframes-core`, etc. Las que importan para reels:

| Skill | Para qué la leí / qué sirve aquí |
|---|---|
| `hyperframes` | Router: orden de trabajo y qué skill usar. En un proyecto existente, ir directo a la operación. |
| `hyperframes-core` | **El contrato**: `data-*`, clips, sub-composiciones, medios, determinismo. Su `references/creator-editing-recipes.md` tiene recetas copiables (corte, trim, punch, Ken Burns, crossfade, ducking). |
| `hyperframes-cli` | init/lint/check/snapshot/preview/render y diagnóstico de render. |
| `hyperframes-keyframes` / `hyperframes-animation` | Zoom/punch/whip seguros al seek; reglas de movimiento y 24 efectos de texto. |
| `hyperframes-creative` | Dirección de arte, ritmo, tipografía (manda `marca/frame.md`). |
| `hyperframes-audio` | Fades, automatización de volumen, **carve** de música bajo voz, efectos (EQ, compresor, limitador). |
| `media-use` | SFX incluidos (sección 7), TTS, transcripción, grading. Música y SFX de HeyGen requieren el CLI `heygen` con sesión (**no** configurado). |
| `hyperframes-registry` | Catálogo (`catalog`/`add`) y cómo cablear bloques y componentes. |
| `general-video`, `motion-graphics`, `embedded-captions`, `talking-head-recut`… | Flujos completos; para nuestros reels el más cercano es `general-video`. |

Nota: `npx hyperframes docs <tema>` (data-attributes, gsap, rendering, troubleshooting, compositions, examples) es muy escueto y en parte viejo (p. ej. dice "calidad draft/standard/high"); manda lo de las skills y `--help`.

## 3. Estructura de un proyecto de reel

```
videos/<id>/
  index.html                 composición raíz (delgada): ranuras de escena + audio
  compositions/
    escena-*.html            una sub-composición por escena (<template>)
    <bloque>.html            bloques del catálogo (hyperframes add)
    components/<comp>.html   componentes del catálogo (fragmentos para pegar)
  assets/fonts|img|sfx|voz|musica/   COPIAS de marca/, assets/, audio/, voz/
  vendor/gsap.min.js         GSAP local
  hyperframes.json           rutas del registro (scaffold)
  hyperframes.lock.json      hash de lo instalado con add
  package.json, meta.json    scaffold (scripts fijados a hyperframes@0.8.141)
  CLAUDE.md, AGENTS.md       genéricos de HyperFrames (los crea init; mandan las reglas de reels/CLAUDE.md)
```

- `init` crea `index.html` de 10 s con GSAP por CDN; reemplázalo.
- **Studio/preview/check reescriben tus HTML**: añaden `data-hf-id="hf-xxxx"` a cada elemento (y reformatean `<img>`). Es normal; no los borres (Studio los usa para editar).
- `npx hyperframes timeline` (o `--json`) lista pistas y clips con tiempos absolutos: úsalo para revisar en vez de leer todo el HTML. Detalle: muestra un `<img>` dentro de una escena como "clip de 3 s por defecto", pero en el render se ve toda la escena (comprobado en el fotograma de 5.9 s).

## 4. Formato de la composición

### 4.1 Raíz (`index.html`), sin `<template>`

```html
<div id="root" data-composition-id="main" data-start="0" data-duration="6" data-fps="30"
     data-width="1080" data-height="1920"> … </div>
<script>
  const tl = gsap.timeline({ paused: true });
  window.__timelines["main"] = tl;          // la clave = data-composition-id
</script>
```

- `data-duration` de la raíz = **largo del render** (se lee una vez; no lo cambies por script). Si la timeline es más larga se corta; si es más corta se congela el último cuadro.
- `#root` con `width/height: 100%` (el runtime pone los píxeles de `data-width/height`).
- Una sola timeline GSAP **pausada** por composición, registrada al final. Nunca `tl.play()`.

### 4.2 Clips: qué hace cada atributo

| Atributo | Qué hace |
|---|---|
| `data-start` | Lo que convierte un elemento en clip (segundos). En sub-composiciones es **local** a la escena. |
| `data-duration` | Ventana visible `[start, start+dur)`: el último instante NO se dibuja; termina la animación un poco antes. Obligatorio en `div` y sub-composiciones; `img` = 3 s por defecto; audio/video = largo del archivo. |
| `data-track-index` | Solo carril visual de Studio. El orden de capas es CSS `z-index`. |
| `data-composition-src` | Monta una sub-composición o un bloque (`compositions/x.html`). |
| `data-composition-id` | En la ranura debe ser **igual** al id interno del archivo y a la clave de `window.__timelines`. Si no coincide, el render espera 45 s y sale sin animación. |
| `data-media-start` | Desde qué segundo del archivo arranca (trim). |
| `data-volume` | Ganancia fija (1 = 0 dB, máx. 3.98). Para fades/ducking: `data-automation`. |
| `data-playback-rate` | Velocidad constante 0.1–10 (speed ramp = lane `rate` en `data-automation`). |
| `class="clip"` | Convención (layout + Studio); lint avisa si falta en un elemento temporizado. No en `<audio>`/`<video>`. |
| `data-layout-allow-overflow` | Marca un desborde intencional (p. ej. el envoltorio del zoom). |
| `data-layout-ignore` | Excluye un decorativo de la auditoría de layout (lo usé en el grano). |

### 4.3 Sub-composición (una escena)

```html
<!doctype html><html lang="es"><head><meta charset="UTF-8" /></head><body>
<template>                      <!-- SOLO se clona lo de adentro: <style>, @font-face y <script> van aquí -->
  <style> #escena-x-root { position:absolute; inset:0; overflow:hidden; } … </style>
  <div id="escena-x-root" data-composition-id="escena-x" data-width="1080" data-height="1920"> … </div>
  <script>
    (function () {             // IIFE: evita choques de "const tl" entre escenas
      const tl = gsap.timeline({ paused: true });
      tl.fromTo("#…", {…}, {…}, 0);         // tiempos LOCALES de la escena
      window.__timelines["escena-x"] = tl;
    })();
  </script>
</template></body></html>
```

En `index.html`: `<div id="el-x" data-composition-id="escena-x" data-composition-src="compositions/escena-x.html" data-start="2.4" data-duration="3.6" data-track-index="1" data-width="1080" data-height="1920"></div>` y en CSS `#root > div[data-composition-src]{position:absolute;inset:0}`.

- Estilar la raíz de la escena por `#id`, nunca por clase (`subcomposition_root_styled_by_class`).
- Usa `fromTo` (no `from`): la escena se vuelve a buscar (seek) cada vez que aparece.
- Ids únicos en todo el ensamblado: prefija (`eg-`, `ec-`).
- Las rutas dentro de `compositions/*.html` son **desde la raíz del proyecto** (`assets/…`, `vendor/…`), no desde `compositions/`.

### 4.4 Animación GSAP: reglas que pasan lint a la primera

- Nunca `transform` en CSS + tween de `x/y/scale` en el mismo elemento (`gsap_css_transform_conflict`). Centra con flex/inset; el estado inicial va en `fromTo`. (`transform-origin` en CSS sí está bien.)
- Nunca `autoAlpha`/`visibility`/`display` sobre un clip (`gsap_animates_clip_element`): anima un hijo.
- Dos tweens de la misma propiedad que se tocan en el mismo instante → aviso `overlapping_gsap_tweens`. Para un pulso usa uno solo con `yoyo: true, repeat: 1`.
- Nada de `Math.random()` sin semilla, `Date.now()`, red en tiempo de render. `repeat: -1` solo con `data-duration` finito en la raíz.
- Escalar un `<span>` inline no hace nada: `display:block` o `inline-block`.
- Cada `<audio>` necesita `id` (sin id el render sale **mudo**); nunca `crossorigin` en audio/video.

## 5. Catálogo (registro) [VERIFICADO]

`npx hyperframes catalog --query "<en inglés>" --json` busca **en local** (tier `words`: coincide palabras del nombre, título, descripción y etiquetas; 392 ítems). La búsqueda "por significado" (`--on-device`) descarga un modelo de 33 MB: no la activé. Consultas en español no devuelven nada.
`npx hyperframes add <id> --no-clipboard --json` sí necesita red (baja los archivos).

- **Bloque** (`type: block`): composición completa con su timeline → `compositions/<id>.html`; se monta con `data-composition-src` (sección 4.3). Casi todos vienen a **1920x1080**: hay que cambiar en el archivo `html,body{width:1080px;height:1920px}` y `data-width="1080" data-height="1920"` de su raíz, o cubren solo una franja (me pasó con el flash: tapaba solo la parte de arriba).
- **Componente** (`type: component`): fragmento HTML/CSS/JS en `compositions/components/<id>.html`; se **pega** dentro de tu escena (copiar marcado, `<style>` y `<script>`, y sus llamadas a la timeline si las trae).
- Los "Shader transition" (`whip-pan`, `glitch`, `flash-through-white`, `light-leak`, `cinematic-zoom`…) usan WebGL y la ruta de composición por capas (más pesada; en esta máquina WebGL va por software). No los probé: para cortes de 2–3 frames basta un bloque/componente CSS.

### 5.1 Lo que devolvió cada consulta (ids exactos; los útiles para Morishita en negrita)

| Consulta | Ids más relevantes (tipo) · qué hacen |
|---|---|
| whip pan | **`whip-pan-cut`** (comp.: escena A sale lateral con desenfoque de movimiento y B entra a la misma velocidad; ranuras `before`/`after`, variables `direction`, `whip_at`; dispara evento `hf:sfx` "whip-cut" pero NO suena) · `whip-pan` (bloque shader) · `cut-the-curve` (corte direccional) · `headline-slam` (titular cae con sacudida de 3 frames) |
| glitch | `glitch` (bloque shader) · **`rgb-glitch-text`** (comp.: copias RGB del texto tiemblan un instante; marca: solo texto, ≤ 3 frames) · `caption-glitch-rgb` (subtítulo glitch + scanlines; no premium) |
| white flash / flash transition | **`editorial-flash-overlay`** (bloque: lavado blanco cálido + núcleo + barrido; golpe a 0.58 × duración; **usado en la prueba**) · `flash-through-white` (bloque shader, crossfade por blanco) · **`beat-accent`** (comp.: destello + micro-pulso de escala en un golpe de música) · `fade-through` (comp.: fundido pasando por un lavado) · `transitions-light` (vitrina) |
| zoom punch | `cinematic-zoom` (shader) · `zoom-through-transition` (comp.) · `yt-camera-move` (comp.: helpers de zoom/slide/tilt para cualquier envoltorio) · `shutter-slam` · para el punch-in de CLAUDE.md lo más simple es la receta GSAP (sección 6) |
| camera shake | **`camera-shake`** (comp.: 9 perfiles de sacudida, seek-safe, para cualquier envoltorio; marca: nunca sobre comida) · `char-slam-explode` · `push-in` (empuje lento a un titular) · `drift-hold` (tarjeta "viva" con respiración) |
| kinetic text | `caption-kinetic-slam` (una palabra a pantalla completa) · `kinetic-center-build` · `kinetic-type-swap` · **`per-word-rise`** (palabras suben de desenfoque a nítido) · **`tracking-in`** (revelado por espaciado, "premium") · `text-shimmer` / `shimmer-sweep` (brillo que cruza el texto) · `soft-blur-in` · `typewriter` (evitar: lento) |
| word by word captions | `caption-pill-karaoke`, `caption-highlight` (fondo rojo TikTok), `caption-clip-wipe`, **`caption-editorial-emphasis`** (dos fuentes, palabra clave mucho más grande), `caption-weight-shift`, `per-word-crossfade`, `staggered-fade-up`, `mk-callout-highlight` (bloque: resalta palabra a palabra con un escalar sincronizable a la voz) |
| highlight word | `mk-callout-highlight` · `caption-highlight` · **`marker-highlight`** (trazo de marcador sobre la palabra) · `inline-highlight` · `yt-feather-highlight` (oscurece todo menos una elipse: útil sobre una captura) |
| counter / number count up | **`count-up`** (comp.: contador que aterriza con pulso; "0 → 14") · **`number-wheel`** (dígitos que ruedan) · `number-pop-in` · `mk-progress-stat` (bloque: cifra grande + barra) · `apple-money-count` (con SFX; estilo finanzas) |
| light leak | `light-leak` (shader) · **`organic-light-leak-overlay`** (bloque CSS finito, "momentos de memoria") · `light-sweep-pass` (comp.: barrido de luz sobre una escena) · `godrays` (WebGPU) |
| film grain | **`grain-overlay`** (comp.: grano SVG animado por CSS; **usado en la prueba** con opacidad 0.09) · `grain-field` |
| particles | `particle-text-dissolve` · `particle-image-reveal` · `confetti` · `caption-particle-burst` (nada de humo; para pétalos sakura mejor hecho a mano con PRNG con semilla) |
| smoke | **0 resultados** (no hay humo en el catálogo: habría que hacerlo con video/PNG de humo o CSS propio) |
| ink | `ink-bleed-reveal` (tinta que florece y revela una marca: posible para el sello 森下) · `whiteboard-ink` · `marble` (WebGPU) |
| ken burns | **0 útiles** (solo devuelve `ridged-burn`): usar la receta GSAP (sección 6) |
| parallax | `parallax-zoom`, `parallax-unzoom`, `focus-rack`, `camera-rig-depth-stack`, `parallax-device-dive` |
| logo reveal | `logo-outro` (bloque) · **`logo-sting`** (comp.: la marca cae, un anillo y un cuadro blanco, y queda quieta) · `logo-brand-close` (letra por letra) · `ink-bleed-reveal` |
| end card / cta | **`cta-lockup`** (comp.: frase de acción + cápsula CTA + microcopia, y se queda quieto = CTA ≥ 3 s) · **`cta-close`** · `social-proof-card` (cierre con 5 estrellas, línea de prueba y CTA; pensado para apps) · `store-badge-lockup` (no aplica) |
| phone mockup | **`device-frame-stage`** (comp.: teléfono con ranura de pantalla; para las capturas de reserva) · `browser-device-stage` · `parallax-device-dive` · `notification-cascade`, `share-sheet-carousel` (bloques 1080x1920) |
| review card / quote | **`testimonial-card`** (comp.: cita a ritmo de lectura + nombre) · **`testimonial-proof-card`** (cita por líneas con máscara suave, avatar con iniciales, nombre en mono) · `social-proof-card` (las consultas "review card" y "end card" devuelven tarjetas de X/Reddit/Spotify: no sirven) |

Todo lo anterior se instala igual: `npx hyperframes add <id> --no-clipboard --json` desde la carpeta del proyecto. Revisa el archivo instalado: casi todos traen GSAP por CDN y tamaños 1920x1080 por defecto.

## 6. Imágenes: zoom, punch-in, Ken Burns [VERIFICADO]

La regla: **el zoom va en un envoltorio interno**, nunca en el clip temporizado ni en el `<img>` con tiempos.

```html
<div id="ec-cam" data-layout-allow-overflow>        <!-- envoltorio que se escala -->
  <img id="ec-img" src="assets/img/foto.jpg" style="display:block;width:1080px;height:1920px;object-fit:cover" />
</div>
```
```js
// Ken Burns / punch-in lento 100 → 105 % en 2.2 s
tl.fromTo("#ec-cam", { scale: 1 }, { scale: 1.05, duration: 2.2, ease: "sine.out" }, 0);
// Punch-in rápido (108–118 % en 6–8 frames = 0.2–0.27 s a 30 fps)
tl.to("#ec-cam", { scale: 1.09, duration: 0.2, ease: "power3.out" }, 2.2);
// Paneo: tl.fromTo("#ec-cam", {scale:1.05, xPercent:0}, {scale:1.15, xPercent:-6, duration:3, ease:"none"}, 0);
```

- Ancla el zoom con `transform-origin` en CSS. Con origen al centro el punch cortó "PASO 01" y "¿Cuántos" en el borde izquierdo; con `transform-origin: 8% 24%` no se corta nada. Revisa siempre el último cuadro del zoom.
- Sin `data-layout-allow-overflow` en el envoltorio, `check` avisa `container_overflow` (el zoom desborda a propósito).
- Las fotos van en `assets/img/` del proyecto. Las capturas de reserva ya miden 1080x1920 (`assets/recortes/`).
- Para que el texto se lea encima: scrim neutro (`#0a0908` al 0–97 %) solo en la franja del texto; no tiñe la foto.

## 7. Audio: voz, música, SFX

### 7.1 Colocar pistas [VERIFICADO]

```html
<audio id="vo-1" data-audio-group="voiceover" src="assets/voz/r01.wav" data-start="0" data-track-index="20" data-volume="1"></audio>
<audio id="music-bed" src="assets/musica/bed.mp3" data-start="0" data-duration="30" data-track-index="21" data-volume="0.8"></audio>
<audio id="sfx-whoosh" src="assets/sfx/whoosh.mp3" data-start="2.24" data-duration="0.57" data-track-index="11" data-volume="0.8"></audio>
```

- `<audio>` en la raíz: `data-start` en segundos **absolutos**. Dentro de una escena: tiempo local (se suma el `data-start` de la ranura).
- Para que un SFX "pegue" en un corte: `data-start = momento del corte − segundo del pico del archivo` (picos medidos en `audio/sfx/bundled/README.md`; el whoosh pica a 0.16 s, el pop a 0.12 s, el impacto a 0.07 s).
- `data-volume` = nivel fijo. Fades/ducking a mano = `data-automation` (lane de volumen, `t` en segundos locales del clip):
  `data-automation='{"version":1,"lanes":[{"target":"volume","points":[{"t":0,"v":0},{"t":1,"v":1},{"t":28,"v":1},{"t":30,"v":0}]}]}'`
  No mezclar lane y tween de `volume` en la misma pista (gana la lane; lint `audio_volume_double_automation`).
- SFX incluidos: `audio/sfx/bundled/` (19 archivos, Pixabay, uso comercial; README con duración, pico y uso). El `riser.mp3` **no** sube 10 s: pica a ~3.5 s y se apaga a ~4.3 s.

### 7.2 Música bajo la voz: "carve" [VERIFICADO en una copia de prueba]

Es la forma que pide CLAUDE.md (`/hyperframes-audio`): en vez de bajar toda la música, le recorta las bandas que ocupa la voz y la baja con un sobre que sigue a la voz.

1. Marca cada clip de voz con `data-audio-group="voiceover"` (solo voces en ese grupo: nada de música ni SFX).
2. La música con id/nombre que "suene" a música (`music`, `bgm`, `bed`…).
3. Corre el script de la skill. **Necesita `@hyperframes/core`**, que no viene con el CLI; lo instalé fuera del repo:
   ```bash
   mkdir -p /tmp/claude-0/hfcore && (cd /tmp/claude-0/hfcore && npm i --no-save @hyperframes/core@0.8.141)
   node ~/.claude/skills/hyperframes-audio/scripts/carve.mjs --comp index.html --core /tmp/claude-0/hfcore   # --dry-run para solo ver
   ```
   Salida real: `bed music-bed · voice vo-1 · carve strength 0.8 · bands 160Hz −7.4dB … 1600Hz −14.8dB … · level 79-point envelope, floor −19.2 dB · lanes 7`. Escribe en la música `data-fx-carve`, `data-fx-chain` y `data-automation`. `check` pasó y el render mezcló bien.
4. `--strength` 0–1 (0.8 por defecto; bájalo si la música es la protagonista), `--bed`/`--voice` si detecta mal. En Studio es el módulo "Voiceover carve" de la pista.

### 7.3 Loudness [VERIFICADO midiendo; sin herramienta de master]

HyperFrames no normaliza el master a −14 LUFS. Mide con `ffmpeg -nostats -i x.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:"` (la prueba: −16.2 LUFS, pico −4.1 dBFS, solo SFX). Ajusta con `data-volume` de cada pista, o con `npx hyperframes normalize-audio` (iguala un clip a otro por LUFS; [DOCS]), o como último paso con `ffmpeg -af loudnorm=I=-14:TP=-1.5` sobre el MP4 final (copiando el video). Pico ≤ −1 dBTP.

## 8. Subtítulos desde timestamps por palabra [VERIFICADO el mecanismo]

Formato que deja `transcribe` en `<proyecto>/transcript.json` (y el que espera el pipeline de captions):

```json
[ { "text": "Solo", "start": 0.21, "end": 0.27, "id": "w0" },
  { "text": "cuatro", "start": 0.27, "end": 0.68, "id": "w1" }, … ]
```

Lo que funcionó (una palabra a la vez, palabra clave en oro y 1.2×): **cada palabra es su propio clip** con `data-start`/`data-duration` (el runtime la oculta fuera de su ventana). Si en cambio solo bajas la opacidad, `check` las cuenta como textos encimados (`content_overlap`, error).

```js
const WORDS = [/* pegar transcript.json corregido */];
const VO_START = 0.2;                     // data-start del <audio> de la voz
const KEY = /^(cuatro|4|omakase|14|catorce)/i;
const caps = document.getElementById("caps");   // <div id="caps" class="clip" data-start="0" data-duration="…">
WORDS.forEach((w, i) => {
  const el = document.createElement("span");
  el.className = "cw" + (KEY.test(w.text) ? " key" : "");   // .cw { position:absolute; … }  .key { color:#d4af6a }
  el.id = "cw-" + i;
  el.textContent = w.text.replace(/[.,]$/, "");
  const fin = WORDS[i + 1] ? WORDS[i + 1].start : w.end + 0.3;
  el.setAttribute("data-start", (VO_START + w.start).toFixed(3));
  el.setAttribute("data-duration", (fin - w.start).toFixed(3));
  caps.appendChild(el);
  tl.fromTo(el, { opacity: 0, y: 20, scale: KEY.test(w.text) ? 1.2 : 1 },
                { opacity: 1, y: 0, scale: 1, duration: 0.1, ease: "power2.out" }, VO_START + w.start);
});
window.__timelines["main"] = tl;          // registrar DESPUÉS de construir
```

- Para 1–3 palabras por bloque: agrupa `WORDS` en frases cortas y usa el `start` de la primera y el `start` de la siguiente frase como fin.
- Revisa la ortografía del transcript antes de pegarlo: Whisper escribió **"omacase"** (es "omakase") y "14" en cifra.
- Alternativa del catálogo: componentes `caption-*` o el flujo `/embedded-captions` (no probados).

## 9. `transcribe` [VERIFICADO]

```bash
npx hyperframes transcribe voz/r01.wav --model small --language es --dir videos/<id> --json
```

- **Motor:** `--engine auto` usa Parakeet si está instalado (`npx hyperframes models install parakeet`, no lo instalé) y si cubre el idioma; si no, **whisper.cpp**. Aquí respondió `"engine":"whisper","model":"small"`.
- `--model small` **sí se acepta** aunque `--help` solo liste `tiny.en … small.en … large-v3`, y descarga el modelo **multilingüe** `ggml-small.bin` (488 MB). Nunca uses `.en` (CLAUDE.md).
- **¿Sin whisper-cpp?** Con `--no-runtime-install` responde `{"ok":false,"skipped":true,"reason":"whisper_unavailable"}`. Sin esa bandera (por defecto) **clona y compila whisper.cpp** solo (hay `cmake` y `gcc` aquí) en `~/.cache/hyperframes/whisper/whisper.cpp/build/bin/whisper-cli` y baja el modelo a `~/.cache/hyperframes/whisper/models/`. Primera vez: **117 s** en total (compilación + 488 MB); después `doctor` marca `whisper-cpp ok` y cada transcripción corta tarda segundos.
- Resultado: `transcript.json` en `--dir` (formato de la sección 8). En stderr, con `--json`, van líneas de progreso y palabras "en vivo" (con tiempos menos precisos que los del archivo final: usa el archivo).
- Calidad con voz es-MX (edge-tts, 5 s): 11 palabras, tiempos buenos; error en "omakase".
- Alternativa ya instalada en el venv compartido: `faster-whisper` (Python). Úsala si hiciera falta; el formato de salida hay que convertirlo al de arriba.
- `--to srt|vtt -o archivo` exporta subtítulos.

## 10. Fuentes locales [VERIFICADO]

```css
@font-face { font-family:"Zen Antique Soft"; src:url("assets/fonts/ZenAntiqueSoft-Regular-subset.woff2") format("woff2"); font-weight:400; font-display:block; }
@font-face { font-family:"DM Mono"; src:url("assets/fonts/DMMono-Medium.ttf") format("truetype"); font-weight:500; font-display:block; }
@font-face { font-family:"Cormorant"; font-style:italic; src:url("assets/fonts/Cormorant-Italic-wght.ttf") format("truetype"); font-weight:300 700; font-display:block; }
```

- Copia los archivos de `marca/fonts/` a `videos/<id>/assets/fonts/` (renombré `Cormorant-Italic[wght].ttf` → `Cormorant-Italic-wght.ttf`: los corchetes en URLs dan lata).
- Cada archivo que use una familia necesita su `@font-face` en el mismo archivo (dentro del `<template>` en escenas); si no, lint da `font_family_without_font_face` (error).
- `snapshot` imprime `Fonts: N loaded`: confírmalo. Zen Antique Soft (subset woff2) y DM Mono se vieron bien en el render.
- El subset de Zen solo trae latín + español + 森下 + kana/kanji básicos; para otros kanji usa el TTF completo (7 MB).

## 11. Errores típicos de lint/check (vistos aquí)

| Regla | Severidad | Causa / arreglo |
|---|---|---|
| `invalid_parent_traversal_in_asset_path` | error | Ruta con `../` (p. ej. `../vendor/gsap.min.js` en `compositions/`). Usa rutas desde la raíz del proyecto. *Ojo: en una corrida no salió y en otra sí; no confíes en que lint lo detecte siempre.* |
| `timeline_id_mismatch` | error | `window.__timelines["x"]` ≠ `data-composition-id`. |
| `gsap_css_transform_conflict` | error | `transform` en CSS + tween de x/y/scale. Usa `fromTo`. |
| `font_family_without_font_face` | error | Familia sin `@font-face` en el archivo. |
| `media_missing_id`, `media_crossorigin_breaks_preview` | error | `<audio>` sin `id` (render mudo) / con `crossorigin`. |
| `gsap_animates_clip_element` | error | `autoAlpha`/`visibility` sobre un `.clip`. |
| `content_overlap` (check) | error/aviso | Dos textos se enciman en algún momento muestreado (también si uno está a opacidad 0). |
| `overlapping_gsap_tweens` | aviso | Dos tweens de la misma propiedad se tocan. |
| `nested_structure_needs_subcomposition` | aviso | Escenas con hijos escritas inline en `index.html`: pásalas a `compositions/`. |
| `container_overflow` (check) | aviso/info | Zoom o capa que desborda; si es a propósito, `data-layout-allow-overflow`. El del bloque de flash queda como "info" (no bloquea). |
| `clip_ends_past_root_duration` | aviso | Un clip termina después del `data-duration` raíz. |

Ojo: un **error de lint apaga** las auditorías de layout y contraste (`check` reporta `0 samples` y parece limpio). Primero 0 errores de lint.
`npx hyperframes validate` sigue existiendo pero está obsoleto ("use check"); corre solo consola + contraste.

## 12. Preview, snapshot, render y QA (tiempos medidos)

| Paso | Comando (desde `videos/<id>/`) | Tiempo medido (prueba de 6 s) |
|---|---|---|
| Lint | `npx hyperframes lint` (`--verbose`, `--json`) | ~1 s |
| Gate | `npx hyperframes check` (`--json`, `--snapshots`, `--at 1,2.4`) | ~12 s |
| Fotogramas sin render | `npx hyperframes snapshot --at 0,2.4,3.6 --no-end -o /tmp/claude-0/<x>` | ~10 s (8 cuadros + `contact-sheet.jpg`) |
| Studio | `npx hyperframes preview --background` → `http://localhost:3002/#project/_prueba-6s` (el puerto puede cambiar); `preview --status`; `preview --stop` | arranca en segundos; respondió HTTP 200 |
| Borrador | `npx hyperframes render --quality draft --fps 30 --output ../../renders/<id>-borrador-vNN.mp4` | **13.3–15.9 s de render (15.2–18.3 s de reloj)** para 180 cuadros: setup 2 s, captura+encode 9.7–11.7 s con 2 workers, `beginframe · software gpu` |
| Final (solo con "render final") | `--quality high` (= `delivery`) | no probado |

- Calidades: `draft`, `looks` (por defecto, CRF 16), `delivery` (= `high`), `standard`. `--fps` por defecto toma `data-fps` de la raíz.
- Estimado para un reel de 30 s: ~5× la prueba → **~1–1.5 min** en borrador (más si hay video o efectos pesados).
- El render corre lint antes; con `--strict` falla si hay errores de lint.
- Al final imprime una línea de "Framey / desktop app": ignórala (no hay app de escritorio aquí).

QA que usé:

```bash
f=renders/prueba-6s-borrador-v01.mp4
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames:format=duration -of compact $f
ffmpeg -nostats -i $f -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):"
for t in 0 1 2.4 2.5 3.6 5.9; do ffmpeg -v error -y -ss $t -i $f -frames:v 1 /tmp/claude-0/hfprueba/fotograma_$t.jpg; done
```

Resultado de la prueba: h264 1080x1920, 30/1 fps, 180 cuadros, 6.000 s, AAC 48 kHz estéreo, 2.6 MB; −16.2 LUFS, pico −4.1 dBFS.

## 13. La prueba de 6 s (`videos/_prueba-6s`)

| Tiempo | Qué pasa | Cómo |
|---|---|---|
| 0.00 | "4 / ASIENTOS" ya en pantalla (gancho en el frame 0), cae de 135 % a 100 % en 6 frames + impacto grave | escena `escena-golpe`, `fromTo` scale; `impact-bass-1` vol 0.35 |
| 0.25 | etiqueta "1 BARRA" (DM Mono, oro) | fade+subida 120 ms |
| 0.0–2.4 | fondo negro cálido con grano sutil | componente `grain-overlay` pegado, opacidad 0.09 |
| 1.30 | pulso 1 → 1.08 → 1 del "4" (interrupción de patrón) | un tween con `yoyo` |
| 2.10–2.40 | empuje del bloque de texto a 112 % | `power3.in` |
| 2.36–2.6 | **flash blanco** (pico en el corte de 2.40) + whoosh | bloque `editorial-flash-overlay` (ranura 2.07, 0.5 s) + `whoosh` desde 2.24 |
| 2.40–6.0 | captura real "Máximo 4 personas por servicio", punch-in lento 100 → 105 % y punch a 109 % en 4.6 s | escena `escena-captura`, envoltorio `#ec-cam` |
| 3.0 / 3.25 / 3.5 | subtítulo kinético "máximo **4** personas" (el 4 en oro y 1.2×) + pop en el "4" | `fromTo` 100 ms por palabra, `pop` desde 3.13 |

"1 barra. 4 asientos." y "Máximo 4 personas por servicio." son textos reales de la web (`fuente/hechos.md`, A5/A6). Es una prueba técnica: no lleva voz ni música ni CTA, y no es para publicar.

Fuentes, imagen y SFX están copiados dentro de `videos/_prueba-6s/assets/`; GSAP en `vendor/`. Código completo (sin los `data-hf-id` que agrega Studio):

### `index.html` · Raíz: ranuras de escena, bloque de flash y SFX

```html
<!DOCTYPE html>
<html lang="es" data-resolution="portrait">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1080, height=1920">
    <title>Prueba 6 s · Morishita</title>
    <!-- GSAP local (vendor/): el render no depende del CDN -->
    <script src="vendor/gsap.min.js"></script>
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      html,
      body {
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #0a0908;
      }
      #root {
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: #0a0908;
      }
      /* Las ranuras de sub-composición llenan el cuadro */
      #root > div[data-composition-src] {
        position: absolute;
        inset: 0;
      }
      #flash {
        z-index: 20;
        pointer-events: none;
      }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="6" data-fps="30" data-width="1080" data-height="1920">
      <!-- Escena 1 · gancho "1 barra · 4 ASIENTOS" (0 – 2.4 s) -->
      <div id="el-golpe" data-composition-id="escena-golpe" data-composition-src="compositions/escena-golpe.html" data-start="0" data-duration="2.4" data-track-index="0" data-width="1080" data-height="1920"></div>

      <!-- Escena 2 · captura real del flujo de reserva con punch-in (2.4 – 6 s) -->
      <div id="el-captura" data-composition-id="escena-captura" data-composition-src="compositions/escena-captura.html" data-start="2.4" data-duration="3.6" data-track-index="1" data-width="1080" data-height="1920"></div>

      <!-- Transición: bloque del catálogo editorial-flash-overlay.
           Su golpe cae a 0.58 × duración: la rampa a blanco dura 0.04 s; con inicio 2.07 el pico cae en 2.40 s (el corte) -->
      <div id="flash" data-composition-id="editorial-flash-overlay" data-composition-src="compositions/editorial-flash-overlay.html" data-start="2.07" data-duration="0.5" data-track-index="2" data-width="1080" data-height="1920"></div>

      <!-- SFX: cada <audio> necesita id; data-start en segundos absolutos del reel -->
      <!-- impacto grave en el gancho (pico a 0.07 s del archivo) -->
      <audio id="sfx-impacto" src="assets/sfx/impact-bass-1.mp3" data-start="0" data-duration="2.1" data-track-index="10" data-volume="0.35"></audio>
      <!-- whoosh en la transición: su pico está a 0.16 s → arranca en 2.24 para pegar en 2.40 -->
      <audio id="sfx-whoosh" src="assets/sfx/whoosh.mp3" data-start="2.24" data-duration="0.57" data-track-index="11" data-volume="0.8"></audio>
      <!-- pop con la palabra clave "4" (3.25 s; pico del archivo a 0.12 s) -->
      <audio id="sfx-pop" src="assets/sfx/pop.mp3" data-start="3.13" data-duration="0.72" data-track-index="12" data-volume="0.4"></audio>
    </div>

    <script>
      // Timeline raíz (vacía): la animación vive en cada sub-composición
      const tl = gsap.timeline({ paused: true });
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
```

### `compositions/escena-golpe.html` · Escena 1: golpe "4 ASIENTOS" con grano

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8">
    <!-- El <head> de una sub-composición se descarta: todo va dentro de <template> -->
  </head>
  <body>
    <template>
      <style>
        @font-face {
          font-family: "Zen Antique Soft";
          src: url("assets/fonts/ZenAntiqueSoft-Regular-subset.woff2") format("woff2");
          font-weight: 400;
          font-display: block;
        }
        @font-face {
          font-family: "DM Mono";
          src: url("assets/fonts/DMMono-Medium.ttf") format("truetype");
          font-weight: 500;
          font-display: block;
        }
        #escena-golpe-root {
          position: absolute;
          inset: 0;
          overflow: hidden;
          background: radial-gradient(ellipse 80% 55% at 50% 42%, #13110e 0%, #0a0908 70%);
        }
        /* Centrado con flex dentro del área útil (x 65–1015, y 270–1248) */
        #eg-stack {
          position: absolute;
          left: 65px;
          right: 65px;
          top: 270px;
          height: 978px;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          gap: 8px;
        }
        #eg-eyebrow {
          display: block;
          font-family: "DM Mono", monospace;
          font-weight: 500;
          font-size: 32px;
          letter-spacing: 0.32em;
          color: #d4af6a;
          text-transform: uppercase;
          margin-bottom: 12px;
        }
        #eg-num {
          display: block;
          font-family: "Zen Antique Soft", serif;
          font-size: 400px;
          line-height: 0.9;
          color: #d4af6a;
          transform-origin: 50% 100%; /* crece hacia arriba: no pisa "ASIENTOS" */
        }
        #eg-word {
          display: block;
          font-family: "Zen Antique Soft", serif;
          font-size: 150px;
          line-height: 0.92;
          letter-spacing: -0.02em;
          color: #f5f0e8;
          transform-origin: 50% 0%; /* crece hacia abajo: no pisa el "4" */
        }
        /* grain-overlay (componente del catálogo), opacidad bajada a textura sutil */
        #eg-grain {
          position: absolute;
          inset: 0;
          overflow: hidden;
          pointer-events: none;
          z-index: 5;
        }
        @keyframes hf-grain-noise {
          0%, 100% { transform: translate(0, 0); }
          10% { transform: translate(-5%, -5%); }
          20% { transform: translate(-10%, 5%); }
          30% { transform: translate(5%, -10%); }
          40% { transform: translate(-5%, 15%); }
          50% { transform: translate(-10%, 5%); }
          60% { transform: translate(15%, 0); }
          70% { transform: translate(0, 10%); }
          80% { transform: translate(-15%, 0); }
          90% { transform: translate(10%, 5%); }
        }
        #eg-grain .grain-texture {
          position: absolute;
          top: -50%;
          left: -50%;
          width: 200%;
          height: 200%;
          background: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
          opacity: 0.09;
          animation: hf-grain-noise 0.5s steps(1) infinite;
        }
      </style>

      <div id="escena-golpe-root" data-composition-id="escena-golpe" data-width="1080" data-height="1920">
        <div id="eg-stack">
          <span id="eg-eyebrow">1 barra</span>
          <span id="eg-num">4</span>
          <span id="eg-word">ASIENTOS</span>
        </div>
        <div id="eg-grain" data-layout-ignore=""><div class="grain-texture"></div></div>
      </div>

      <script>
        (function () {
          const tl = gsap.timeline({ paused: true });
          // Gancho visible desde el frame 0: el número ya está en pantalla y "cae" en 6 frames
          tl.fromTo("#eg-num", { scale: 1.35 }, { scale: 1, duration: 0.2, ease: "power4.out" }, 0);
          tl.fromTo("#eg-word", { scale: 1.15 }, { scale: 1, duration: 0.2, ease: "power4.out" }, 0);
          tl.fromTo("#eg-eyebrow", { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.12, ease: "power2.out" }, 0.25);
          // Interrupción de patrón a 1.3 s: pulso 1 → 1.08 → 1 (un solo tween con yoyo, sin solapes)
          tl.to("#eg-num", { scale: 1.08, duration: 0.12, ease: "power2.out", yoyo: true, repeat: 1 }, 1.3);
          // Empuje hacia el flash (2.1 → 2.4 s)
          tl.fromTo("#eg-stack", { scale: 1 }, { scale: 1.12, duration: 0.29, ease: "power3.in" }, 2.1);
          window.__timelines["escena-golpe"] = tl;
        })();
      </script>
    </template>
  </body>
</html>
```

### `compositions/escena-captura.html` · Escena 2: captura real con punch-in y subtítulo kinético

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8">
  </head>
  <body>
    <template>
      <style>
        @font-face {
          font-family: "Zen Antique Soft";
          src: url("assets/fonts/ZenAntiqueSoft-Regular-subset.woff2") format("woff2");
          font-weight: 400;
          font-display: block;
        }
        #escena-captura-root {
          position: absolute;
          inset: 0;
          overflow: hidden;
          background: #0a0908;
        }
        /* El zoom va en un envoltorio interno (nunca en el clip temporizado) */
        #ec-cam {
          position: absolute;
          inset: 0;
          transform-origin: 8% 24%; /* ancla a la izquierda para no cortar "PASO 01" ni "¿Cuántos" */
        }
        #ec-img {
          display: block;
          width: 1080px;
          height: 1920px;
          object-fit: cover;
        }
        /* Scrim neutro (negro de marca) detrás del subtítulo: no tiñe la captura */
        #ec-scrim {
          position: absolute;
          left: 0;
          right: 0;
          top: 860px;
          height: 460px;
          background: linear-gradient(180deg, rgba(10, 9, 8, 0) 0%, rgba(10, 9, 8, 0.97) 20%, rgba(10, 9, 8, 0.97) 80%, rgba(10, 9, 8, 0) 100%);
        }
        /* Subtítulo kinético dentro del área útil (y 1010–1180) */
        #ec-sub {
          position: absolute;
          left: 65px;
          right: 65px;
          top: 1010px;
          height: 170px;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 26px;
        }
        #ec-sub .w {
          display: inline-block;
          font-family: "Zen Antique Soft", serif;
          font-size: 104px;
          line-height: 1.05;
          letter-spacing: -0.01em;
          color: #f5f0e8;
          transform-origin: 50% 80%;
        }
        #ec-sub .w.key {
          color: #d4af6a;
        }
      </style>

      <div id="escena-captura-root" data-composition-id="escena-captura" data-width="1080" data-height="1920">
        <div id="ec-cam" data-layout-allow-overflow="">
          <img id="ec-img" src="assets/img/captura-reserva-comensales-oscuro__maximo-4.jpg" alt="Paso 01 del flujo de reserva: Máximo 4 personas por servicio">
        </div>
        <div id="ec-scrim"></div>
        <div id="ec-sub">
          <span class="w" id="ec-w1">máximo</span>
          <span class="w key" id="ec-w2">4</span>
          <span class="w" id="ec-w3">personas</span>
        </div>
      </div>

      <script>
        (function () {
          const tl = gsap.timeline({ paused: true });
          // Tiempos LOCALES de la escena (0 = 2.4 s del reel)
          // Punch-in lento 100 → 105 % en 2.2 s
          tl.fromTo("#ec-cam", { scale: 1 }, { scale: 1.05, duration: 2.2, ease: "sine.out" }, 0);
          // Punch-in rápido a 109 % en 6 frames (2.2 s local = 4.6 s del reel)
          tl.to("#ec-cam", { scale: 1.09, duration: 0.2, ease: "power3.out" }, 2.2);
          // Subtítulo palabra por palabra, entrada de 100 ms; la palabra clave en oro y a 1.2×
          tl.fromTo("#ec-w1", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.1, ease: "power2.out" }, 0.6);
          tl.fromTo("#ec-w2", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1.2, duration: 0.1, ease: "power2.out" }, 0.85);
          tl.to("#ec-w2", { scale: 1, duration: 0.18, ease: "power2.out" }, 0.95);
          tl.fromTo("#ec-w3", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.1, ease: "power2.out" }, 1.1);
          window.__timelines["escena-captura"] = tl;
        })();
      </script>
    </template>
  </body>
</html>
```

### `compositions/editorial-flash-overlay.html` · Bloque del catálogo, ya adaptado (1080x1920 y GSAP local)

```html
<!DOCTYPE html><!-- hyperframes-registry-item: editorial-flash-overlay -->

<html lang="en">
  <head>
    <meta charset="UTF-8">
    <script src="vendor/gsap.min.js"></script>
    <style>
      *,
      *::before,
      *::after {
        box-sizing: border-box;
      }

      html,
      body {
        width: 1080px;
        height: 1920px;
        margin: 0;
        overflow: hidden;
        background: transparent;
      }

      #ef-flash {
        --hf-editorial-flash-wash: 255 253 250;
        --hf-editorial-flash-warm: 255 174 105;
        --hf-editorial-flash-cool: 183 218 255;
        position: absolute;
        inset: -12%;
        overflow: hidden;
        pointer-events: none;
      }

      #ef-flash .ef-layer {
        position: absolute;
        inset: 0;
        opacity: 0;
        will-change: opacity, transform;
      }

      #ef-wash {
        background: rgb(var(--hf-editorial-flash-wash));
      }

      #ef-core {
        inset: -18%;
        background: radial-gradient(
          ellipse 68% 92% at 37% 47%,
          rgb(255 255 255) 0%,
          rgb(255 255 255 / 98%) 20%,
          rgb(var(--hf-editorial-flash-wash) / 86%) 45%,
          rgb(var(--hf-editorial-flash-warm) / 32%) 67%,
          transparent 86%
        );
        mix-blend-mode: screen;
        transform-origin: 38% 48%;
      }

      #ef-sweep {
        inset: -28%;
        background: linear-gradient(
          108deg,
          transparent 21%,
          rgb(var(--hf-editorial-flash-warm) / 10%) 38%,
          rgb(var(--hf-editorial-flash-wash) / 90%) 49%,
          rgb(255 255 255 / 98%) 53%,
          rgb(var(--hf-editorial-flash-cool) / 24%) 62%,
          transparent 79%
        );
        mix-blend-mode: screen;
      }
    </style>
  </head>
  <body>
    <div id="editorial-flash-overlay" data-composition-id="editorial-flash-overlay" data-start="0" data-duration="4" data-width="1080" data-height="1920">
      <div id="ef-flash" aria-hidden="true">
        <div id="ef-wash" class="ef-layer"></div>
        <div id="ef-core" class="ef-layer" data-layout-allow-overflow=""></div>
        <div id="ef-sweep" class="ef-layer" data-layout-allow-overflow=""></div>
      </div>
    </div>

    <script>
      window.__timelines = window.__timelines || {};

      var flash = document.getElementById("ef-flash");
      var host = flash && flash.closest("[data-composition-id]");
      if (!host) throw new Error("Editorial Flash could not find its composition host");

      var compositionId = host.getAttribute("data-composition-id");
      var duration = Number(host.getAttribute("data-duration")) || 4;
      var hit = Math.max(0.12, duration * 0.58);
      var tl = gsap.timeline({ paused: true });

      tl.to({}, { duration: duration, ease: "none" }, 0);
      tl.to("#ef-wash", { opacity: 0.92, duration: 0.04, ease: "power4.in" }, hit);
      tl.fromTo(
        "#ef-core",
        { opacity: 0, scale: 0.86, rotation: -5 },
        { opacity: 1, scale: 1, rotation: -5, duration: 0.05, ease: "power4.in" },
        hit - 0.01,
      );
      tl.fromTo(
        "#ef-sweep",
        { opacity: 0, xPercent: -12, rotation: -2 },
        { opacity: 0.9, xPercent: 8, rotation: -2, duration: 0.04, ease: "power4.in" },
        hit,
      );
      tl.to("#ef-wash", { opacity: 0, duration: 0.18, ease: "power3.out" }, hit + 0.04);
      tl.to(
        "#ef-core",
        { opacity: 0, scale: 1.18, rotation: -5, duration: 0.34, ease: "power2.out" },
        hit + 0.04,
      );
      tl.to(
        "#ef-sweep",
        { opacity: 0, xPercent: 28, rotation: -2, duration: 0.3, ease: "power2.out" },
        hit + 0.04,
      );

      window.__timelines[compositionId] = tl;
    </script>
  </body>
</html>
```

## 14. Pendientes y cosas no probadas

- No probado: transiciones shader (`whip-pan`, `glitch`, `flash-through-white`), `whip-pan-cut`, `count-up`, `camera-shake`, `cta-lockup`, `testimonial-*`, `device-frame-stage`, Parakeet, render `--quality high`, `normalize-audio`, `beats`.
- Música: no hay pista con licencia todavía; `media-use resolve --type bgm` necesita el CLI `heygen` con sesión (no se inicia sesión aquí). El carve se probó con una cama sintética.
- `marca/frame.md` sugiere `@font-face` con `../../marca/fonts/…`: no funciona en HyperFrames (rutas fuera del proyecto); copiar las fuentes al proyecto.
