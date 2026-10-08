# frame.md: marca de Morishita para reels (1080x1920)

> **Estado:** PROPUESTA del 2026-10-08, sacada del CSS de la web en vivo (`index.html`, idéntico al de producción). CLAUDE.md la deja como "[PENDIENTE, sácalos del CSS y confírmamelos]": **falta el OK del dueño.**
> Manda sobre esto: CLAUDE.md (reglas) y `estilo.md` (ritmo medido). Este archivo define el **look**: color, tipografía, logo, movimiento y zonas.
> Vista previa: `marca/logo/preview-logos.png` (todas las versiones del logo) y `marca/logo/preview-frame-1080x1920.png` (maqueta con zonas seguras, subtítulo kinético y logo).

---

## 1. Paleta (tokens)

La web tiene **dos temas**: claro (crema y tinta, acento rosa sakura) y oscuro (casi negro y crema, acento dorado). En el tema oscuro, el rosa de acento **se vuelve dorado**. El tema cambia solo: oscuro de noche (19:00–07:00) o si el sistema está en oscuro.

**Para reels, el tema base es el OSCURO** (CLAUDE.md: "contraste alto, negros profundos, cálido en carnes y fuego"). El claro queda para cierres o tarjetas de dato de "respiro".

### 1.1 Tema oscuro (base de los reels) · CSS `[data-theme="dark"]`

| Token | Hex | En la web | En reels |
|---|---|---|---|
| `--negro` (paper) | `#0a0908` | fondo principal; fondo del favicon | fondo, scrims, barras |
| `--negro-calido` (paper-warm) | `#13110e` | secciones | degradado de fondo (`#0a0908 → #13110e`, como el body de la web) |
| `--negro-tarjeta` (paper-deep) | `#1a1814` | tarjetas | tarjetas de dato o reseña |
| `--negro-profundo` | `#050403` | fondo de la sección de reseñas | fondo de la reseña |
| `--crema` (ink) | `#f5f0e8` | texto principal y logo | texto principal y logo · contraste 17.5:1 sobre negro |
| `--crema-media` (ink-mid) | `#d8d0c2` | texto secundario | texto secundario · 13:1 |
| `--gris-calido` (ink-soft) | `#9a9285` | texto suave | autor de reseña, notas pequeñas · 6.5:1 |
| `--oro` (gold / sakura-d) | `#d4af6a` | acento: cursivas de títulos, eyebrows, botones, estrellas, **kanji del favicon** | **acento único**: palabra clave del subtítulo, cifras, estrellas, línea divisoria · 9.6:1 |
| `--oro-hover` | `#e0bd7e` | hover de los botones dorados | brillo/flash sobre el oro, highlights |
| `--linea-oscura` (line) | `#2e2a23` | divisores | divisores sutiles |
| `--sakura-apagado` (sakura) | `#9a6470` | pétalos en oscuro | partículas de pétalo a baja opacidad (nunca texto: 4.2:1) |

### 1.2 Tema claro · CSS `:root`

| Token | Hex | En la web | En reels |
|---|---|---|---|
| `--papel` (paper) | `#faf8f4` | fondo crema (CLAUDE.md) | fondo de tarjetas de "respiro" o del cierre claro |
| `--papel-calido` (paper-warm) | `#f3ede4` | secciones | fondo alterno |
| `--papel-profundo` (paper-deep) | `#ece4d8` | tarjetas | tarjetas |
| `--tinta` (ink) | `#0d0d0b` | texto, logo, botón primario | texto sobre crema · 18.3:1 |
| `--tinta-media` (ink-mid) | `#2a2925` | texto secundario | — |
| `--tinta-suave` (ink-soft) | `#6b6760` | leads y tagline del logo | texto secundario · 5.3:1 |
| `--sakura-oscuro` (sakura-d) | `#c4607a` | **acento** en claro: eyebrows, cursivas, botones hover | acento sobre crema **solo en texto grande** (3.7:1: ≥ 60 px) |
| `--sakura` | `#e8a0b0` | pétalos, decoración | solo decoración (sobre crema 2:1, nunca texto) |
| `--sakura-claro` (sakura-l) | `#f5d0da` | acento de la sección de reseñas (fondo tinta) | acento sobre tinta `#0d0d0b` (13.8:1) |
| `--sakura-palido` (sakura-ll) | `#fdf0f3` | fondos suaves | — |
| `--oro-claro` (gold) | `#c9a45c` | acento dorado en claro | **no para texto sobre crema** (2.2:1); sí sobre negro (8.5:1) |
| `--linea` (line) | `#ddd5c8` | divisores; línea vertical del logo | divisor del logo en claro |

### 1.3 Reglas de color

1. **Un solo acento por cuadro:** oro (`#d4af6a`) sobre oscuro y rosa `#c4607a` sobre crema. No mezclar oro y rosa en el mismo cuadro (la web nunca lo hace).
2. El acento va en la **palabra clave**, la cifra o la estrella. Nunca en párrafos.
3. **Nunca** se tiñe la foto del producto con la paleta: ni duotonos, ni overlays de color, ni LUTs que cambien el color real del pescado o de la carne (CLAUDE.md). Para que el texto se lea sobre una foto se usa un **scrim neutro**: degradado de `#0a0908` al 0–70 % de opacidad, en la parte baja del área útil.
4. Flash de transición: **crema `#f5f0e8`** (más cálido que el blanco puro) en 2–3 frames.
5. Prohibido: neón, arcoíris, rojo "de oferta", amarillo puro. El oro es mate y cálido, no brillante.

### 1.4 Bloque CSS listo para HyperFrames

```css
:root{
  /* oscuro (base reels) */
  --negro:#0a0908; --negro-calido:#13110e; --negro-tarjeta:#1a1814; --negro-profundo:#050403;
  --crema:#f5f0e8; --crema-media:#d8d0c2; --gris-calido:#9a9285;
  --oro:#d4af6a; --oro-hover:#e0bd7e; --linea-oscura:#2e2a23; --sakura-apagado:#9a6470;
  /* claro */
  --papel:#faf8f4; --papel-calido:#f3ede4; --papel-profundo:#ece4d8;
  --tinta:#0d0d0b; --tinta-suave:#6b6760; --sakura-oscuro:#c4607a; --sakura:#e8a0b0;
  --sakura-claro:#f5d0da; --linea:#ddd5c8;
  /* tipos */
  --display:'Zen Antique Soft',serif;
  --serif:'Cormorant',Georgia,serif;
  --mono:'DM Mono',ui-monospace,monospace;
  /* movimiento (de la web) */
  --ease-ui:cubic-bezier(.4,0,.2,1);      /* transiciones .35s */
  --ease-in:cubic-bezier(.2,.7,.2,1);     /* screenIn .5s */
  --ease-sello:cubic-bezier(.2,.9,.3,1.2);/* hankoIn .8s, con rebote */
}
```

---

## 2. Tipografías

La web carga (Google Fonts): `Zen Antique Soft` · `Cormorant: ital,wght@0,300;0,400;0,500;1,300;1,400` · `DM Mono: wght@300;400`. Las tres tienen licencia **SIL Open Font License 1.1** (OFL, uso comercial permitido; la licencia va junto a cada fuente). Descargadas de `github.com/google/fonts` (TTF completos, sin recortes por unicode-range) a `marca/fonts/`.

| Rol | Familia | Pesos | Archivo(s) en `marca/fonts/` | Cómo lo usa la web | Cómo se usa en reels |
|---|---|---|---|---|---|
| **Display** (títulos, cifras, kanji) | Zen Antique Soft | 400 (única) | `zen-antique-soft/ZenAntiqueSoft-Regular.ttf` (7 MB, completo) · `ZenAntiqueSoft-Regular-subset.woff2` (68 KB: latín + español + 森下 + kana + kanji básicos) | H1 "Omakase" (54–108 px, interlineado .92, tracking −.02em), títulos de sección (tracking −.015em), números del flujo ("2", "1:00 pm"), kanji 森下 del logo | Golpes de texto, cifras ("14", "4"), subtítulos kinéticos, kanji. **Usar el woff2 recortado en HTML** (el TTF pesa 7 MB). |
| **Texto y cursiva de acento** | Cormorant | 300, 400, 500 + cursiva 300, 400 | `cormorant/Cormorant[wght].ttf` y `Cormorant-Italic[wght].ttf` (variables 300–700) · estáticas en `cormorant/static/` (Light, Regular, Medium, LightItalic, Italic) | Cuerpo (16 px), segunda línea en cursiva 300 de cada título ("*Confia en el chef*", "*Solo dos días por semana.*"), leads y citas en cursiva | Segunda línea en cursiva del acento; texto de reseñas; frase del chef. Las **estáticas** sirven para ffmpeg/Pillow, que no manejan fuentes variables. |
| **Mono / etiquetas** | DM Mono | 300, 400 (web) · 500 (extra, no está en la web) | `dm-mono/DMMono-Light.ttf`, `-Regular`, `-Medium` (+ cursivas) | Eyebrows en MAYÚSCULAS con tracking .32em, botones (.24em), menú, "MORISHITA" (.205em) y "AUTHENTIC JAPANESE CUISINE" del logo | Etiquetas de contexto ("TIEMPO 01 · NIGIRI", "ENSENADA · BAJA CALIFORNIA"), autor de la reseña, CTA ("RESERVA EN EL LINK"). Medium 500 a tamaños chicos en video. |
| **Kanji 森下** | Zen Antique Soft | 400 | ídem | Logo del header, loader y footer | Logo y sello. **El `favicon.png` usa OTRA tipografía** (un mincho más fino): no mezclarlas en un mismo cuadro. |

`@font-face` para un proyecto en `videos/<id>/` (rutas relativas; si HyperFrames exige los assets dentro del proyecto, copia los archivos y ajusta la ruta):

```css
@font-face{font-family:'Zen Antique Soft';src:url('../../marca/fonts/zen-antique-soft/ZenAntiqueSoft-Regular-subset.woff2') format('woff2');font-weight:400;font-display:block}
@font-face{font-family:'Cormorant';src:url('../../marca/fonts/cormorant/Cormorant[wght].ttf') format('truetype');font-weight:300 700;font-display:block}
@font-face{font-family:'Cormorant';font-style:italic;src:url('../../marca/fonts/cormorant/Cormorant-Italic[wght].ttf') format('truetype');font-weight:300 700;font-display:block}
@font-face{font-family:'DM Mono';src:url('../../marca/fonts/dm-mono/DMMono-Regular.ttf') format('truetype');font-weight:400;font-display:block}
@font-face{font-family:'DM Mono';src:url('../../marca/fonts/dm-mono/DMMono-Medium.ttf') format('truetype');font-weight:500;font-display:block}
```

Si el subset no tiene un kanji que necesites, usa el TTF completo o regenera el subset con `pyftsubset` (instrucción en la sección 7).

### Escala tipográfica para 1080x1920 (mínimos de legibilidad en el teléfono)

| Uso | Familia | Tamaño | Tracking | Interlineado |
|---|---|---|---|---|
| Golpe / cifra ("14", "4") | Zen Antique Soft | 220–420 px | −.02em | .9 |
| Titular de 1–4 palabras | Zen Antique Soft | 120–170 px | −.02em | .92 |
| Subtítulo kinético (voz) | Zen Antique Soft | 84–110 px | −.01em | 1.05 |
| Cursiva de acento (2.ª línea) | Cormorant Italic 300 | 80–120 px | 0 | 1.05 |
| Reseña (cita) | Cormorant Italic 400 | 54–64 px | 0 | 1.35 |
| Etiqueta / eyebrow | DM Mono 400–500, MAYÚSCULAS | 28–36 px (**mínimo 26**) | .28–.32em | 1.2 |
| Autor / nota | DM Mono 400, MAYÚSCULAS | 26–30 px | .2em | 1.2 |

Escritura: frases en minúscula normal (no TODO MAYÚSCULAS salvo las etiquetas mono). Cifras con número ("14 tiempos", "$1,850 MXN"). Ortografía correcta aunque la web traiga erratas ("Confía", "experiencia").

---

## 3. Logo

Archivos en `marca/logo/`. Los SVG tienen el **texto convertido a trazos** (no dependen de fuentes instaladas) con la geometría exacta del header de la web (`viewBox 0 0 360 72`: kanji 60 px en x=8, divisor vertical en x=135, "MORISHITA" 19.5 px con tracking 4, tagline 8.5 px con tracking 3.2). Verificado contra el SVG original con texto vivo: coinciden (ver `preview-logos.png`).

| Archivo | Para | Colores |
|---|---|---|
| `logo-horizontal-fondo-claro.svg/.png` | sobre crema | tinta `#0d0d0b`, tagline `#6b6760`, divisor `#ddd5c8` (= web en claro) |
| `logo-horizontal-fondo-oscuro.svg/.png` | sobre negro | todo crema `#f5f0e8`, divisor `#2e2a23` (= web en oscuro) |
| `logo-horizontal-fondo-oscuro-dorado.svg` | sobre negro | **PROPUESTA**: kanji oro `#d4af6a` (como el favicon), resto crema |
| `logo-vertical-fondo-claro.svg/.png` | **cierre/CTA 9:16** sobre crema | kanji arriba, divisor corto, MORISHITA, tagline |
| `logo-vertical-fondo-oscuro.svg/.png` | **cierre/CTA 9:16** sobre negro | crema |
| `logo-vertical-fondo-oscuro-dorado.svg/.png` | cierre sobre negro | **PROPUESTA**: kanji y divisor en oro, MORISHITA crema, tagline `#d8d0c2` |
| `sello-morishita-dorado-fondo-negro.svg` · `-dorado-transparente.svg/.png` · `-tinta-transparente.svg` | sello 森 sobre 下 (vertical, como el favicon) | oro o tinta. Ojo: es Zen Antique Soft, **no** la misma tipografía del favicon. |
| `favicon.png` | copia de `/favicon.png` de la web (512x512, 森下 vertical `#d4af6a` sobre `#0a0908`) | avatar/sello; tipografía mincho distinta |
| `logo-web-original-texto.svg` | el SVG original de la web, con texto vivo (solo referencia) | — |

Los PNG son transparentes: el vertical mide 900 px de ancho y el horizontal 1104 px.

**Reglas de logo**
1. **Nunca al inicio** del reel (CLAUDE.md: nada de logo ni intro en el gancho). El logo vive en el **cierre/CTA** (últimos 3–6 s) y, si acaso, como sello pequeño en una tarjeta de dato.
2. Siempre **dentro del área útil** (x 65–1015, y 270–1248). En el cierre, el vertical va entre **480 y 720 px de ancho**, centrado. Por debajo de ~700 px el tagline "AUTHENTIC JAPANESE CUISINE" ya no se lee (queda decorativo): si importa que se lea, ponlo aparte como texto DM Mono de ≥ 28 px.
3. Espacio libre alrededor ≥ la altura de "MORISHITA" en todos los lados.
4. Solo los colores de las versiones de arriba. Sin deformar, sin rotar (salvo la animación de sello), sin contornos, sin sombras duras ni glow. Sobre una foto: solo con scrim oscuro detrás.
5. No reescribir el logo con otra tipografía (la imagen del menú usa una sans y dice "QUISINE": no tomarla como referencia).
6. Las versiones **dorado** son propuesta: el oro sale del favicon y del acento oscuro de la web, pero el header de la web es monocromo.

---

## 4. Personalidad de movimiento: premium, dopamínico ≠ ruidoso

**Idea:** la energía está en el **ritmo del corte y en las entradas del texto**, no en el exceso de efectos. Rápido en el gancho y en las transiciones; **respiro** en el plato estrella. Si se siente caótico o "barato", se baja el ritmo (CLAUDE.md).

Vocabulario de movimiento tomado de la web (mantiene la coherencia de marca):

| Movimiento | En la web | En reels |
|---|---|---|
| **Entrada suave** (`screenIn`) | opacidad 0→1 + translateY 12 px → 0, .5 s, `cubic-bezier(.2,.7,.2,1)` | entrada de subtítulos y tarjetas, comprimida a **80–120 ms** (subtítulo) o 300–500 ms (tarjeta), misma curva |
| **Pop** (`pop`) | escala 1 → 1.2 → 1 en .28 s (el número de comensales) | palabra clave al aparecer (1.2×) y cifras al caer |
| **Sello** (`hankoIn`) | 森 entra de escala .2 y −30° a 1 y 0° en .8 s con rebote `cubic-bezier(.2,.9,.3,1.2)` | **firma del cierre**: el sello 森下 cae como hanko sobre el CTA, con un golpe grave suave |
| **Pétalos** (`petalFall`) | pétalos sakura cayendo en el fondo | partículas de pétalo a baja opacidad (≤ 35 %), **máximo 1–2 momentos por reel**, nunca encima del plato estrella |
| **Transición UI** | .35 s `cubic-bezier(.4,0,.2,1)`, hover con translateY −2 px | microdesplazamientos de botones o tarjetas en el CTA |
| **Pulso** (`plPulse`) | tres puntos con escala .7↔1 en 1.2 s | indicador "disponible" en el CTA (punto oro que respira) |

**Sí:**
- Punch-in de 108–118 % en 6–8 frames sobre el detalle (corte del pescado, textura del arroz).
- Ken Burns lento (102 → 108 % en 2–3 s) en fotos fijas: todo el material es foto, no hay video.
- Flash crema de 2–3 frames y whip pan en los cambios de bloque; un glitch sutil **solo en el texto** y en ≤ 3 frames.
- Conteo en las cifras ("0 → 14") con pop al final.
- Hold de 1.5–2 s, sin texto encima, en la foto más fuerte del producto.

**No:**
- Glitch RGB, shake o distorsión **sobre la comida** (cambia el color real y se ve barato).
- Más de un efecto a la vez sobre la misma imagen.
- Rebotes elásticos exagerados, giros 3D, emojis animados, stickers.
- Texto que entra letra por letra y tarda en leerse (máximo 120 ms por bloque).
- Cortes rápidos encima del CTA (≥ 3 s estable).

---

## 5. Zonas seguras 1080x1920 (de CLAUDE.md)

```
y=0    ┌───────────────────────────────┐
       │  UI de Instagram (14 %)       │  nada importante
y=270  ├──┬─────────────────────────┬──┤
       │6%│                         │6%│
       │  │   ÁREA ÚTIL 950 x 978   │  │  x 65–1015 · y 270–1248
       │  │                         │  │  todo texto, cifras, logo y CTA
y=1248 ├──┴─────────────────────────┴──┤
       │  caption, botones, audio      │  35 % inferior: nada importante
y=1920 └───────────────────────────────┘
```

- **Área útil: x 65–1015, y 270–1248.** Todo texto, cifra, logo y CTA va adentro.
- Recomendación de colocación:
  - Etiqueta mono arriba: y ≈ 300–360.
  - Golpe o titular: tercio central (y ≈ 520–900).
  - Subtítulo kinético de la voz: **y ≈ 900–1180** (abajo del área útil, nunca debajo de 1248).
- La foto puede llenar los 1920 px (fondo a sangre), pero su parte importante (el plato, la mano, el corte) debe caer dentro de y 270–1248.
- Las capturas de la web (`assets/fotos/web/captura-reserva-*.png`, 1082 px de ancho) se montan como **teléfono flotante** a 600–760 px de ancho dentro del área útil, o recortadas al bloque clave (calendario, horarios, ficha de precio).

---

## 6. Subtítulos kinéticos (palabra clave resaltada)

Base (CLAUDE.md): 1–3 palabras por bloque, palabra clave resaltada (color de marca o escala 1.2×), entrada de 80–120 ms, dentro del área útil.

| Estilo | Cuándo | Especificación |
|---|---|---|
| **S1 · Voz** (default) | todo lo que dice la voz | Zen Antique Soft 92–104 px, crema `#f5f0e8`, centrado, máximo 2 líneas de ≤ 16 caracteres. Clave en **oro `#d4af6a` + escala 1.2×** (pop .28 s). Entrada: opacidad 0→1 + y +12 px → 0 en 100 ms (`--ease-in`). Salida: corte seco con el siguiente bloque (sin fade lento). Legibilidad sobre foto: `text-shadow: 0 4px 24px rgba(10,9,8,.6)` + scrim inferior. |
| **S2 · Golpe** | cifras y momentos clave ("14 TIEMPOS", "4 ASIENTOS", "SÁB · DOM") | Cifra en Zen Antique Soft 260–420 px en oro, con conteo y pop; la palabra en DM Mono 500 de 40–56 px, MAYÚSCULAS, tracking .3em, en crema. SFX: pop o impacto. Máximo 1 por cada 5–6 s. |
| **S3 · Título con cursiva** | apertura de un bloque o "respiro" (eco del estilo de la web) | Línea 1 en Zen Antique Soft 130–160 px crema; línea 2 en Cormorant Italic 300 de 90–110 px en oro. Ejemplo literal: "Cuatro asientos." / *"Solo dos días por semana."* |
| **S4 · Etiqueta** | contexto de la foto ("TIEMPO 01 · NIGIRI", "ENSENADA · BAJA CALIFORNIA") | DM Mono 400–500 de 28–34 px, MAYÚSCULAS, tracking .32em, en oro, con filetes de 56–80 px a los lados (como `.section-eyebrow` de la web). Y ≈ 300–360. |
| **S5 · Reseña** | prueba social (20–28 s) | Tarjeta `#1a1814` o fondo `#050403`; ★★★★★ en oro de 48 px; cita en Cormorant Italic 400 de 56–62 px en crema (máximo 3–4 líneas; si es más larga, en 2 tarjetas); autor en DM Mono 28 px MAYÚSCULAS tracking .2em en `#9a9285`, **exactamente como en hechos.md (e)**. Alternativa: usar la captura real `fuente/capturas/resena-tN-dark.png`. |
| **S6 · CTA** | últimos 4–6 s | Estable ≥ 3 s, sin cortes encima. Línea de acción en Zen Antique Soft 96–120 px ("Reserva en el link"), con la clave en oro; dato real debajo en DM Mono 32 px (el texto sale de hechos.md, por ejemplo "CUATRO LUGARES POR SESIÓN" / "SÁB · DOM"); logo vertical 480–720 px; sello 森下 con la animación hanko. |

Reglas de la palabra clave:
- **Una** por bloque, y debe ser el sustantivo o la cifra que vende: "**14** tiempos", "solo **4** asientos", "**sábado** y domingo", "**reserva**".
- La clave se resalta con color **o** con escala 1.2×. Las dos a la vez solo en el gancho y en el CTA.
- Nunca se resalta "Wagyu" ni "Kobe" en este lote.
- Sincronía: el bloque aparece **en la sílaba de inicio** de su primera palabra (de `voz/<id>.words.json`), con ±1 frame de tolerancia.

---

## 7. Mantenimiento

- Regenerar los SVG del logo (los trazos salen de `marca/fonts/` con fontTools): `python -I marca/logo/scripts/make_logos.py marca/fonts marca/logo` (con fonttools instalado). Vistas previas y PNG transparentes: `python -I marca/logo/scripts/preview_logos.py <ruta abs marca/logo> <ruta abs marca/fonts> /tmp/preview.html` (Playwright + Chromium de `/opt/pw-browsers/chromium`). Maqueta 9:16: `marca/logo/scripts/preview_frame.py`.
- Subset del display con más kanji: `pyftsubset ZenAntiqueSoft-Regular.ttf --unicodes="U+0020-007E,U+00A0-00FF,U+2010-2027,U+3000-303F,U+3041-3096,U+30A0-30FF" --text="森下…" --flavor=woff2 --output-file=ZenAntiqueSoft-Regular-subset.woff2` (necesita `fonttools` y `brotli`).
- Al aprobar, mover lo que el dueño confirme a la línea "Marca" de CLAUDE.md (reemplazando el [PENDIENTE]).
