# r01-vale-cada-peso · guion v01

> Lote 01 · Ángulo: prueba social + objeción de precio · Duración objetivo: 36–40 s · 1080x1920, 30 fps.
> **Material 100 % real o permitido:** reseñas textuales de Google, datos de `fuente/hechos.md`, capturas reales del flujo de reserva, logo y tipografías de la marca, y texturas, partículas o tinta generadas (CLAUDE.md las permite). **No usa ninguna foto de comida, barra o chef** porque las de la web son IA (`assets/catalogo.md`).
> Sin Wagyu A5 ni Kobe.

## 1. Ganchos (0–3 s, ≤ 8 palabras)

| # | Fórmula | Gancho (voz y pantalla) | Pro | Contra |
|---|---|---|---|---|
| **A (recomendado)** | Pregunta-objeción + número | **"¿Vale $1,850 un omakase?"** (pantalla: "¿VALE $1,850?") | Filtra y atrae al lead caliente: quien se detiene ya está pensando en pagarlo. Abre un lazo que la reseña "vale cada peso" cierra casi al final. La cifra grande da golpe visual sin necesidad de foto. | Muestra el precio de entrada; quien busca algo barato se va (eso es bueno: no es lead). |
| B | Contraste | "Solo 4 personas por sesión. Esto escribieron." | Escasez real (A5) y curiosidad. | Sin una imagen real de la barra, el "4" pierde fuerza en el frame 0. |
| C | Número concreto | "5 estrellas. 4 asientos. 14 tiempos." | Tres cifras con golpe, muy "dopamínico". | No abre lazo: no hay pregunta que se pague al final. |

**Recomendado: A.** Es el único que convierte la objeción principal en el lazo abierto del reel. Y como no tenemos video real, el número es la imagen más fuerte que sí es verdad.

## 2. Guion línea por línea

Voz: propuesta en `voz/voz-aprobada.md` (pendiente de tu OK). Cifras escritas como se dicen. Los tiempos son objetivo: los finales salen de `voz/r01.words.json`.

| t (s) | Voz | Texto en pantalla (área útil y 270–1248) | Asset exacto | Efecto / transición | SFX | Fuente del dato |
|---|---|---|---|---|---|---|
| 0.0–3.0 | "¿Vale mil ochocientos cincuenta pesos un omakase?" | "¿VALE" (DM Mono) · **"$1,850"** gigante en oro, con conteo 0→1,850 en 0.6 s · "MXN POR PERSONA" | Fondo `#0a0908` con textura de tinta sumi y grano (generado) | Frame 0 con el texto ya en pantalla; golpe de escala 1.15→1.0 en 6 frames; partículas doradas al cerrar el conteo | Boom grave en el frame 0, ticks del conteo, hyoshigi al terminar | A2 · hechos (a) |
| 3.0–6.2 | "No te lo decimos nosotros. Mira lo que escribieron en Google." | "NO LO DECIMOS NOSOTROS" (palabra por palabra) → "★★★★★" que aparecen de una en una | Fondo de tinta | Flash crema de 2 frames al entrar; las estrellas hacen pop (escala 0→1.2→1) | Whoosh y 5 pops (uno por estrella) | Reseñas de 5★ · hechos (e) / `fuente/resenas-google.md` |
| 6.2–9.6 | «Una experiencia espectacular de principio a fin.» | Tarjeta de reseña: cita en Cormorant cursiva con **"espectacular"** en oro; autor "— Lucia Ojeda · Google" y ★★★★★ | Tarjeta tipográfica con el texto literal, o la captura real `fuente/capturas/resena-t1-dark.png` | La tarjeta entra con slide-up de 10 px y fade; punch-in lento de 100→106 %; cada palabra se ilumina al sonar | Campanita "rin" suave al entrar la tarjeta | Reseña 1 (Lucia Ojeda), textual |
| 9.6–13.6 | «Es toda una experiencia ver la preparación de cada platillo.» | Tarjeta 2 con **"ver la preparación"** en oro; "— Angelica Serrano · Google" (nombre exacto pendiente: hechos D7) | Tarjeta tipográfica o `fuente/capturas/resena-t2-dark.png` | Whip pan horizontal de 6 frames de la tarjeta 1 a la 2 | Whoosh | Reseña 2 (Angelica Serrano), textual |
| 13.6–17.0 | "Catorce tiempos, sin carta, frente a la chef Vero Morishita." | **"14"** (conteo 1→14) **"TIEMPOS"** · "SIN CARTA" · "FRENTE A LA CHEF" (un golpe por frase, ~1 s c/u) | Fondo de papel washi oscuro (generado) y kanji 森下 en marca de agua al 6 % | Corte con flash entre las 3 frases; cada número con punch-in de 112 % en 6 frames | Pop en cada frase, ticks del conteo | A1, A11, A10, A18 |
| 17.0–20.2 | "Solo cuatro asientos por sesión. Sábado y domingo." | **"4 ASIENTOS"** sobre la captura real; después "SÁB · DOM" | `assets/recortes/captura-reserva-comensales-oscuro__maximo-4.jpg` (pantalla real: "¿Cuántos asientos este día? Máximo 4 personas por servicio.") | Punch-in lento de la captura (100→110 %) con scrim negro abajo; el "4" con golpe | Tap de UI y pop | A5, A6, A7 · captura real |
| 20.2–22.0 | "¿Y la respuesta a la pregunta del principio?" | "¿LA RESPUESTA?" | Fondo de tinta | **Mini-gancho**: riser de 1.5 s, glitch corto de 3 frames al final y el texto se encoge (tensión) | Riser 1.5 s y glitch zap | — |
| 22.0–25.2 | «Una experiencia que vale cada peso.» | Tarjeta 3: "…una experiencia que **VALE CADA PESO**" (VALE CADA PESO gigante en oro) · "— Cyn RM · Google" ★★★★★ | Tarjeta tipográfica o `fuente/capturas/resena-t3-dark.png` | **Revelación**: boom, flash crema de 3 frames, ráfaga de partículas doradas, punch-in de 115 % | Boom e impacto, hyoshigi | Reseña 3 (Cyn RM), textual (fragmento con "…") |
| 25.2–27.8 | "Bebidas sin alcohol ilimitadas, incluidas." | "$1,850 MXN P/P" · "BEBIDAS SIN ALCOHOL ILIMITADAS · INCLUIDAS" | `assets/recortes/captura-reserva-resumen-oscuro__tabla-datos.jpg` (tabla real: Sáb·Dom / 4 asientos / 14 / $1,850 MXN p/p / 50 %) | Pan vertical lento sobre la tabla real; el texto entra en 2 golpes | Pop ×2 | A2, A3 (B4: confirmar) |
| 27.8–32.5 | "Comenta OMAKASE y te mando las fechas libres de este fin de semana." | **"COMENTA"** · **"OMAKASE"** (gigante, oro, subrayado animado) · "te mando las fechas libres por DM" | `assets/recortes/captura-reserva-fechas-oscuro__calendario.jpg` (calendario real de octubre 2026) dentro de un marco de teléfono (vector) | El teléfono sube con ease; "OMAKASE" con golpe y brillo; **sin cortes rápidos** | Tap de UI y pop | CTA de palabra clave (CLAUDE.md) · A25 |
| 32.5–36.5 | (silencio, la música resuelve) | "OMAKASE" se queda · logo **森下 MORISHITA** · "ENSENADA · BAJA CALIFORNIA" · "SÁB · DOM · 4 ASIENTOS" | `marca/logo/logo-vertical-fondo-oscuro.svg` | CTA fijo ≥ 3 s (de 27.8 a 36.5 son 8.7 s); el sello entra con rebote (`--ease-sello`) | Nota final de la música y hyoshigi suave | A17, A5, A7 |

- **Lazo abierto:** la pregunta "¿Vale $1,850?" (0 s) se paga con "vale cada peso" (22 s).
- **Mini-gancho a la mitad:** "¿Y la respuesta a la pregunta del principio?" (20 s), con riser.
- **Interrupción de patrón cada 2–3 s:** golpe y conteo → estrellas → tarjeta → whip → números → captura real → glitch → revelación → tabla → teléfono.
- **Respiro:** tarjetas de reseña de 3–4 s con punch-in lento (no cortes encima de la cita).

## 3. CTA y respuesta automática del DM

- **CTA:** "Comenta OMAKASE y te mando las fechas libres de este fin de semana."
- **Palabra clave:** `OMAKASE`, registrada en `embudo/palabras-clave.md` con su respuesta automática. **El reel no se publica hasta que esa respuesta esté activa.**
- **Escasez:** solo la real ("4 asientos por sesión", "sábado y domingo"). Nada de "quedan X" sin tu confirmación del día.

## 4. Caption

> ¿Vale $1,850 un omakase?
> No lo decimos nosotros: lo dicen nuestras reseñas de 5★ en Google.
> 14 tiempos sin carta, frente a la Chef Vero Morishita. Solo 4 asientos por sesión, sábado y domingo, en Ensenada.
> $1,850 MXN por persona, con bebidas sin alcohol ilimitadas incluidas.
> Comenta OMAKASE y te mando por DM las fechas libres de este fin de semana.
>
> #omakase #Ensenada #BajaCalifornia #omakaseensenada #cocinajaponesa

## 5. Checklist

- [x] Ninguna imagen de comida, barra o chef (todas las de la web son IA). Solo capturas reales, tipografía y texturas.
- [x] Reseñas textuales, sin parafrasear. El fragmento de Cyn RM va con "…".
- [ ] Autores con el nombre **exacto como aparece en Google** (pendiente de `fuente/resenas-google.md`; hechos D7).
- [x] Precio en MXN y por persona.
- [ ] Bebidas: CLAUDE.md dice "bebidas aparte" y la web en vivo dice "bebidas sin alcohol ilimitadas incluidas". Este guion usa lo de la web; **confírmalo (B4/D4)** y, si se vende alcohol, decidir si se agrega "alcohol aparte".
- [x] Sin escasez falsa: el temporizador de la web no aparece (B15).
- [x] Sin Wagyu ni Kobe.
- [ ] "Chef Vero Morishita": es el nombre de la web en vivo; confírmalo (D6).
- [ ] Respuesta automática de OMAKASE activa antes de publicar.
- [ ] Recapturar el calendario el día que se publique.
