---
workflow: general-video
flow: companion
storyboard: no (guion aprobado como plan de tomas; ver tabla)
format: 1080x1920 · 30 fps · ~38 s · español
---

# BRIEF · r01-vale-cada-peso (borrador v01)

Edición según `reels/estilo.md` (si no existe, los valores dopamínicos de `reels/CLAUDE.md`), marca según `reels/marca/frame.md`, contenido, voz y CTA según `reels/CLAUDE.md` y `reels/guiones/lote-01/r01-vale-cada-peso.md` (v02). Guía técnica verificada: `reels/docs/hyperframes-notas.md`.

## Regla de oro de material
SOLO material real o permitido: tipografía, logo, texturas/tinta/grano/partículas/humo generados, capturas REALES (Google y flujo de reserva). **Prohibido** usar cualquier foto de comida, barra, chef o comensales de `assets/fotos/web/` (son IA). Sin Wagyu ni Kobe. No mostrar la dirección de la ficha de Google (recortarla), ni el temporizador de la web.

## Audio
- Voz: `reels/voz/r01/r01.wav` (31.61 s, inicia en t=0). Timestamps por palabra: `reels/voz/r01/r01.words.json`. Normalizar la voz para que la mezcla final dé −14 LUFS integrado, pico ≤ −1 dBTP; voz siempre clara.
- Música: `reels/audio/musica/morishita-bed-B-120.wav` (120 BPM, original, sintetizada) con **media-start 20.3 s** → reel 0 s = drop; respiro bajo las reseñas (11.7–19.7 s); rebuild bajo tiempos/asientos/pregunta (19.7–25.7 s); **drop2 cae exacto en 25.7 s = revelación**; salida/acorde final ~35.7 s; fade-out últimos 1.5 s. Carve/ducking bajo la voz (≈ −10 a −14 dB mientras habla).
- SFX: `reels/audio/sfx/synth/` y `reels/audio/sfx/bundled/` (ver sus README: restar el segundo del golpe). Whoosh en transiciones, pop/click en textos, boom en 0 s y 25.7 s, riser antes de 25.7, rin en reseñas, tap en CTA, hyoshigi en el cierre. Sin tapar la voz.
- Copiar todo asset DENTRO del proyecto (lint prohíbe rutas con `../`).

## Plan de tomas (tiempos de la voz real)
| t (s) | Voz | Pantalla | Visual / asset | Movimiento | SFX |
|---|---|---|---|---|---|
| 0.00–2.95 | ¿Vale mil ochocientos cincuenta pesos un omakase? | "¿VALE" + **$1,850** gigante oro (conteo 0→1,850 en ~0.6 s, visible desde frame 0 con valor final legible para miniatura) + "MXN POR PERSONA" + "¿un omakase?" | fondo negro #0a0908 + tinta sumi/grano | golpe escala 1.15→1 en 6 frames, partículas doradas | boom t=0, ticks, hyoshigi |
| 3.00–4.70 | No te lo decimos nosotros. | "NO LO DECIMOS" / "NOSOTROS" palabra a palabra | tinta | flash crema 2 fr | whoosh, pops |
| 4.77–8.45 | Cuatro punto nueve estrellas, en cuarenta y una reseñas de Google. | **4,9 ★★★★★** (conteo) + "41 RESEÑAS DE GOOGLE" | captura REAL `fuente/capturas/resenas/00-cabecera-4-9-41-resenas.png` recortada SIN la línea de dirección, sobre tarjeta clara | estrellas pop 1×1, punch-in lento | 5 pops, rin |
| 8.55–11.40 | «Fue una experiencia espectacular de principio a fin.» | cita literal "…fue una experiencia **espectacular** de principio a fin" — Lucia Ojeda · Google ★★★★★ | tarjeta tipográfica (Cormorant itálica) + mini captura real `01-lucia-ojeda-5estrellas.png` | palabras se iluminan al sonar | rin |
| 11.53–15.20 | «La chef fue atenta y amable, explicando cada pieza con detalle.» | "La chef fue atenta y amable, explicando **cada pieza con detalle**." — Lucia Ojeda | tarjeta 2 (respiro de música) | whip horizontal 6 fr de entrada | whoosh |
| 15.39–16.90 | «Producto super fresco.» | "Producto super fresco !!" (literal) — Alejandra Rivera · Google | tarjeta 3 | punch 112% | pop |
| 17.06–19.95 | Catorce tiempos, sin carta, frente a la chef. | **14** (conteo 1→14) **TIEMPOS** · "SIN CARTA" · "FRENTE A LA CHEF" | washi oscuro + 森下 marca de agua 6 % | flash entre frases | pops, ticks |
| 20.16–23.90 | Solo cuatro asientos por sesión. Sábado y domingo. | **4 ASIENTOS** · "POR SESIÓN" · "SÁB · DOM" | captura REAL `assets/recortes/captura-reserva-comensales-oscuro__maximo-4.jpg` | punch-in lento 100→110 %, scrim | tap UI, pop |
| 24.13–25.60 | ¿Y vale lo que cuesta? | "¿Y VALE LO QUE CUESTA?" | tinta | tensión: se encoge, glitch 3 fr al final | riser (pico en 25.7), glitch |
| 25.70–27.60 | «De verdad vale mucho la pena.» | "…de verdad **VALE MUCHO LA PENA**" gigante oro — Natalia Lopez · Google ★★★★★ (+ captura real `10-natalia-lopez-5estrellas.png` recortada al texto) | revelación | boom, flash crema 3 fr, ráfaga dorada, punch 115 % | boom, hyoshigi |
| 27.95–38.00 | Comenta omakase y te mando las fechas libres de este fin de semana. (luego música) | **COMENTA** · **OMAKASE** (gigante oro, subrayado animado) · "te mando las fechas libres por DM"; desde ~31.8 s: "$1,850 MXN p/p · bebidas sin alcohol ilimitadas incluidas" pequeño; desde ~34 s logo 森下 MORISHITA + "ENSENADA · B.C." + "SÁB · DOM · 4 ASIENTOS" | teléfono vectorial con `assets/recortes/captura-reserva-fechas-oscuro__calendario.jpg` | sube con ease, SIN cortes rápidos; "OMAKASE" se queda fijo ≥ 3 s | tap, pop, hyoshigi suave al logo |

Zonas seguras: todo texto importante en x 65–1015, y 270–1248. Debajo de 1248 solo fondo/decoración.
Tipos: Zen Antique Soft (display, kanji), Cormorant (citas itálicas), DM Mono (etiquetas). Acento único oro #d4af6a sobre negro. Flash crema #f5f0e8. Estilo premium: dopamínico ≠ ruidoso.
