# r01-vale-cada-peso · guion v02

> Lote 01 · Ángulo: prueba social + objeción de precio · Duración: ~38 s (voz 31.6 s + cierre) · 1080x1920, 30 fps.
> **Cambio v01 → v02:** las reseñas que muestra la web **no son literales** (están editadas). La frase "una experiencia que vale cada peso" **no existe** en Google. v02 usa solo frases copiadas carácter por carácter de las 41 reseñas reales (`fuente/resenas-google.md` / `.json`). El nombre conserva "vale" porque la respuesta real es de Natalia Lopez: "de verdad vale mucho la pena".
> **Material:** tipografía, texturas generadas, capturas reales de Google y del flujo de reserva. Ninguna foto de comida, barra o chef: las de la web son IA. Sin Wagyu ni Kobe.

## 1. Ganchos (≤ 8 palabras)

| # | Gancho | Por qué |
|---|---|---|
| **A (recomendado)** | **"¿Vale $1,850 un omakase?"** | Ataca la objeción del lead caliente y abre un lazo que se cierra en 25.7 s con "de verdad vale mucho la pena" (literal). |
| B | "4,9 estrellas. 41 reseñas. 4 asientos." | Número concreto y real, con golpe; no abre lazo. |
| C | "Fue mi primera vez yendo a un omakase" (Valeria Colado, literal) | Identificación para el primerizo; menos urgencia. |

## 2. Guion (tiempos reales de `voz/r01/r01.words.json`)

| t (s) | Voz (Jorge es-MX +8 %) | Pantalla | Asset | Fuente |
|---|---|---|---|---|
| 0.00–2.95 | ¿Vale mil ochocientos cincuenta pesos un omakase? | ¿VALE **$1,850**? · MXN POR PERSONA | tinta y grano generados | hechos A2 |
| 3.00–4.70 | No te lo decimos nosotros. | NO LO DECIMOS / NOSOTROS | tinta | — |
| 4.77–8.45 | Cuatro punto nueve estrellas, en cuarenta y una reseñas de Google. | **4,9 ★★★★★** · 41 RESEÑAS DE GOOGLE | captura real `fuente/capturas/resenas/00-cabecera-4-9-41-resenas.png` (sin la dirección) | Google, 2026-10-08 |
| 8.55–11.40 | «Fue una experiencia espectacular de principio a fin.» | "…fue una experiencia espectacular de principio a fin" — Lucia Ojeda | tarjeta y captura real `01-lucia-ojeda` | reseña literal |
| 11.53–15.20 | «La chef fue atenta y amable, explicando cada pieza con detalle.» | (cita completa) — Lucia Ojeda | tarjeta | reseña literal |
| 15.39–16.90 | «Producto super fresco.» | "Producto super fresco !!" — Alejandra Rivera | tarjeta | reseña literal |
| 17.06–19.95 | Catorce tiempos, sin carta, frente a la chef. | **14 TIEMPOS** · SIN CARTA · FRENTE A LA CHEF | washi generado | A1, A11, A10 |
| 20.16–23.90 | Solo cuatro asientos por sesión. Sábado y domingo. | **4 ASIENTOS** · POR SESIÓN · SÁB · DOM | captura real `captura-reserva-comensales-oscuro__maximo-4` | A5, A7 |
| 24.13–25.60 | ¿Y vale lo que cuesta? | ¿Y VALE LO QUE CUESTA? (riser) | tinta | mini-gancho |
| 25.70–27.60 | «De verdad vale mucho la pena.» | "…de verdad **vale mucho la pena**" — Natalia Lopez | revelación con captura real `10-natalia-lopez` | reseña literal |
| 27.95–38.00 | Comenta omakase y te mando las fechas libres de este fin de semana. | **COMENTA OMAKASE** · calendario real en teléfono · $1,850 MXN p/p · bebidas sin alcohol ilimitadas incluidas · logo 森下 · ENSENADA · B.C. · SÁB · DOM · 4 ASIENTOS | captura real `captura-reserva-fechas-oscuro__calendario` | A2, A3, A5, A7, A17 |

- **Lazo abierto:** "¿Vale $1,850?" (0 s) → "de verdad vale mucho la pena" (25.7 s).
- **Mini-gancho:** "¿Y vale lo que cuesta?" (24.1 s), con riser.
- **Música:** `audio/musica/morishita-bed-B-120.wav` desde 20.3 s, de modo que el drop2 cae justo en la revelación (25.7 s).

## 3. CTA

- "Comenta OMAKASE y te mando las fechas libres de este fin de semana."
- La respuesta automática está en `embudo/palabras-clave.md`. **No se publica hasta activarla.**

## 4. Caption

> ¿Vale $1,850 un omakase?
> 4,9★ en 41 reseñas de Google. "De verdad vale mucho la pena", escribió Natalia.
> 14 tiempos sin carta, frente a la chef. Solo 4 asientos por sesión, sábado y domingo, en Ensenada.
> $1,850 MXN por persona, con bebidas sin alcohol ilimitadas incluidas.
> Comenta OMAKASE y te mando por DM las fechas libres de este fin de semana.
>
> #omakase #Ensenada #BajaCalifornia #omakaseensenada #cocinajaponesa

## 5. Checklist

- [x] Citas literales verificadas contra `fuente/resenas-google.json`, con el autor exacto.
- [x] Sin fotos IA, sin dirección, sin temporizador, sin Wagyu ni Kobe.
- [x] Precio en MXN por persona.
- [ ] Bebidas: la web en vivo dice "sin alcohol ilimitadas incluidas" y CLAUDE.md dice "bebidas aparte". **Confirmar (B4/D4).**
- [ ] 4,9★ / 41 reseñas: dato del 2026-10-08. Recapturar si cambia antes de publicar.
- [ ] Respuesta automática de OMAKASE activa.
- [ ] Recapturar el calendario el día de publicación.
