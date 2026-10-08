Actúa como mi estratega de contenido y editor de video con HyperFrames. Vamos a crear reels con estilo dopamínico para Morishita Japanese Cuisine (https://www.morishitajapanesecuisine.com), un omakase de 14 tiempos con 4 lugares por servicio en Baja California. El objetivo es atraer leads calientes que reserven su omakase. Edición con música, efectos de sonido, transiciones, animaciones, voz en off con acento mexicano del norte y fotos y videos reales que correspondan a lo que dice el guion.

Sigue CLAUDE.md en todo momento. Trabaja paso a paso; en cada ⛔ PUNTO DE CONTROL detente y espera mi OK.

## PASO 1 · PREPARA TODO

1. Node ≥ 22, ffmpeg/ffprobe y `npx hyperframes doctor --json` (revisa el campo `ok`). Instala lo que falte; antes de instalar algo a nivel sistema, dime qué y por qué.
2. Skills: usa `/hyperframes:hyperframes` si el plugin está instalado; si no, `npx hyperframes skills update` y dime si debo reiniciar Claude Code.
3. `npx hyperframes auth status` y `npx hyperframes media-use resolve --doctor`: dime si ya tengo música, SFX y voz disponibles o si necesito iniciar sesión en HeyGen (no inicies sesión por mí). Revisa si hay `ELEVENLABS_API_KEY` en el entorno.
4. Crea las carpetas de CLAUDE.md. Tabla: herramienta · versión · estado · qué hiciste.

## PASO 2 · EXTRAE LA WEB Y JUNTA EL MATERIAL

1. Lee la web completa (experiencia, producto, chef, preguntas frecuentes, reservar) y guárdala textual en `fuente/web.md`. Descarga sus fotos a `assets/fotos/web/` y captúrala con `npx hyperframes capture` para tener el flujo de reserva como visual del CTA.
2. Saca del CSS colores (hex), tipografías y el logo 森下 / Morishita.
3. Instagram: no intentes scrapearlo (pide inicio de sesión). Yo te paso mis fotos y videos en `assets/` (de mi galería o de la descarga de información de Instagram). Si la carpeta está vacía, pídemelos y sigue con lo de la web mientras tanto.
4. Arma `fuente/hechos.md` como borrador con todo lo citable y señálame:
   - Lo que falta y sirve para vender: dirección o zona, horarios de servicio, número de WhatsApp, nombre del chef, bebidas.
   - El chef: la web dice "Chef Morishita" y las reseñas hablan de "la chef". ¿Cómo lo nombramos?
   - Respaldo de "Kobe" y "Wagyu A5" (certificado o factura).
   - El usuario de Instagram de la web (`morishitajapanesecuisine`) no coincide con mi perfil (`morishita.japanesecuisine`): confirma cuál es el correcto para corregir el link.
5. Cataloga cada asset en `assets/catalogo.md` mirándolo tú (qué se ve, encuadre, calidad, si sirve de gancho, vertical o recorte). Al final, dime qué momentos del omakase tienen buen material y cuáles faltan, con una lista de tomas para grabar el próximo fin de semana.
6. ⛔ PUNTO DE CONTROL: confirmo hechos, nombre del chef y material.

## PASO 3 · ESTILO Y MARCA

1. Si hay reels de referencia en `referencia/`, analízalos (fotogramas a 2 por segundo + cambios de plano, audio, loudness, SFX) y escribe `estilo.md` con valores medidos. Si no hay, escribe estilo.md con los valores dopamínicos de CLAUDE.md marcados [SUPOSICIÓN].
2. Crea `marca/frame.md` (formato HyperFrames, /hyperframes-creative) con colores y tipografías de la web.
3. Haz una prueba de 6 s (gancho + una transición + subtítulo kinético + SFX) con un asset real y dame un borrador `--quality draft` para calibrar el look y el ritmo antes de los guiones. ⛔ PUNTO DE CONTROL.

## PASO 4 · VOZ NORTEÑA

1. Escribe un texto de prueba de 15 s con el tono de la marca.
2. Dame 3 muestras para comparar: HeyGen (voces es-MX, filtra las masculinas y femeninas que suenen menos neutras), ElevenLabs si hay key (Voice Design con la descripción "hombre mexicano del norte, 35 años, voz cálida y segura, acento de Baja California, ritmo ágil") y, si quiero, mi propia nota de voz. Avísame antes de cualquier generación con costo.
3. ⛔ PUNTO DE CONTROL: elijo la voz → guárdala en `voz/voz-aprobada.md` (proveedor, ID, velocidad, estilo).

## PASO 5 · PRIMER LOTE (6 reels)

1. `calendario/lote-01.md` con 6 ideas: 2 de experiencia (qué vives en 2 horas), 2 de producto (wagyu A5 / Kobe, pescado de temporada, nigiri con oro), 1 de prueba social (reseña textual), 1 de ocasión (aniversario, cumpleaños, cita). Por idea: id · gancho · ángulo · CTA (reserva directa o palabra clave) · assets que usa · tomas que faltan.
2. ⛔ PUNTO DE CONTROL: apruebo el calendario.

## PASO 6 · GUIONES

Para cada idea, `guiones/lote-01/<id>.md`:
- 3 ganchos (0–3 s, ≤ 8 palabras) + recomendado y por qué.
- Tabla por línea: tiempo · voz · texto en pantalla · asset exacto (ruta del catálogo) · efecto/transición · SFX · fuente del dato (hechos.md) o PROPUESTA.
- Lazo abierto en el gancho y mini-gancho a la mitad.
- CTA con datos reales y, si es palabra clave, la respuesta automática del DM.
- Caption del post (primer renglón = gancho, CTA, 3–5 hashtags locales: Tijuana, Baja, omakase, wagyu).
- Checklist: cada asset coincide con su línea, sin escasez falsa, precio en MXN con "bebidas aparte" si se menciona.
⛔ PUNTO DE CONTROL: enséñame 2 guiones primero para calibrar, luego el resto.

## PASO 7 · PRODUCCIÓN (BORRADOR RÁPIDO → FINAL EN ALTA)

1. Genera la voz con la voz aprobada (texto con cifras escritas como se dicen), transcríbela con `--model small --language es` y compárala contra el guion.
2. Construye el primer reel con el router de HyperFrames pasándole todo el contexto: vertical 1080x1920, español, duración real de la voz, workflow general-video, flow companion, storyboard yes. Proyecto: `videos/<id>`. En BRIEF.md: assets con rutas exactas y la nota "Edición según estilo.md, marca según frame.md, contenido, voz y CTA según CLAUDE.md".
3. Busca en el catálogo de HyperFrames transiciones, flashes, glitch, contadores y texto kinético antes de programarlos a mano. Música con carve bajo la voz; SFX en transiciones y textos según estilo.md.
4. `npx hyperframes check` sin errores → **borrador rápido** `npx hyperframes render --quality draft --fps 30 --output renders/<id>-borrador-v01.mp4` → QA de CLAUDE.md → enséñamelo (y la URL de Studio por si quiero ajustar a mano).
5. ⛔ PUNTO DE CONTROL: pido cambios → aplicas → nuevo borrador (v02, v03…).
6. Solo cuando escriba **"render final"**: `npx hyperframes render --quality high --fps 30 --output renders/<id>-final.mp4` + QA.
7. Cuando apruebe el primero, congela la receta `reel-omakase` (/media-use → recipe freeze) y haz los otros 5 con flow automation, storyboard no, siempre borrador primero.

## PASO 8 · PUBLICAR Y MEDIR

1. Sugiere días y horas de publicación pensando en reservar el fin de semana (p. ej. martes a jueves para llenar sábado y domingo).
2. Antes de publicar: si el CTA es palabra clave, confirma que su respuesta automática está activa en `embudo/palabras-clave.md`; confirma que el link de reserva del perfil funciona.
3. Crea `metricas/registro.md`: id · fecha · vistas · retención 3 s · % visto completo · comentarios con palabra clave · DMs · reservas atribuidas.
4. Correcciones aprobadas → estilo.md, voz-aprobada.md o CLAUDE.md, según el tipo.

Empieza por el PASO 1.
