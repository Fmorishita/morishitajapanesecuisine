# Reseñas de Google: Morishita Japanese Cuisine (Ensenada)

Extraídas el **2026-10-08** del panel público de reseñas de Google (búsqueda `Morishita Japanese Cuisine Ensenada`, `hl=es`), sin iniciar sesión, con Playwright (Chromium headless, locale es-MX). Ficha: *Morishita Japanese Cuisine · Del Parque 136, Bahia, 22880 Ensenada, B.C., México* (place id `0x80d88dd1e00b30ed:0x2ae0f6e9db38e348`).

Datos crudos (JSON con autor, estrellas, fecha, etiquetas, texto completo y atributos): `fuente/resenas-google.json`.

## Lo accionable primero

- **Calificación global: 4,9 ★ · 41 reseñas** (captura: `capturas/resenas/00-cabecera-4-9-41-resenas.png`). Reparto de las 41: 38 de 5★, 1 de 4★, 1 de 3★, 1 de 2★. 36 traen texto.
- **Ninguna reseña menciona Wagyu ni Kobe** (ni "A5", "carne" o "res"). No hay frases que separar por esa restricción.
- **Las 3 reseñas de la web NO son textuales**: existen en Google, pero la web las editó (corrigió ortografía, recortó y reescribió). **Ninguno de los 5 fragmentos de `hechos.md` §e es literal**; uno ("una experiencia que vale cada peso") no aparece en ninguna reseña de Google. Detalle abajo. Propuesta para `hechos.md` §e: reemplazar por los textos de esta página.
- Nombre exacto: **"Angelica Serrano Silva"** (no "Angelica Serrano."). **"Cyn RM" sí es Local Guide.** **"Lucia Ojeda"** sin acento. Google **no muestra ciudad** de ningún autor: "Tijuana", "San Diego" y "Mexicali" de la web no salen de Google; no usarlas.
- **No usar** la reseña de **"Patricia Morishit"** ("Gracias hermana…"): es familiar de la chef; citarla como reseña de cliente sería engañoso.
- Las fotos de avatar son caras reales de clientes: en el reel, **difuminar el avatar** (o recortar a nombre + estrellas + texto) salvo permiso. Lucia Ojeda tiene avatar de letra "L" (sin cara).

## Intentos (bitácora)

| # | Ruta | Resultado |
|---|---|---|
| a | Google Maps `maps/search/Morishita+Japanese+Cuisine+Ensenada` | Abre la ficha (4,9 ★, dirección, teléfono +52 646 245 4294, "Reservar una mesa: instagram.com"), pero en **"vista limitada de Google Maps"** sin sesión: no hay pestaña Opiniones ni número de reseñas. Bloqueado para reseñas. |
| b | `google.com/search?q=Morishita+Japanese+Cuisine+Ensenada&hl=es` → enlace "41 reseñas de Google" | **Funcionó.** Diálogo de reseñas con filtros y orden. Orden "Más relevantes": scroll hasta cargar las **41/41** (todas, coincide con el total), clic en cada "Más", extracción del DOM. |
| b2 | Mismo diálogo, orden "Más recientes" | El chip no respondió al clic en headless (2 intentos, elemento "no estable"). No hace falta: ya están las 41; las fechas relativas permiten ordenar (abajo). |
| c | WebSearch/WebFetch | No necesario. Nota: en la búsqueda aparecen Facebook (5,0, 1 reseña) y otros directorios; no son reseñas de Google y no se usan. |

## Verificación de las 3 reseñas que cita la web (hechos.md §e, D7)

| Web (en vivo) | Google (exacto) | ¿Existe? | ¿Texto idéntico? |
|---|---|---|---|
| "Lucia Ojeda · Tijuana" | **Lucia Ojeda** · 3 reseñas · 11 fotos · 5★ · Hace 6 meses | Sí | **No.** La web condensa y reescribe ("La chef explica cada pieza…", "cada tiempo perfectamente balanceado"). Google: "La chef fue atenta y amable, explicando cada pieza con detalle", "cada pieza tenía un sabor  perfectamente balanceado". |
| "Angelica Serrano. · San Diego" | **Angelica Serrano Silva** · 1 reseña · 9 fotos · 5★ · Hace 5 meses | Sí | **No.** La web corrige y quita frases ("Me encantó todo — ingredientes frescos…", "volvería"). Google: "Me encanto todo, muy buen sabor, ingredientes fescos…", "definitivamente volvere." |
| "Cyn RM · Mexicali" | **Cyn RM** · **Local Guide** · 6 reseñas · 35 fotos · 5★ · Hace 7 meses | Sí | **No.** La web reescribe ("Sin duda de la mejor cocina japonesa en Baja…", "una experiencia que vale cada peso"). Google: "sin duda de la mejor cocina japonesa en la Baja"; **"vale cada peso" no existe**. |

Fragmentos de `hechos.md` §e contra Google:

| Fragmento en hechos.md | ¿Literal en Google? | Forma literal que sí se puede usar |
|---|---|---|
| "Una experiencia espectacular de principio a fin." (Lucia Ojeda) | No | "fue una experiencia espectacular de principio a fin" |
| "La chef explica cada pieza con detalle" (Lucia Ojeda) | No | "La chef fue atenta y amable, explicando cada pieza con detalle." |
| "Me encantó todo" (Angelica Serrano) | No (Google: sin acento) | "Me encanto todo" (Angelica Serrano Silva) |
| "100% recomendado, definitivamente volvería." (Angelica Serrano) | No | "100% recomendado, definitivamente volvere." |
| "una experiencia que vale cada peso" (Cyn RM) | **No existe** | — (no usar) |

Las capturas antiguas `fuente/capturas/resena-t1|t2|t3-dark.png` son de la **web**, con el texto editado: no sirven como prueba de Google. Usar las de `capturas/resenas/`.

## Frases para reels (literales, ≤ 15 palabras, solo reseñas de 5★)

Cada frase es una **subcadena exacta** del texto en Google (verificado por script), con su ortografía original. Si se recorta, se cita con "…" y siempre con el autor tal como aparece. Excluida Patricia Morishit.

**Experiencia**
- "fue una experiencia espectacular de principio a fin" — Lucia Ojeda
- "Cada bocado es una experiencia inolvidable." — KAREN GARCIA
- "Obra de arte culinaria" — Danae Barreto
- "Es un viaje culinario atraves de la cultura japonesa y su historia" — Huerta Abraham
- "True omakase con especial atención a detalle." — Jesus Ruben Villavicencio Ruiz
- "El servicio de omakasen hace que la experiencia sea intima, especial y con mucho merito." — Esmeralda Vargas S.
- "vivir la experiencia de no saber que es lo que vas a degustar" — Annet Alarcón
- "aunque no sabes que vendrá o cuál es el siguiente plato" — Aries Ferreyra
- "Una experiencia de 10 ✨" — Annet Alarcón
- "Que espectáculo" — Cyn RM

**Chef**
- "La chef fue atenta y amable, explicando cada pieza con detalle." — Lucia Ojeda
- "la chef hace un trabajo espectacular, cuenta la historia de sus ingredientes" — KAREN GARCIA
- "te hace sentir como si estuvieras en Japón." — KAREN GARCIA
- "la interacción comensal-chef no en cualquier lugar la encuentras" — YARA CORREA JAUREGUI
- "preparados por una chef veterana qué transmite el amor de su cultura." — Danae Barreto
- "los tiempos son al ritmo de la chef" — Annet Alarcón
- "te explican el platillo y el por que de los ingredientes" — Francisco Cobo
- "la chef es súper atenta y amable" — Natalia Lopez
- "Gracias totales a la chef 🙏🏻" — Annet Alarcón

**Producto / frescura**
- "Producto super fresco !!" — Alejandra Rivera
- "Frescura y simplicidad en su máxima expresión" — Rosanna Saad
- "Los ingredientes estaban bastante frescos" — Lucia Ojeda
- "Toda la comida es fresca y con ingredientes de calidad" — Natalia Lopez
- "Alimentos frescos y de alta gama" — Danae Barreto
- "los sabores y la frescura 1000/10🤌🏼" — Annet Alarcón
- "Los sabores intensos y muy frescos los ingredientes" — jafet pedrotte ortiz
- "muy fresco el marisco" — Armida Arangure
- "Platillos con presentación impecable" — Esmeralda Vargas S.
- "creatividad de sabores y servicio muy cálido." — Rosanna Saad

**Valor / calidad (no hay reseña 5★ que hable de precio en pesos)**
- "de verdad vale mucho la pena" — Natalia Lopez
- "Definitivamente vale mucho la pena probar una experiencia “Omakase”" — KAREN GARCIA
- "servicio premium desde la reservacion hasta la despedida." — Danae Barreto
- "Un lugar perfecto para quienes buscan un omakase auténtico, de calidad y lleno de detalles." — Lucia Ojeda
- "El mejor Omakase de la baja" — Maximiliano Gonzalez
- "sin duda de la mejor cocina japonesa en la Baja" — Cyn RM
- "LA MEJOR COMIDA EN EL OMAKASE" — Anuar Dajlala Flores
- "No te vas a arrepentir." — Mar

**Ocasión / primera vez / grupo**
- "reservamos en Morishita para celebrar el día del amor" — Cyn RM
- "dejarse consentir y sorprender por el menú sorpresa de la chef" — Cyn RM
- "Fue mi primera vez yendo a un omakase" — Valeria Colado
- "honestamente es la mejor cosa que he probado" — Valeria Colado
- "Súper recomendable si eres de vivir una experiencia única y nueva." — essi block
- "parece que estás comiendo en la casa de un familiar." — jafet pedrotte ortiz
- "Tiene un ambiente de hogar" — Pablo Farias

**Volver / recomendar**
- "Sin duda un lugar al que volveré pronto" — Annet Alarcón
- "Nos fuimos con muchas ganas de volver." — Miguel Angel Sepulveda
- "quedamos encantados y esperamos volver pronto" — Carla Perea
- "Definitivamente algo que volvería a repetir." — Valeria Colado
- "definitivo volvería a ir" — YARA CORREA JAUREGUI
- "sin duda tendremos que volver" — Cyn RM
- "100% recomendado, definitivamente volvere." — Angelica Serrano Silva
- "Es una experiencia 100% recomendable." — Carla Perea

**Wagyu / Kobe (no se usan en este lote):** ninguna reseña los menciona. Sin frases.

**Ojo con ortografía visible:** varias frases traen erratas del cliente ("atraves", "reservacion", "volvere", "autentica", "intima", "merito", "qué transmite"). Por regla se citan tal cual; si molesta en pantalla, elegir otra frase en vez de corregirla.

## Alertas para el dueño (no usar sin confirmar)

- **"12 tiempos"** (omar castro, hace 8 meses) contradice los 14 tiempos de hoy (en Facebook, dic 2025, también se anunció "omakase de 12 tiempos"). No usar ese fragmento.
- Nombre de la chef en reseñas: "Verónica, la chef" (Miguel Angel Sepulveda), "la Chef Verónica" (Jennhy Torres), "la chef morishita" (Huerta Abraham), "la chef Morishita" (Ricardo Rodriguez); "la chef y su hijo" (Cyn RM). Relevante para D6.
- "el maridaje de las bebidas" (Huerta Abraham): posible alcohol (D4). No usar sin la leyenda del abogado.
- "como es al aire libre ponen calentón de patio", "puedes poner la música que gustes" (Annet Alarcón): datos no confirmados en hechos.md.
- "el postre estuvo riquísimo" (Valeria Colado): toca D5 (postre).
- "son atentos en preguntar si alguna persona del grupo reservado es alérgico" (atributo de KAREN GARCIA): respalda "restricciones alimentarias se anotan al reservar".
- Reseñas negativas a atender: **Pablito Pro (3★)**: "vi que tiraban todo el arroz sobrante directo a la banqueta" (tema operativo/higiene, conviene responder); **Elihu Rivera (2★, Local Guide)**: "De japonés solo el nombre."… (Comida/Servicio/Ambiente 1/5, espera +1 hora). Ninguna tiene respuesta visible del propietario.
- Etiquetas de precio que eligen los clientes varían ("Más de 1000 $" la mayoría; KAREN GARCIA "100-200 $", Miguel Angel Sepulveda "1-100 $"): no son dato citable.
- Ficha de Google: sin sesión muestra "¿Eres el propietario de esta empresa?" y "Añadir sitio web" (el botón de reserva apunta a instagram.com). Posible ficha sin reclamar o sin sitio web: conviene agregar `morishitajapanesecuisine.com` (y su `?reservar=1`) como sitio y enlace de reserva, y responder reseñas.
- "Fatima Contreras" marcó "Recogí el pedido" y "Venta de boilers y minisplits Mirage" es una cuenta de negocio: sin texto, irrelevantes.

## Tabla de las 41 reseñas (orden "Más relevantes" de Google)

| # | Autor (exacto) | Perfil | ★ | Fecha | Etiquetas de Google | Menciona | Captura |
|---|---|---|---|---|---|---|---|
| 1 | Angelica Serrano Silva | 1 reseña · 9 fotos | 5 | Hace 5 meses | Comí allí  \|  Comida | chef, producto/frescura, experiencia, volveria | `capturas/resenas/02-angelica-serrano-silva-5estrellas.png` |
| 2 | jafet pedrotte ortiz | 4 reseñas · 4 fotos | 5 | Hace 3 meses | Comí allí  \|  Cena  \|  Más de 1000 $ | producto/frescura, experiencia, ocasion | `capturas/resenas/20-jafet-pedrotte-ortiz-5estrellas.png` |
| 3 | Jesus Ruben Villavicencio Ruiz | 1 reseña · 3 fotos | 5 | Hace 8 meses | Cena | experiencia | `capturas/resenas/14-jesus-ruben-villavicencio-ruiz-5estrellas.png` |
| 4 | Natalia Lopez | 3 reseñas · 9 fotos | 5 | Hace 8 meses | Comí allí | chef, producto/frescura, valor/precio | `capturas/resenas/10-natalia-lopez-5estrellas.png` |
| 5 | Lucia Ojeda | 3 reseñas · 11 fotos | 5 | Hace 6 meses | Comí allí | chef, producto/frescura, experiencia | `capturas/resenas/01-lucia-ojeda-5estrellas.png` |
| 6 | Annet Alarcón | Local Guide · 11 reseñas · 19 fotos | 5 | Hace 8 meses | Comí allí  \|  Cena  \|  Más de 1000 $ | chef, producto/frescura, experiencia, volveria | `capturas/resenas/04-annet-alarcon-5estrellas.png` |
| 7 | Miguel Angel Sepulveda | 3 reseñas · 7 fotos | 5 | Hace 9 meses | Comí allí  \|  1-100 $ | chef, experiencia, volveria | `capturas/resenas/15-miguel-angel-sepulveda-5estrellas.png` |
| 8 | Carla Perea | Local Guide · 13 reseñas · 5 fotos | 5 | Hace 6 meses | Comí allí | producto/frescura, experiencia, volveria | `capturas/resenas/16-carla-perea-5estrellas.png` |
| 9 | Cyn RM | Local Guide · 6 reseñas · 35 fotos | 5 | Hace 7 meses | Comida  \|  Más de 1000 $ | chef, experiencia, valor/precio, ocasion, volveria | `capturas/resenas/03-cyn-rm-5estrellas.png` |
| 10 | YARA CORREA JAUREGUI | 1 reseña · 3 fotos | 5 | Hace 8 meses | Más de 1000 $ | chef, volveria | `capturas/resenas/09-yara-correa-jauregui-5estrellas.png` |
| 11 | omar castro | 7 reseñas · 7 fotos | 5 | Hace 8 meses | Comí allí  \|  Más de 1000 $ | chef, producto/frescura, experiencia, volveria |  |
| 12 | Mar | Local Guide · 35 reseñas · 19 fotos | 5 | Hace 8 meses | Comí allí  \|  Más de 1000 $ | producto/frescura, valor/precio | `capturas/resenas/17-mar-5estrellas.png` |
| 13 | KAREN GARCIA | 2 reseñas · 8 fotos | 5 | Hace 9 meses | Comí allí  \|  100-200 $ | chef, producto/frescura, experiencia, valor/precio | `capturas/resenas/05-karen-garcia-5estrellas.png` |
| 14 | Alejandra Rivera | Local Guide · 7 reseñas · 21 fotos | 5 | Hace 8 meses | Comí allí | producto/frescura, experiencia | `capturas/resenas/12-alejandra-rivera-5estrellas.png` |
| 15 | Danae Barreto | 2 reseñas · 3 fotos | 5 | Hace 9 meses | Comí allí  \|  Más de 1000 $ | chef, producto/frescura, valor/precio, ocasion, volveria | `capturas/resenas/06-danae-barreto-5estrellas.png` |
| 16 | Valeria Colado | 1 reseña · 2 fotos | 5 | Hace 8 meses | — | experiencia, valor/precio, ocasion, volveria | `capturas/resenas/08-valeria-colado-5estrellas.png` |
| 17 | Zewen Lin Wu | 2 reseñas · 9 fotos | 5 | Hace 7 meses | Cena  \|  Más de 1000 $ | — |  |
| 18 | Anuar Dajlala Flores | 1 reseña · 2 fotos | 5 | Hace 8 meses | Comí allí  \|  Cena | experiencia, valor/precio | `capturas/resenas/19-anuar-dajlala-flores-5estrellas.png` |
| 19 | Huerta Abraham | Local Guide · 58 reseñas · 14 fotos | 5 | Hace un mes | Comí allí  \|  Cena  \|  Más de 1000 $ | chef, experiencia | `capturas/resenas/18-huerta-abraham-5estrellas.png` |
| 20 | Rosanna Saad | 6 reseñas | 5 | Hace 4 meses | Comida  \|  Más de 1000 $ | producto/frescura, experiencia | `capturas/resenas/11-rosanna-saad-5estrellas.png` |
| 21 | Francisco Cobo | 11 reseñas · 12 fotos | 5 | Hace 3 meses | Comí allí  \|  Comida | producto/frescura, experiencia |  |
| 22 | essi block | 1 reseña | 5 | Hace 8 meses | Comí allí | chef, producto/frescura, experiencia, volveria |  |
| 23 | Aries Ferreyra | 1 reseña | 5 | Hace 5 meses | Más de 1000 $ | producto/frescura | `capturas/resenas/21-aries-ferreyra-5estrellas.png` |
| 24 | Jennhy Torres | Local Guide · 34 reseñas · 154 fotos | 5 | Hace 5 meses | Comida  \|  Más de 1000 $ | chef, experiencia, volveria |  |
| 25 | Pablito Pro | 1 reseña | 3 | Hace 4 meses | — | — |  |
| 26 | Carem Rios | 1 reseña | 5 | Hace 8 meses | — | chef, experiencia |  |
| 27 | Elihu Rivera | Local Guide · 71 reseñas · 57 fotos | 2 | Hace 8 meses | Comí allí  \|  Otro  \|  Más de 1000 $ | producto/frescura, experiencia, valor/precio |  |
| 28 | Coolbox | 1 reseña | 5 | Hace 9 meses | Cena  \|  Más de 1000 $ | experiencia |  |
| 29 | Esmeralda Vargas S. | Local Guide · 21 reseñas · 6 fotos | 5 | Hace 8 meses | Más de 1000 $ | chef, experiencia, valor/precio, volveria | `capturas/resenas/07-esmeralda-vargas-s-5estrellas.png` |
| 30 | Ricardo Rodriguez | 1 reseña | 5 | Hace 8 meses | — | chef, experiencia |  |
| 31 | Maximiliano Gonzalez | 3 reseñas · 3 fotos | 5 | Hace 8 meses | — | experiencia, valor/precio | `capturas/resenas/13-maximiliano-gonzalez-5estrellas.png` |
| 32 | Patricia Morishit | 4 reseñas | 5 | Hace 9 meses | — | — |  |
| 33 | Armida Arangure | Local Guide · 3 reseñas | 5 | Hace 2 semanas | Comí allí  \|  Más de 1000 $ | producto/frescura | `capturas/resenas/22-armida-arangure-5estrellas.png` |
| 34 | Pablo Farias | 1 reseña | 5 | Hace 2 semanas | — | — |  |
| 35 | Luiana Hernandez | Local Guide · 14 reseñas · 1 foto | 5 | Hace 4 meses | — | producto/frescura, volveria |  |
| 36 | ana rubio | 1 reseña | 5 | Hace 7 meses | Cena  \|  Más de 1000 $ | sin texto |  |
| 37 | Martha Aguilar | 1 reseña | 5 | Hace 8 meses | — | sin texto |  |
| 38 | Fatima Contreras |  | 5 | Hace un mes | Recogí el pedido  \|  Más de 1000 $ | sin texto |  |
| 39 | Joel Martínez | Local Guide · 1 reseña | 4 | Hace un mes | — | sin texto |  |
| 40 | Manuel limon |  | 5 | Hace 8 meses | — | sin texto |  |
| 41 | Venta de boilers y minisplits Mirage | 8 reseñas · 6 fotos | 5 | Hace 8 meses | — | sin texto |  |

Más recientes: Armida Arangure y Pablo Farias (hace 2 semanas); Huerta Abraham, Fatima Contreras y Joel Martínez (hace un mes); jafet pedrotte ortiz y Francisco Cobo (hace 3 meses).

## Textos completos (verbatim, sin corregir)

Texto del cliente tal cual (saltos de línea conservados como líneas de cita; dobles espacios originales conservados). Debajo, los atributos estructurados que Google muestra en la tarjeta.

### 1. Angelica Serrano Silva · 5★ · Hace 5 meses
Perfil: 1 reseña · 9 fotos · Etiquetas: Comí allí  |  Comida

> Me encanto todo, muy buen sabor, ingredientes fescos y todo muy limpio. El ambiente es muy agradable y la chef muy amigable. Es toda una experiencia ver la preoaracion de cada uno de los platillos y una sorpresa de sabores con cada uno.
> 100% recomendado, definitivamente volvere.

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Tiempo de espera: Sin espera

### 2. jafet pedrotte ortiz · 5★ · Hace 3 meses
Perfil: 4 reseñas · 4 fotos · Etiquetas: Comí allí  |  Cena  |  Más de 1000 $

> Exelente ambiente....... Los sabores intensos y muy frescos los ingredientes una experiencia facinante..... El trato exelente parece que estás comiendo en la casa de un familiar. 10/10

Atributos: Tiempo de espera: Sin espera

### 3. Jesus Ruben Villavicencio Ruiz · 5★ · Hace 8 meses
Perfil: 1 reseña · 3 fotos · Etiquetas: Cena

> Buenisima experiencia. True omakase con especial atención a detalle. El lugar está impecable y los platillos exquisitos.

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Reservas: Reserva obligatoria · Nivel de ruido: Bajo, pero se puede conversar fácilmente

### 4. Natalia Lopez · 5★ · Hace 8 meses
Perfil: 3 reseñas · 9 fotos · Etiquetas: Comí allí

> El lugar está delicioso! Toda la comida es fresca y con ingredientes de calidad; la chef es súper atenta y amable, de verdad vale mucho la pena

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Tamaño del grupo: 3-4 personas · Tiempo de espera: Sin espera

### 5. Lucia Ojeda · 5★ · Hace 6 meses
Perfil: 3 reseñas · 11 fotos · Etiquetas: Comí allí

> Tuvimos la oportunidad de disfrutar un omakase y fue una experiencia espectacular de principio a fin. En lo personal todos los platillos me gustaron mucho.
> La chef fue atenta y amable, explicando cada pieza con detalle. Los ingredientes estaban bastante frescos y cada pieza tenía un sabor  perfectamente balanceado.
> El ambiente del lugar es tranquilo.
> Un lugar perfecto para quienes buscan un omakase auténtico, de calidad y lleno de detalles.

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 4/5

### 6. Annet Alarcón · 5★ · Hace 8 meses
Perfil: Local Guide · 11 reseñas · 19 fotos · Etiquetas: Comí allí  |  Cena  |  Más de 1000 $

> Sin duda un lugar al que volveré pronto, excelente servicio desde la bienvenida, los tiempos son al ritmo de la chef, vivir la experiencia de no saber que es lo que vas a degustar definitivamente no es para cualquiera, los sabores y la frescura 1000/10🤌🏼
>
> Ambiente súper agradable, ya que son servicios personalizados, puedes poner la música que gustes y como es al aire libre ponen calentón de patio para nosotros los friolentos.
>
> Una experiencia de 10 ✨
> Gracias totales a la chef 🙏🏻

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Tiempo de espera: Sin espera

### 7. Miguel Angel Sepulveda · 5★ · Hace 9 meses
Perfil: 3 reseñas · 7 fotos · Etiquetas: Comí allí  |  1-100 $

> ¡Excelente experiencia! La bienvenida fue inmediata y muy amable, y Verónica, la chef, nos sorprendió con un menú increíble. Nos fuimos con muchas ganas de volver.

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Tamaño del grupo: 2 personas

### 8. Carla Perea · 5★ · Hace 6 meses
Perfil: Local Guide · 13 reseñas · 5 fotos · Etiquetas: Comí allí

> Es una experiencia 100% recomendable. La calidad de los productos, la presentación,  los sabores, todo es excelente 👌   quedamos encantados y esperamos volver pronto

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5

### 9. Cyn RM · 5★ · Hace 7 meses
Perfil: Local Guide · 6 reseñas · 35 fotos · Etiquetas: Comida  |  Más de 1000 $

> Que espectáculo 🤩 disfrutamos muchísimo nuestra experiencia omakase que reservamos en Morishita para celebrar el día del amor 🥰
> La comida deliciosa 🤤 sin duda de la mejor cocina japonesa en la Baja 😮‍💨 y la atención de la chef y su hijo lo máximo, súper amables y serviciales.. sin duda tendremos que volver y llevar a amigos y familia a dejarse consentir y sorprender por el menú sorpresa de la chef 🤗

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Tamaño del grupo: 2 personas y 3-4 personas

### 10. YARA CORREA JAUREGUI · 5★ · Hace 8 meses
Perfil: 1 reseña · 3 fotos · Etiquetas: Más de 1000 $

> Un lugar súper agradable, la comida buenisima y el servicio excelente 🙌 son personas muy amables y agradables, te explica cada cosa y la interacción comensal-chef no en cualquier lugar la encuentras definitivo volvería a ir 🤌🤌

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Tamaño del grupo: 3-4 personas · Tiempo de espera: Sin espera · Tipo de asiento: Asientos en la barra

### 11. omar castro · 5★ · Hace 8 meses
Perfil: 7 reseñas · 7 fotos · Etiquetas: Comí allí  |  Más de 1000 $

> Es una experiencia muy buena, 12 tiempos con platillos bien servidos y de sabor rico,  muy tradicional estilo japonés, la chef muy amable y explica sobre el producto y técnicas, recomendado

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Tamaño del grupo: 3-4 personas · Tiempo de espera: Sin espera

### 12. Mar · 5★ · Hace 8 meses
Perfil: Local Guide · 35 reseñas · 19 fotos · Etiquetas: Comí allí  |  Más de 1000 $

> Top 🔝
> Super recomiendo, si quieres autentica comida japonesa, calidad en los alimentos y en el servicio este es tu lugar. No te vas a arrepentir.

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Tiempo de espera: Sin espera

### 13. KAREN GARCIA · 5★ · Hace 9 meses
Perfil: 2 reseñas · 8 fotos · Etiquetas: Comí allí  |  100-200 $

> Cada bocado es una experiencia inolvidable. Definitivamente vale mucho la pena probar una experiencia “Omakase”, la chef hace un trabajo espectacular, cuenta la historia de sus ingredientes y te hace sentir como si estuvieras en Japón.
>
> Cada tiempo está delicioso, sin duda lo recomiendo.

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Tamaño del grupo: 5-8 personas · Restricciones alimentarias: Antes de llegar la fecha de tu reservación, son atentos en preguntar si alguna persona del grupo reservado es alérgico a algún alimento.

### 14. Alejandra Rivera · 5★ · Hace 8 meses
Perfil: Local Guide · 7 reseñas · 21 fotos · Etiquetas: Comí allí

> Toda la experiencia estuvo excelente !! Producto super fresco !! Todo delicioso!

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5

### 15. Danae Barreto · 5★ · Hace 9 meses
Perfil: 2 reseñas · 3 fotos · Etiquetas: Comí allí  |  Más de 1000 $

> Obra de arte culinaria 👌🏽 servicio premium desde la reservacion hasta la despedida. Alimentos frescos y de alta gama preparados por una chef veterana qué transmite el amor de su cultura. Recomendado 100%

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Tamaño del grupo: 3-4 personas

### 16. Valeria Colado · 5★ · Hace 8 meses
Perfil: 1 reseña · 2 fotos · Etiquetas: —

> Fue mi primera vez yendo a un omakase y honestamente es la mejor cosa que he probado. La experiencia me encantó de principio a fin, todos los platillos estaban increíbles y el postre estuvo riquísimo. Definitivamente algo que volvería a repetir.

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5

### 17. Zewen Lin Wu · 5★ · Hace 7 meses
Perfil: 2 reseñas · 9 fotos · Etiquetas: Cena  |  Más de 1000 $

> Muy buena comida y servicio.

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Tamaño del grupo: 3-4 personas · Tiempo de espera: Menos de 10 min

### 18. Anuar Dajlala Flores · 5★ · Hace 8 meses
Perfil: 1 reseña · 2 fotos · Etiquetas: Comí allí  |  Cena

> LA MEJOR COMIDA EN EL OMAKASE, excelente servicio al cliente, se nota que les importa la experiencia.

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5

### 19. Huerta Abraham · 5★ · Hace un mes
Perfil: Local Guide · 58 reseñas · 14 fotos · Etiquetas: Comí allí  |  Cena  |  Más de 1000 $

> Es un viaje culinario atraves de la cultura japonesa y su historia, llevados de la mano de la agradable chef morishita, ve con espacio suficiente en el estomago, porque aunque es degustacion, las porciones son vastas, y el maridaje de las bebidas tampoco se queda atras.

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Reservas: Reserva obligatoria

### 20. Rosanna Saad · 5★ · Hace 4 meses
Perfil: 6 reseñas · Etiquetas: Comida  |  Más de 1000 $

> Muy grata experiencia. Frescura y simplicidad en su máxima expresión, creatividad de sabores y servicio muy cálido.

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Nivel de ruido: Bajo, pero se puede conversar fácilmente · Tipo de asiento: Asientos en la barra

### 21. Francisco Cobo · 5★ · Hace 3 meses
Perfil: 11 reseñas · 12 fotos · Etiquetas: Comí allí  |  Comida

> Muy buen lugar para probar comida japonesa, te explican el platillo y el por que de los ingredientes, es una experiencia distinta.

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Tiempo de espera: Sin espera

### 22. essi block · 5★ · Hace 8 meses
Perfil: 1 reseña · Etiquetas: Comí allí

> Agradable experiencia, atención 10/10 del chef y la comida súper rica y de buena calidad. Súper recomendable si eres de vivir una experiencia única y nueva.

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5

### 23. Aries Ferreyra · 5★ · Hace 5 meses
Perfil: 1 reseña · Etiquetas: Más de 1000 $

> La comida está esquisita, aunque no sabes que vendrá o cuál es el siguiente plato, es seguro que estará delicioso, me tocó probar una sopa fría que me encantó, junto una anguila espectacular 1000/10

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Nivel de ruido: Bajo, pero se puede conversar fácilmente · Tamaño del grupo: 3-4 personas · Tipo de asiento: Asientos en la barra

### 24. Jennhy Torres · 5★ · Hace 5 meses
Perfil: Local Guide · 34 reseñas · 154 fotos · Etiquetas: Comida  |  Más de 1000 $

> Bonita y muy rica experiencia, la Chef Verónica muy atenta. Recomendable

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Reservas: Reserva obligatoria · Nivel de ruido: Bajo, pero se puede conversar fácilmente

### 25. Pablito Pro · 3★ · Hace 4 meses
Perfil: 1 reseña · Etiquetas: —

> Tenía muchas ganas de ir por todos los videos que había visto y la verdad el lugar sí se veía muy bien. No dudo que la comida esté rica, pero sí me llevé una mala impresión porque vi que tiraban todo el arroz sobrante directo a la banqueta. Además de ser un desperdicio de comida, siento que eso puede atraer roedores o plagas y la verdad da un poco de desconfianza.

### 26. Carem Rios · 5★ · Hace 8 meses
Perfil: 1 reseña · Etiquetas: —

> Super deliciosa comida una experiencia inigualable felicitaciones ala chef 💐

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Plaza de aparcamiento: Muchas plazas libres · Opciones de aparcamiento: Aparcamiento gratuito

### 27. Elihu Rivera · 2★ · Hace 8 meses
Perfil: Local Guide · 71 reseñas · 57 fotos · Etiquetas: Comí allí  |  Otro  |  Más de 1000 $

> De japonés solo el nombre.
> El lugar intenta verse “oriental”, pero la experiencia se queda en disfraz. El sushi parecía armado con prisa y sin cariño, el arroz pasado y el pescado sin frescura. Los sabores no cuadran y las porciones no justifican el precio. El servicio fue lento y desatento, como si pedir algo fuera una molestia. Si buscas comida japonesa de verdad, este restaurante es más ilusión que realidad.

Atributos: Comida: 1/5  |  Servicio: 1/5  |  Ambiente: 1/5 · Tiempo de espera: +1 hora

### 28. Coolbox · 5★ · Hace 9 meses
Perfil: 1 reseña · Etiquetas: Cena  |  Más de 1000 $

> Excelente lugar de comida japonesa, el omakase estuvo de lujo! Gracias

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Tiempo de espera: Sin espera · Plaza de aparcamiento: Muchas plazas libres

### 29. Esmeralda Vargas S. · 5★ · Hace 8 meses
Perfil: Local Guide · 21 reseñas · 6 fotos · Etiquetas: Más de 1000 $

> Uno de los mejores lugares para degustar comida japonesa en todo su explendor. El servicio de omakasen hace que la experiencia sea intima, especial y con mucho merito. Platillos con presentación impecable, ejecución master donde se nota la ha ilidad y experiencia de la chef. 300% recomendado y la plática es el plus extra.

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Nivel de ruido: Bajo, pero se puede conversar fácilmente · Tiempo de espera: Sin espera

### 30. Ricardo Rodriguez · 5★ · Hace 8 meses
Perfil: 1 reseña · Etiquetas: —

> No solo la comida está deliciosa, es una gran experiencia y la chef Morishita brinda un cálido servicio !!

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5

### 31. Maximiliano Gonzalez · 5★ · Hace 8 meses
Perfil: 3 reseñas · 3 fotos · Etiquetas: —

> El mejor Omakase de la baja 🫰🏻

### 32. Patricia Morishit · 5★ · Hace 9 meses
Perfil: 4 reseñas · Etiquetas: —

> Gracias hermana por seguir conservando nuestras raíces.
> Siempre sorprendiéndonos con cada sushi.

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5

### 33. Armida Arangure · 5★ · Hace 2 semanas
Perfil: Local Guide · 3 reseñas · Etiquetas: Comí allí  |  Más de 1000 $

> Delicioso todo, muy fresco el marisco, la atención de lujo, la l sabor exquisito y la ambientación de diez 🥰🌼🌷

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Nivel de ruido: Bajo, pero se puede conversar fácilmente · Tamaño del grupo: 3-4 personas

### 34. Pablo Farias · 5★ · Hace 2 semanas
Perfil: 1 reseña · Etiquetas: —

> Tiene un ambiente de hogar, muy delicioso los tiempos.

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5

### 35. Luiana Hernandez · 5★ · Hace 4 meses
Perfil: Local Guide · 14 reseñas · 1 foto · Etiquetas: —

> Atención excelente,  la comida tiene un muy buen sabor y la presentación es exquisita. Muy recomendable

### 36. ana rubio · 5★ · Hace 7 meses
Perfil: 1 reseña · Etiquetas: Cena  |  Más de 1000 $

_(sin texto)_

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Tamaño del grupo: 3-4 personas · Tiempo de espera: Sin espera

### 37. Martha Aguilar · 5★ · Hace 8 meses
Perfil: 1 reseña · Etiquetas: —

_(sin texto)_

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5

### 38. Fatima Contreras · 5★ · Hace un mes
Perfil: — · Etiquetas: Recogí el pedido  |  Más de 1000 $

_(sin texto)_

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 5/5 · Nivel de ruido: Bajo, pero se puede conversar fácilmente · Tamaño del grupo: 3-4 personas · Plaza de aparcamiento: Muchas plazas libres · Opciones de aparcamiento: Aparcamiento en la calle gratuito

### 39. Joel Martínez · 4★ · Hace un mes
Perfil: Local Guide · 1 reseña · Etiquetas: —

_(sin texto)_

Atributos: Comida: 5/5  |  Servicio: 5/5  |  Ambiente: 4/5

### 40. Manuel limon · 5★ · Hace 8 meses
Perfil: — · Etiquetas: —

_(sin texto)_

### 41. Venta de boilers y minisplits Mirage · 5★ · Hace 8 meses
Perfil: 8 reseñas · 6 fotos · Etiquetas: —

_(sin texto)_

## Capturas (prueba visual real)

En `fuente/capturas/resenas/`, tomadas del diálogo de Google a escala 3× (1779 px de ancho, nítidas para 1080 px), con "Más" expandido. Se ocultaron solo las fotos del cliente bajo el texto y la fila "Coloca el cursor encima para reaccionar"; nombre, perfil, estrellas, fecha y texto están intactos. Recomendado: difuminar avatares con cara antes de usarlas.

- `capturas/resenas/00-cabecera-4-9-41-resenas.png`
- `capturas/resenas/01-lucia-ojeda-5estrellas.png`
- `capturas/resenas/02-angelica-serrano-silva-5estrellas.png`
- `capturas/resenas/03-cyn-rm-5estrellas.png`
- `capturas/resenas/04-annet-alarcon-5estrellas.png`
- `capturas/resenas/05-karen-garcia-5estrellas.png`
- `capturas/resenas/06-danae-barreto-5estrellas.png`
- `capturas/resenas/07-esmeralda-vargas-s-5estrellas.png`
- `capturas/resenas/08-valeria-colado-5estrellas.png`
- `capturas/resenas/09-yara-correa-jauregui-5estrellas.png`
- `capturas/resenas/10-natalia-lopez-5estrellas.png`
- `capturas/resenas/11-rosanna-saad-5estrellas.png`
- `capturas/resenas/12-alejandra-rivera-5estrellas.png`
- `capturas/resenas/13-maximiliano-gonzalez-5estrellas.png`
- `capturas/resenas/14-jesus-ruben-villavicencio-ruiz-5estrellas.png`
- `capturas/resenas/15-miguel-angel-sepulveda-5estrellas.png`
- `capturas/resenas/16-carla-perea-5estrellas.png`
- `capturas/resenas/17-mar-5estrellas.png`
- `capturas/resenas/18-huerta-abraham-5estrellas.png`
- `capturas/resenas/19-anuar-dajlala-flores-5estrellas.png`
- `capturas/resenas/20-jafet-pedrotte-ortiz-5estrellas.png`
- `capturas/resenas/21-aries-ferreyra-5estrellas.png`
- `capturas/resenas/22-armida-arangure-5estrellas.png`
- `capturas/resenas/00-cabecera-4-9-41-resenas.png` (4,9 ★ · 41 reseñas)
