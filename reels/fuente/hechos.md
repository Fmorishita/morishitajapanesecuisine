# hechos.md: BORRADOR, lo confirma el dueño

> **Estado:** BORRADOR propuesto el 2026-10-08. Según CLAUDE.md este archivo es lo ÚNICO citable en los reels, y lo mantiene el dueño. **Nada aquí está confirmado por el dueño todavía.**
> Marcas: **[WEB]** = está en la web en vivo, falta tu OK · **[OK DUEÑO]** = confirmado (aún ninguno) · **[PENDIENTE]** = no se dice hasta que lo confirmes · **[NO USAR]** = no se usa en este lote.
> Fuentes: `JSON clave` = `fuente/web-content-api.json` (= `/api/content` en vivo, sobrescribe al HTML); `HTML clave` = `index.html` (= HTML en vivo, idéntico byte a byte); `IMG menú` = `assets/fotos/web/menu_14_tiempos-mjc.jpg` (la imagen de la sección "Menú de 14 tiempos"); `backend` = `backend/server.js`. Detalle de todo en `fuente/web.md`.

**Restricción de este lote (del dueño):** el Wagyu A5 y el Kobe **no** son protagonistas porque ahora no hay disponible. Pueden aparecer cero o casi cero veces.

---

## (a) Confirmados en la web en vivo (falta tu OK)

| # | Hecho | Texto literal en la web | Fuente | Uso en reels |
|---|---|---|---|---|
| A1 | Omakase de **14 tiempos** | "1 Barra. 4 Asientos. 14 Tiempos." · "Tiempos: 14" · "14 tiempos en formato degustación" | `JSON hero.sub` · `HTML reserve.row.tiempos.value` · IMG menú | [WEB] |
| A2 | **$1,850 MXN por persona** | "$1,850 MXN p/p" · "Precio por persona: Omakase Morishita — $1,850 MXN." · checkout "Por persona $1,850" | `HTML reserve.row.precio.value` · IMG menú · `index.html CFG.price=1850` · `backend PRECIO_POR_PERSONA_MXN=1850` | [WEB]. Si se dice el precio, decir también lo de las bebidas (ver B4). |
| A3 | Incluye **bebidas sin alcohol ilimitadas** | "Si, tu sesión de 14 tiempos incluye bebidas sin alcohol ilimitadas." · "Bebidas ilimitadas sin alcohol, ideal para acompañar la experiencia." | `JSON faq.a6` · IMG menú | [WEB]. El alcohol no se menciona en la web en vivo (ver D4). |
| A4 | Incluye **1 postre especial del chef** | "1 postre especial del chef, inspirado en sabores japoneses contemporáneos." | IMG menú | [WEB]. **No está claro si es uno de los 14 tiempos o es adicional** (ver D5). |
| A5 | **Máximo 4 comensales por sesión** | "Cuatro lugares por sesión." · "con máximo 4 comensales por sesión" · "Capacidad: 4 asientos" · flujo: "Máximo 4 personas por servicio." | `JSON pilares.p2.body` · IMG menú · `HTML reserve.row.capacidad.value` · `backend CAPACIDAD_MAXIMA_SESION=4` | [WEB]. Es **por sesión**; en un día hay hasta 3 sesiones (ver C). |
| A6 | **Una barra de 4 asientos** | "1 Barra. 4 Asientos." · "1 barra de 4 asientos." | `JSON hero.sub` · `JSON footer.desc` | [WEB] |
| A7 | Abre **solo sábado y domingo** | "Solo abrimos sábado y domingo." · "Servicio: Sáb · Dom" · "Una barra. Dos días por semana." | `JSON pilares.p2.body` · `HTML reserve.row.servicio.value` · `HTML footer.hours` · `index.html CFG.openDays=[0,6]` | [WEB] |
| A8 | **Solo con reservación** | "Servicio por reservación" | `HTML footer.service_note` | [WEB] |
| A9 | Dura **aproximadamente dos horas** | "Aproximadamente dos horas." | `HTML faq.a4` | [WEB] |
| A10 | Se prepara **a la vista / delante del comensal** | "Cada uno de los 14 tiempos se prepara a la vista y se sirve en su momento." · "En cada sesión, cada plato se construye delante del comensal." | `HTML faq.a4` · `JSON chef.p2` | [WEB] |
| A11 | **No hay carta**: el menú depende del mejor producto del día | "No hay carta. El menú lo construye el chef según el mejor producto del día." · "El menú lo dicta el mar y el día." · "Catorce tiempos Sorpresa" | `HTML faq.a3` · `JSON pilares.p3.title` · `JSON pilares.p3.num` | [WEB] |
| A12 | Progresión de **nigiris, sashimis, platillos calientes** y creaciones de la chef | "…degustaras un menú de 14 tiempos curados por la chef Vero Morishita, donde viviras una progresión de Nigiris, sashimis, platillos calientes y demás creaciones secretas de la chef." [sic] | `JSON custom.csmowqknu37iw.paragraph` | [WEB] |
| A13 | **Alergias y restricciones** se anotan al reservar | "Si tienes alergias o restricciones, indícalas al reservar y se adapta el menú sin sacrificar la experiencia." · checkout: "Alergias / restricciones (opcional)" por comensal | `HTML faq.a3` · `index.html buildGuestFields` | [WEB] |
| A14 | Campo **"Motivo"** al reservar (aniversario, cumpleaños) | "Motivo (opcional)" con el ejemplo "Aniversario, cumpleaños…" | `index.html #resForm` | [WEB]. Sirve para el CTA de ocasión, pero ese CTA requiere tu aprobación (CLAUDE.md). |
| A15 | **Anticipo del 50 %** con tarjeta (Stripe); el otro 50 % se paga en el restaurante después del servicio | "Anticipo: 50%" · "Anticipo hoy · 50% · Vía Stripe" · "El 50% restante … se paga en el restaurante después del servicio." | `JSON reserve.row.anticipo.value` · `index.html` checkout · `backend PORCENTAJE_ANTICIPO=0.5`, `payment_method_types:['card']` | [WEB] |
| A16 | Anticipo **reembolsable hasta 48 h antes** | "Reembolsable hasta 48 horas antes del servicio. Después de ese momento, el anticipo se aplica al producto que ya separamos para tu sesión." | `JSON faq.a2` | [WEB]. Sustituye a las 72 h de CLAUDE.md (ver B3). |
| A17 | **Ubicación: Ensenada, Baja California, México** | "Ensenada · Baja California" · "Ensenada, Baja California, México" · "La familia Morishita trae a Ensenada…" | `JSON hero.eyebrow` · `JSON footer.location` · `JSON hero.sub` | [WEB]. Sin dirección exacta (D1). |
| A18 | **Chef Vero Morishita**, formada en la disciplina clásica japonesa, **+15 años** | "Chef Vero Morishita / Una vida en la barra y cocina." · "Formada en la disciplina clásica japonesa, la chef Vero Morishita lleva +15 años perfeccionando el oficio del Omakase y la cocina japonesa." | `JSON chef.h2`, `JSON chef.p1` | [WEB]. En escritorio la firma aún dice "Chef Morishita" (B2). |
| A19 | **Fran Morishita**, fundador de Morishita Meat y Morishita Japanese Cuisine | "Fran Morishita, Fundador de  Morishita Meat y Morishita Japanese Cuisine…" | `JSON custom.csmot6cqlyzxu.paragraph` | [WEB]. CLAUDE.md: Morishita Meat solo si lo pides. |
| A20 | Negocio **familiar** | "La familia Morishita trae a Ensenada una experiencia omakase auténtica" | `JSON hero.sub` | [WEB] |
| A21 | **Pescado y marisco de temporada**, selección semanal; cortes del Pacífico y, según temporada, de importación japonesa | "el mejor pescado y marisco de temporada" · "Pescado de temporada de las mejores aguas." · "Selección semanal. Cortes premium del Pacífico y de importación japonesa cuando la temporada lo requiere." | `JSON hero.sub` · `JSON pilares.p1.body` · `HTML producto.item2.body` | [WEB]. "Importación japonesa" se dice solo si la confirmas para la temporada actual (D11). |
| A22 | **Arroz japonés, vinagre maderado, dashi preparado en casa** | "Arroz japonés cocido al punto, sazonado con vinagre maderado. Dashi preparado en casa." | `HTML producto.item3.body` | [WEB]. La web dice "maderado", no "añejado" como CLAUDE.md (B10). |
| A23 | Servicio tipo **chef's table**, atención personalizada, espacio privado | "Atención personalizada en un servicio tipo chef's table…" · "Acceso a un espacio privado con máximo 4 comensales por sesión" | IMG menú | [WEB] |
| A24 | **Frase del chef** | "El producto manda. Nuestra técnica solo lo acompaña." | `HTML chef.quote` (sigue en vivo) | [WEB] |
| A25 | **Reserva directa** en la web, en 4 pasos (Comensales → Fecha → Horario → Reservar) | link `https://www.morishitajapanesecuisine.com/?reservar=1` | `index.html` (STEP_PARAMS, flujo) | [WEB]. Probado en vivo: carga y muestra el calendario. |
| A26 | **WhatsApp +52 646 245 4294**; dudas por WhatsApp | `https://wa.me/+526462454294` · "Si tu pregunta no está aquí, escríbenos por WhatsApp. Respondemos personalmente." | `JSON footer.whatsapp_url` · `HTML faq.lead` | [WEB] |
| A27 | **Instagram: @morishita.japanesecuisine** | `https://instagram.com/morishita.japanesecuisine` | `JSON footer.instagram_url` | [WEB] (coincide con tu perfil) |
| A28 | Email **reservas@morishitajapanesecuisine.com** | enlace "Email" del footer | `HTML footer.email_href` | [PENDIENTE] confirmar que el buzón existe (D8). |
| A29 | Código de vestimenta: **no formal** | "No hay código formal. Sugerimos vestir cómodo pero cuidado." | `HTML faq.a5` | [WEB] |
| A30 | Wagyu A5 de **Miyazaki** y Kobe de **Hyogo**, "100% certificado" | "Wagyu Beef A5 / Importado desde Miyazaki, Japón" · "…El Wagyu A5 de la prefectura de Miyazaki y Kobe autentico de Hyogo, Japón, 100% certificado…" | `JSON producto.h2` · `JSON custom.csmot6cqlyzxu.paragraph` | **[NO USAR]** en este lote (no hay disponible) y, en general, solo con certificado o factura archivados (D3). |

## (b) Contradicciones (repo vs web en vivo vs base de CLAUDE.md)

| # | Tema | HTML del repo (sustituido, ya no se ve) | Web en vivo | Base de CLAUDE.md | Propuesta |
|---|---|---|---|---|---|
| B1 | Ubicación | "Omakase · Baja California"; footer "Baja California, México"; metadatos con keywords "tijuana, omakase tijuana" | "Ensenada · Baja California" / "Ensenada, Baja California, México" | Fórmula de gancho "Así se ve un omakase en **Tijuana**"; hashtags "Tijuana" | Usar **Ensenada**. Corregir el gancho y los hashtags de CLAUDE.md/prompt-arranque (Ensenada, Baja). Los metadatos de la web siguen diciendo Baja California, Kobe y tijuana. |
| B2 | Nombre y género del chef | "Chef Morishita", "el chef", "Formado…", "lleva años" | "Chef Vero Morishita", "la chef", "Formada…", "+15 años" (móvil). En **escritorio la firma sigue siendo "— Chef Morishita · 森下"** | "nombre del chef" no citable; prompt: "¿cómo lo nombramos?" | **"Chef Vero Morishita" / "la chef"** cuando lo confirmes. Corregir la firma de escritorio (`chef.sign`). |
| B3 | Reembolso del anticipo | "hasta **72 horas** antes" | "hasta **48 horas** antes" | "reembolsable hasta 72 h antes" | **48 h**. Actualizar CLAUDE.md. |
| B4 | Bebidas | "El precio del Omakase es solo el menú de 14 tiempos. Bebidas (sake, vino de Valle, agua, etc.) se cobran aparte. Te recomendamos el sake del chef." | "incluye bebidas sin alcohol ilimitadas" (FAQ e imagen del menú). **No dice nada del alcohol.** | "bebidas aparte"; "Precio siempre en MXN e indicando que las bebidas son aparte" | Proponer: "$1,850 MXN por persona, con bebidas sin alcohol ilimitadas incluidas". Decir "alcohol aparte" solo si confirmas que se vende (D4). Actualizar la regla de CLAUDE.md. |
| B5 | Wagyu A5 / Kobe | Hero, pilares, producto y footer: "Wagyu A5 y Kobe importados de Japón" | Hero, pilares, producto y footer: **solo Wagyu A5** (Miyazaki). Kobe (Hyogo) solo en la sección Morishita Meat y en los metadatos | Se usan solo con certificado o factura | Este lote: ni Wagyu ni Kobe como protagonistas. **Alerta:** el hero en vivo promete que la experiencia trae Wagyu A5; si hoy no hay, la web misma puede ser engañosa (D3). |
| B6 | "Noches" vs "días" | "Dos noches por semana" (pilares, reservar, FAQ) | Pilares y reservar: "Dos días por semana"; **FAQ a1 sigue diciendo "Dos noches por semana"** | — | Usar "**sábado y domingo**" o "dos días por semana" (hay sesión de 1:00 pm, no solo de noche). |
| B7 | Autores de las reseñas | "Lucia Ojeda · Google", "**Angelica Serrano Silva** · Google", "Cyn RM · **Local Guide** · Google" | "Lucia Ojeda · Tijuana", "**Angelica Serrano.** · San Diego", "Cyn RM · Mexicali" | "Lucia Ojeda, Angelica Serrano Silva, Cyn RM"; regla: "con el nombre como aparece en Google" | Verificar en Google el nombre exacto (sobre todo Serrano vs Serrano Silva) y de dónde salen las ciudades antes de citar (D7). |
| B8 | Instagram | `instagram.com/morishitajapanesecuisine` | `instagram.com/morishita.japanesecuisine` | El prompt marcaba la discrepancia | **@morishita.japanesecuisine** (ya corregido en vivo). |
| B9 | Titular | "El producto / al frente." | "Omakase / Confia en el chef" | Titular "El producto al frente." | "El producto al frente" **ya no está en la web en vivo**. Si lo quieres citable, confírmalo como frase de marca. La frase del chef sí sigue en vivo. |
| B10 | Vinagre del arroz | "vinagre maderado" | "vinagre maderado" (sin cambio) | "arroz con vinagre **añejado**" | Usar "**maderado**" (es lo que dice la web) o confirmar cuál es correcto. |
| B11 | Anticipo y cuenta final | "se aplica directamente a tu cuenta final, no es un cargo adicional" | Esa frase se quitó; el checkout dice "El 50% restante … se paga en el restaurante después del servicio" | — | Decir "anticipo del 50 %; el resto se paga en el restaurante". |
| B12 | Postre | — | La imagen del menú lista "14 tiempos" y "1 postre especial del chef" como viñetas separadas | Contexto del lote: "los 14 tiempos incluyen 1 postre" | Ambiguo: confirmar (D5). Mientras tanto no decir "14 tiempos + postre" ni "postre incluido en los 14". |
| B13 | Variantes móvil y escritorio | — | Producto/Carne: móvil "Nigiri de Wagyu A5 … respetan la tradición japonesa"; escritorio "Wagyu A5 … tataki, sumibiyaki, nigiri". Menú en escritorio con eyebrow de relleno "ETIQUETA" | — | Arreglo de la web (fuera del alcance de los reels). |
| B14 | Marca en la imagen del menú | — | "AUTHENTIC JAPANESE **QUISINE**" y un logo sans distinto al de la web | "Authentic Japanese Cuisine" | En reels usar "Authentic Japanese Cuisine" y el logo de la web (`marca/logo/`). |
| B15 | Escasez | — | Flujo: contador "8:00 restantes" / "si expira se libera tu lugar" | Escasez y urgencia solo reales | El contador es solo del navegador: **el backend no aparta lugares**. **No usarlo como urgencia en reels.** La insignia "Últimos lugares" sí es real (sale con ≤ 2 lugares), pero solo vale el día que la confirmes. |

## (c) Horarios de sesión (código + prueba en vivo)

**Código:**
- `index.html` → `CFG={price:1850, openDays:[0,6], slots:['13:00','15:30','18:00'], max:4, dep:.5}` y los nombres `SN={'13:00':'Comida temprana','15:30':'Sobremesa','18:00':'Cena omakase'}`. El calendario solo deja elegir **domingo (0) y sábado (6)**.
- `backend/server.js` → `GET /disponibilidad?fecha=YYYY-MM-DD` devuelve `COMIDA`, `TARDE` y `CENA`, cada una con `capacidad: 4`, `ocupados`, `disponibles` y `bloqueado` (tabla `time_blocks` por fecha+horario o `DIA_COMPLETO`). `mapearHorario`: 12–14 h → COMIDA (1:00 pm), 14–17 h → TARDE (3:30 pm), 17–20 h → CENA (6:00 pm). Existe el enum `NOCHE`, pero no se ofrece.
- El backend **no** valida el día de la semana: el jueves 2026-10-08 respondió 4/4 libres. La restricción sábado/domingo está solo en la web.

**Prueba en vivo** (GET de solo lectura, 2026-10-08 ~09:06 UTC):

| Fecha | 1:00 pm (COMIDA) | 3:30 pm (TARDE) | 6:00 pm (CENA) |
|---|---|---|---|
| Sáb 2026-10-10 | 4 de 4 libres | 4 de 4 | 4 de 4 |
| Dom 2026-10-11 | **bloqueado** | **bloqueado** | **bloqueado** |
| Sáb 2026-10-17 | 4 de 4 | 4 de 4 | 4 de 4 |

El calendario de octubre 2026 (captura) muestra disponibles los sáb 10, 17, 24, 31 y dom 18, 25; el dom 11 sale como lleno/cerrado.

**Conclusión (por confirmar):** hay **3 sesiones por día** (1:00 pm, 3:30 pm, 6:00 pm), sábado y domingo, de hasta 4 personas cada una. Las sesiones de ~2 h caben en esos huecos (1:00–3:00, 3:30–5:30, 6:00–8:00). Antes de decir horarios en un reel, confirma que las 3 sesiones operan de verdad (D2).

## (d) PENDIENTE de confirmar por el dueño (no se dice hasta tu OK)

| # | Qué falta | Por qué importa |
|---|---|---|
| D1 | **Dirección exacta o zona** en Ensenada (y link de Google Maps) | La web solo dice "Ensenada, Baja California, México". Ayuda a vender ("a 5 min de…"), pero no se dice sin confirmar. |
| D2 | **Horarios**: ¿operan las 3 sesiones (1:00, 3:30 y 6:00 pm)? ¿Se pueden publicar? ¿Hora de llegada? | Está en el código y en la API, no en el texto de la web. |
| D3 | **Wagyu A5 / Kobe**: certificado o factura de importación (Miyazaki / Hyogo) archivados; **disponibilidad actual: no hay** | CLAUDE.md (LFPC art. 32; Kobe es denominación protegida). La web en vivo promete Wagyu A5 en el hero, los pilares, el producto y el footer: si hoy no se sirve, conviene ajustarla. |
| D4 | **Alcohol**: ¿se vende sake/vino/cerveza? ¿Se puede llevar? ¿Qué leyenda legal pide el abogado? | La web en vivo solo dice "bebidas sin alcohol ilimitadas". El HTML viejo mencionaba sake, vino de Valle y "el sake del chef". La foto del hero (IA) muestra botellas de sake. |
| D5 | **Postre**: ¿es uno de los 14 tiempos o es adicional? | La imagen del menú lo lista aparte. |
| D6 | **Nombre del chef** en reels: ¿"Chef Vero Morishita", "la chef Vero", "Chef Morishita"? | En móvil se ve "Chef Vero Morishita"; en escritorio, "Chef Morishita". |
| D7 | **Reseñas**: nombre exacto en Google (¿"Angelica Serrano" o "Angelica Serrano Silva"?), si las ciudades salen del perfil de Google, y que las 3 existan públicamente en Google | Regla de CLAUDE.md: textual y con el nombre como aparece en Google. La web les pone el sello "Reseña verificada · Google". |
| D8 | ¿Funciona **reservas@morishitajapanesecuisine.com**? | Aparece en el footer. |
| D9 | **Precio $1,850 MXN**: ¿vigente? ¿Incluye IVA? ¿Propina aparte? | Para no prometer de más en el CTA. |
| D10 | **Reembolso 48 h**: ¿también aplica a cambios de fecha? | Hoy la web solo habla de reembolso. |
| D11 | ¿Hoy hay pescado de **importación japonesa**? ¿Qué producto de temporada hay este mes? | Para el reel de producto sin Wagyu ni Kobe: se necesita el producto estrella real del fin de semana. |
| D12 | ¿Se puede mencionar a **Fran Morishita** o a **Morishita Meat**? | CLAUDE.md: Morishita Meat solo si lo pides. |
| D13 | **Foto del hero de la web generada por IA** (`hero-comensales-generated.jpg`) | No se usa en reels (CLAUDE.md prohíbe IA de platos, interiores y personas como si fueran reales). Valorar cambiarla en la web por una foto real. Según el inventario del lote, varias fotos de la web llevan la marca ✦ de Gemini (no lo verifiqué foto por foto): revisar en `assets/catalogo.md`. |
| D14 | ¿Edad mínima o menores? ¿Estacionamiento? ¿Accesibilidad? | Preguntas frecuentes de leads calientes (opcional). |
| D15 | ¿Fechas bloqueadas este mes, como el **dom 11 de octubre**? ¿Eventos privados (barra completa para 4)? | La API muestra el dom 11 bloqueado. "Mesa completa · toda la barra para tu grupo" sale en el flujo al elegir 4 personas. |
| D16 | Frase de marca "**El producto al frente.**": ¿se sigue usando? | Ya no está en la web en vivo. |

## (e) Reseñas de la web (textuales; autor EXACTO como aparece en la web en vivo)

Todas llevan ★★★★★ y el sello "Reseña verificada · Google". Fuente: `JSON social.t1–t3.quote/author`. **Antes de citarlas, verifica el nombre en Google (D7).** Las comillas rectas y la raya "—" son de la web.

1. "Una experiencia espectacular de principio a fin. La chef explica cada pieza con detalle, los ingredientes frescos y cada tiempo perfectamente balanceado. Un omakase auténtico, de calidad y lleno de detalles."
   **— Lucia Ojeda · Tijuana** (en el HTML del repo: "— Lucia Ojeda · Google")
2. "Me encantó todo — ingredientes frescos, ambiente agradable y la chef muy amigable. Es toda una experiencia ver la preparación de cada platillo. 100% recomendado, definitivamente volvería."
   **— Angelica Serrano. · San Diego** (así, con punto; en el HTML del repo y en CLAUDE.md: "Angelica Serrano Silva")
3. "Sin duda de la mejor cocina japonesa en Baja. Disfrutamos muchísimo el omakase que reservamos en Morishita. La comida deliciosa y una experiencia que vale cada peso."
   **— Cyn RM · Mexicali** (en el HTML del repo: "— Cyn RM · Local Guide · Google")

Fragmentos cortos (≤ 8 palabras) literales. Se citan con "…" si se recortan y siempre con el autor:
- "Una experiencia espectacular de principio a fin." (Lucia Ojeda)
- "La chef explica cada pieza con detalle" (Lucia Ojeda)
- "Me encantó todo" (Angelica Serrano)
- "100% recomendado, definitivamente volvería." (Angelica Serrano)
- "una experiencia que vale cada peso" (Cyn RM)

Capturas listas: `fuente/capturas/resena-t1|t2|t3-dark.png` (tarjeta sola, 1082 px de ancho).

## (f) Frases citables cortas para reels (≤ 8 palabras, literales de la web en vivo)

Verificadas por script contra el texto renderizado en vivo y la transcripción del menú. Si la web trae una errata, se indica la forma corregida que se usaría en pantalla.

**Experiencia y formato**
- "1 Barra. 4 Asientos. 14 Tiempos." · `JSON hero.sub`
- "Omakase" / "Confia en el chef" · `JSON hero.h1`. En pantalla: "Confía en el chef".
- "Omakase Significa confiar en el chef" · `JSON custom.csmowqknu37iw.paragraph`. En pantalla: "Omakase significa confiar en el chef".
- "Catorce tiempos Sorpresa" · `JSON pilares.p3.num`
- "14 tiempos en formato degustación" · IMG menú
- "No hay carta." · `HTML faq.a3` / `pilares.p3.body`
- "El menú se construye pieza por pieza" · `JSON reservar.lead`
- "cada plato se construye delante del comensal" · `JSON chef.p2`
- "Aproximadamente dos horas." · `HTML faq.a4`
- "Es una experiencia para disfrutar sin prisa." · `HTML faq.a4`
- "La barra es íntima" · `HTML faq.a5`
- "una cena que importa" · `HTML faq.a5`
- "servicio tipo chef's table" · IMG menú
- "Atención personalizada" · IMG menú
- "un entorno íntimo y exclusivo" · IMG menú
- "una experiencia tranquila y sin interrupciones" · IMG menú
- "La misma cena no se repite jamás." · `HTML pilares.p3.body`. Es una afirmación absoluta: úsala solo si la sostienes.

**Exclusividad (escasez real, no inventada)**
- "Cuatro asientos." / "Solo dos días por semana." · `JSON reservar.h2`
- "Una barra. Dos días por semana." · `JSON pilares.p2.title`
- "Solo abrimos sábado y domingo." · `JSON pilares.p2.body`
- "Cuatro lugares por sesión." · `JSON pilares.p2.body`
- "máximo 4 comensales por sesión" · IMG menú
- "1 barra de 4 asientos." · `JSON footer.desc`
- "Mesa completa · toda la barra para tu grupo." · flujo de reserva (4 personas)

**Producto (sin Wagyu ni Kobe)**
- "el mejor pescado y marisco de temporada" · `JSON hero.sub`
- "Pescado de temporada de las mejores aguas." · `JSON pilares.p1.body`
- "Pescado y mariscos de temporada." · `JSON footer.desc`
- "Cada pieza, seleccionada a mano." · `HTML pilares.p1.title`
- "Selección semanal." · `HTML producto.item2.body`
- "Cortes premium del Pacífico" · `HTML producto.item2.body`
- "Arroz, vinagre, dashi" · `HTML producto.item3.title`
- "Dashi preparado en casa." · `HTML producto.item3.body`
- "donde se reconoce un Omakase real" · `HTML producto.item3.body`
- "Selección de ingredientes premium" · IMG menú
- "ingredientes seleccionados al momento" · IMG menú
- "El insumo debe ser de la mejor calidad." · `JSON producto.p1`

**Chef y marca**
- "El producto manda." / "Nuestra técnica solo lo acompaña." · `HTML chef.quote`
- "Una vida en la barra y cocina." · `JSON chef.h2`
- "Formada en la disciplina clásica japonesa" · `JSON chef.p1`
- "+15 años perfeccionando el oficio del Omakase" · `JSON chef.p1`
- "una experiencia omakase auténtica" · `JSON hero.sub`
- "Tres reglas. Sin excepción." · `HTML pilares.title`
- "La barra habla por sí sola" · `JSON social.title`
- "Lo que dicen quienes ya estuvieron" · `HTML social.eyebrow`

**Incluido**
- "incluye bebidas sin alcohol ilimitadas" · `JSON faq.a6`
- "Bebidas ilimitadas sin alcohol" · IMG menú
- "1 postre especial del chef" · IMG menú (ver D5)

**CTA (textos de botones y flujo)**
- "Reserva tu lugar" · `JSON reservar.eyebrow`
- "Ver fechas disponibles" · `HTML cta.reservar_section.label`
- "Reservar asientos" · `JSON cta.hero_primary.label`
- "Servicio por reservación" · `HTML footer.service_note`
- "¿Cuántos asientos este día?" · flujo, paso 1
- "Elige tu servicio." · flujo, paso 3
- "Te esperamos en Morishita" · pantalla de confirmación
- "Respondemos personalmente." · `HTML faq.lead`
- "Ensenada · Baja California" · `JSON hero.eyebrow`

Casi citables (pasan de 8 palabras; se usan completas solo como texto secundario, no como gancho): "El menú lo dicta el mar y el día." (9) · "Si tu pregunta no está aquí, escríbenos por WhatsApp." (9).
