# Web en vivo de Morishita: copia textual

- **URL:** https://www.morishitajapanesecuisine.com
- **Extraído:** 2026-10-08 09:05–09:15 UTC (02:05–02:15 hora de Ensenada).
- **Cómo:**
  1. `curl` del HTML en vivo: es **idéntico byte a byte** al `index.html` del repo (124,936 bytes).
  2. `GET /api/content` en vivo: es **idéntico** a `reels/fuente/web-content-api.json` (14,876 bytes). Al cargar, la página aplica ese JSON encima del HTML (los valores del JSON sobrescriben el texto estático).
  3. Render con Playwright/Chromium en móvil (412 px) y en escritorio (1440 px) para leer el texto final tal como lo ve el visitante. Se bloqueó PostHog para no ensuciar las analíticas.
- **Leyenda de origen:**
  - **[JSON `clave`]**: valor de `web-content-api.json`; sobrescribe al HTML.
  - **[JSON `clave.mobile`]**: variante que solo se ve en móvil.
  - **[HTML `clave`]**: texto estático de `index.html`; no tiene override, así que se ve tal cual.
  - **[IMG]**: texto dentro de una imagen.
  - *Antes (HTML repo)*: texto estático que el JSON reemplazó. Ya **no** se ve en vivo y solo sirve para rastrear contradicciones.
- Los textos se copian **literal**, con sus erratas (las marco con [sic] y las listo al final). Los `<em>` (segunda línea en cursiva de los títulos) se muestran como " / ".
- **Excluido a propósito:** las claves `evaluacion_miyagi_*` del JSON. Son datos internos de una evaluación de platillos (incluyen el nombre de una persona), no contenido de la web. Ver la nota de privacidad al final.

**Orden real de las secciones en vivo** (`sections.order`): Hero → Chef → Pilares → Omakase Experience (custom) → Morishita Meat (custom) → Producto → Menú de 14 tiempos (custom) → Reseñas → Reservar → FAQ → Footer.

---

## 0. Metadatos (pestaña, Google, WhatsApp/Facebook) [HTML, sin override]

- `<title>`: Morishita — Omakase Baja California · Wagyu A5 · 4 asientos
- description: Omakase de 14 tiempos en Baja California. Wagyu A5 y Kobe importados de Japón. Cuatro asientos. Sábados y domingos. Reserva con anticipo.
- keywords: omakase, baja california, tijuana, wagyu a5, kobe, sushi premium, japanese cuisine, omakase tijuana, omakase baja, morishita
- og:title / twitter:title: Morishita — Omakase · Baja California
- og:description: 14 tiempos. Wagyu A5 y Kobe importados de Japón. Una barra de cuatro asientos. Sábados y domingos.
- twitter:description: 14 tiempos. Wagyu A5 y Kobe importados de Japón. Cuatro asientos. Sáb · Dom.
- og:image: favicon.png (森下 dorado sobre negro)

> Ojo: los metadatos siguen diciendo "Kobe", "Baja California" y "tijuana" aunque la página ya dice Ensenada.

## 1. Barra superior y logo [HTML]

- Logo (SVG): **森下** | **MORISHITA** | **AUTHENTIC JAPANESE CUISINE**
- Menú: La experiencia · El producto · El chef · FAQ · **Reservar**
- Botón flotante de tema (luna/sol). El tema es automático: oscuro si el sistema está en oscuro **o** si son entre las 19:00 y las 07:00; si no, claro.

## 2. Hero

| Elemento | Texto en vivo | Origen |
|---|---|---|
| Eyebrow | Ensenada · Baja California | [JSON `hero.eyebrow`] · *Antes:* Omakase · Baja California |
| Título | **Omakase** / *Confia en el chef* [sic: sin tilde] | [JSON `hero.h1`] · *Antes:* El producto / al frente. |
| Subtítulo | 1 Barra. 4 Asientos. 14 Tiempos. **La familia Morishita trae a Ensenada una experiencia omakase auténtica: el mejor pescado y marisco de temporada, junto la carne más exclusiva: el Wagyu A5 importado desde Japón.** [sic: "junto la"] | [JSON `hero.sub`] · *Antes:* Una barra de cuatro asientos. Catorce tiempos curados con Wagyu A5, Kobe importado de Japón y el mejor pescado de la temporada. |
| Botón | Reservar asientos → | [JSON `cta.hero_primary.label`] · *Antes:* Reservar mesa |
| Imagen | foto de 4 comensales en una mesa con sushi y botellas de sake | [JSON `img.hero`] = `…/1777712099906-Generated_Image_May_02__2026_-_1_54AM.jpg` → local `assets/fotos/web/hero-comensales-generated.jpg`. **Es una imagen generada por IA** (así se llama el archivo en el servidor). |
| Ocultos | botón "Conocer la experiencia", meta "Sáb · Dom / 4 asientos / 14 tiempos / $1,850 MXN p/p", etiqueta "La barra · 4 asientos · Sábados & Domingos" | `cta.hero_secondary.show`, `hero.meta.show` y `hero.card_tag.show` = false |

## 3. El chef

| Elemento | Texto en vivo | Origen |
|---|---|---|
| Eyebrow | El chef | [HTML `chef.eyebrow`] |
| Título | Chef Vero Morishita / *Una vida en la barra y cocina.* (en escritorio "Chef Vero Morishita." con punto) | [JSON `chef.h2` y `chef.h2.mobile`] · *Antes:* Chef Morishita. / Una vida en la barra. |
| Párrafo 1 | Formada en la disciplina clásica japonesa, la chef Vero Morishita lleva +15 años perfeccionando el oficio del Omakase y la cocina japonesa. | [JSON `chef.p1`] · *Antes:* Formado en la disciplina clásica japonesa, el chef Morishita lleva años perfeccionando el oficio del Omakase: la lectura del producto, la temperatura exacta, el corte preciso, el silencio entre tiempos. |
| Párrafo 2 | En cada sesión, cada plato se construye delante del comensal. | [JSON `chef.p2`] · *Antes:* En cada servicio, cada plato se construye delante del comensal. No hay carta porque no hay receta fija — hay una conversación entre el chef, el producto del día y los cuatro invitados que se sientan a la barra. |
| Cita | "El producto manda. Nuestra técnica solo lo acompaña." | [HTML `chef.quote`] (sigue en vivo) |
| Firma | **Móvil:** — Chef Vero Morishita · 森下 · **Escritorio:** — Chef Morishita · 森下 | [JSON `chef.sign.mobile`]; en escritorio no hay override y queda el HTML. **Inconsistencia en vivo.** |
| Imagen | chef (mujer) en la barra | [JSON `img.chef`] → `assets/fotos/web/vero_v2.jpg` |

## 4. Pilares ("La filosofía")

- Eyebrow: La filosofía [HTML]
- Título: **Tres reglas.** / *Sin excepción.* [HTML `pilares.title`]
- Lead: Un Omakase no se mide solo por la receta. Se mide por la materia prima, el tiempo dedicado a cada pieza y la intimidad del servicio. [JSON `pilares.lead`] · *Antes:* "…no se mide por la receta…"

| # | Número | Título | Cuerpo |
|---|---|---|---|
| 01 | 01 · El producto manda [HTML] | Cada pieza, seleccionada a mano. [HTML] | Pescado de temporada de las mejores aguas. Carne Wagyu A5 importada de Japón. [JSON `pilares.p1.body`] · *Antes:* Wagyu A5 y Kobe importados de Japón. Pescado de temporada de las mejores aguas. Si una pieza no llega al estándar, no entra a la barra. |
| 02 | 02 · Cuatro asientos [HTML] | Una barra. Dos días por semana. [JSON `pilares.p2.title`] · *Antes:* Una barra. Dos noches por semana. | Solo abrimos sábado y domingo. Cuatro lugares por sesión. [JSON `pilares.p2.body`] · *Antes:* Solo abrimos sábado y domingo. Cuatro lugares por servicio. El chef cocina y narra cada tiempo frente a ti. |
| 03 | 03 · Catorce tiempos Sorpresa [JSON `pilares.p3.num`] | El menú lo dicta el mar y el día. [JSON `pilares.p3.title`] · *Antes:* El menú lo dicta el día. | No hay carta. Hay una secuencia construida con el mejor producto que llegó esa semana. La misma cena no se repite jamás. [HTML `pilares.p3.body`] |

## 5. Omakase Experience (sección custom `csmowqknu37iw`) [JSON]

- Eyebrow: Omakase Experience
- Título: ¿Como funciona la / *expericia Omakase?* [sic: "Como" sin tilde, "expericia"]
- Párrafo: Omakase Significa confiar en el chef, degustaras un menú de 14 tiempos curados por la chef Vero Morishita, donde viviras una progresión de Nigiris, sashimis, platillos calientes y demás creaciones secretas de la chef. [sic: "degustaras", "viviras" sin tilde]
- Botón: Saber más → URL `/?reservar=1` en escritorio (con un espacio inicial) y `#/?reservar=1` en móvil (`button_url.mobile`). Probablemente en móvil no abre la reserva.
- Imagen: `assets/fotos/web/vero_v3.jpg`

## 6. Morishita Meat (sección custom `csmot6cqlyzxu`) [JSON]

- Eyebrow: MORISHITA MEAT - KOBE & wagyu a5 (se muestra en mayúsculas)
- Título: Morishita Meat - / *The Finest Beef on Earth*
- Párrafo: Fran Morishita, Fundador de  Morishita Meat y Morishita Japanese Cuisine,  trae a Ensenada la carne más exclusiva a nivel global: El Wagyu A5 de la prefectura de Miyazaki y Kobe autentico de Hyogo, Japón, 100% certificado , brindando experiencias gastronómicas únicas [sic: dobles espacios, "autentico" sin tilde, espacio antes de la coma, sin punto final]
- Botón oculto (`button_show` = false).
- Imagen: `assets/fotos/web/WAGYU_FRAN_VF3.jpg`

## 7. Producto ("El insumo")

Orden de las tarjetas en vivo (`producto.order`): Pescado → Base → Carne.

- Eyebrow: El insumo [HTML]
- Título: **Wagyu Beef A5** / *Importado desde Miyazaki, Japón* [JSON `producto.h2`] · *Antes:* Wagyu A5. Kobe. / Importados directo de Japón.
- P1: El corazón de un Omakase serio no es solo la técnica. El insumo debe ser de la mejor calidad. [JSON `producto.p1`] · *Antes:* El corazón de un Omakase serio no es la técnica: es la pieza. Por eso trabajamos con una sola exigencia, sin atajos.
- P2: Carne Wagyu A5 certificada, importadas pieza por pieza. [sic: "importadas"] [JSON `producto.p2`] · *Antes:* Carnes Wagyu A5 y Kobe certificadas, importadas pieza por pieza. Pescado fresco de selección. Arroz japonés, vinagre maderado y dashi preparado en casa. Cada elemento pasa por un solo filtro: ¿es lo mejor que se puede conseguir hoy?
- Imagen principal + etiqueta: `assets/fotos/web/wagyu-hero.jpg` · "Wagyu A5 · Origen Japón · Certificado" [HTML `producto.card_tag`]

| Tarjeta | Etiqueta | Título | Cuerpo | Imagen |
|---|---|---|---|---|
| Pescado | Pescado [HTML] | Pescado de temporada [HTML] | Selección semanal. Cortes premium del Pacífico y de importación japonesa cuando la temporada lo requiere. Lo que no esté en el punto, no entra al servicio. [HTML] | [JSON `img.pescado`] → `producto-pescado-v2-live.jpg` |
| Base | Base [HTML] | Arroz, vinagre, dashi [HTML] | Arroz japonés cocido al punto, sazonado con vinagre maderado. Dashi preparado en casa. La base que la mayoría descuida — y donde se reconoce un Omakase real. [HTML] | `producto-base.jpg` |
| Carne | Carne [HTML] | **Móvil:** Nigiri de Wagyu A5 [JSON `.mobile`] · **Escritorio:** Wagyu A5 [JSON] · *Antes:* Wagyu A5 + Kobe | **Móvil:** Importados directo de Japón con certificación de origen. Marmoleado A5, el grado más alto del estándar japonés. Servido en preparaciones que respetan la tradición japonesa. · **Escritorio (HTML):** …Servido en preparaciones que respetan la pieza: tataki, sumibiyaki, nigiri. | `producto-carne.jpg` (nigiri con hoja de oro, según el alt) |

## 8. Menú de 14 tiempos (sección custom `csmowt1n3juvx`) [JSON]

- Eyebrow: vacío en móvil (`eyebrow.mobile` = ""). **En escritorio se ve "ETIQUETA"**, un texto de relleno de la plantilla que quedó publicado.
- Título: Menú de / *14 tiempos*
- Párrafo: Experiencia diseñada para llevarte por una progresión equilibrada de sabores y texturas, que te sorprenderán en cada tiempo.
- Botón: Saber más → URL `#` (no lleva a ningún lado).
- Imagen: `assets/fotos/web/menu_14_tiempos-mjc.jpg`

### 8.1 Transcripción de la imagen `menu_14_tiempos-mjc.jpg` [IMG]

> **森下**
> **MORISHITA**
> AUTHENTIC JAPANESE QUISINE [sic: "QUISINE"]
>
> \*\***Precio por persona:** Omakase Morishita —
> **$1,850 MXN.**
>
> Incluye una experiencia completa diseñada especialmente para grupos reducidos, con ingredientes seleccionados al momento y técnicas japonesas contemporáneas:
>
> • **14 tiempos en formato degustación**, estructurados para llevarte por una progresión equilibrada de sabores y texturas.
>
> • **Selección de ingredientes premium**, elegidos según temporada y calidad del día.
>
> • **Bebidas ilimitadas sin alcohol**, ideal para acompañar la experiencia.
>
> • **1 postre especial del chef**, inspirado en sabores japoneses contemporáneos.
>
> • **Atención personalizada** en un servicio tipo chef's table, donde cada detalle está pensado un entorno íntimo y exclusivo. [sic: "pensado un entorno"]
>
> • **Acceso a un espacio privado** con máximo 4 comensales por sesión, garantizando una experiencia tranquila y sin interrupciones.

Notas de la imagen: lleva iconos (sushi, rábano, botella, postre, chef), fondo con flores de cerezo y tinta sumi, y marco dorado. El "\*\*" antes de "Precio" es literal (parece un resto de Markdown). El logo de la imagen usa una tipografía sans distinta a la de la web. **No dice si el postre es uno de los 14 tiempos o es adicional:** aparece como viñeta aparte.

## 9. Reseñas ("Lo que dicen quienes ya estuvieron")

- Eyebrow: Lo que dicen quienes ya estuvieron [HTML]
- Título: **La barra** / *habla por sí sola* (en escritorio con punto final: "habla por sí sola.") [JSON `social.title.mobile`]
- Cada tarjeta: ★★★★★ + cita + autor + sello "Reseña verificada · Google" (con logo G) [HTML `social.badge`]
- La sección es oscura en los dos temas.

| # | Cita (literal, con comillas rectas) | Autor en vivo (literal) | Autor en el HTML del repo (ya no se ve) |
|---|---|---|---|
| t1 | "Una experiencia espectacular de principio a fin. La chef explica cada pieza con detalle, los ingredientes frescos y cada tiempo perfectamente balanceado. Un omakase auténtico, de calidad y lleno de detalles." | — Lucia Ojeda · Tijuana [JSON] | — Lucia Ojeda · Google |
| t2 | "Me encantó todo — ingredientes frescos, ambiente agradable y la chef muy amigable. Es toda una experiencia ver la preparación de cada platillo. 100% recomendado, definitivamente volvería." | — Angelica Serrano. · San Diego [JSON] (con punto después de "Serrano") | — Angelica Serrano Silva · Google |
| t3 | "Sin duda de la mejor cocina japonesa en Baja. Disfrutamos muchísimo el omakase que reservamos en Morishita. La comida deliciosa y una experiencia que vale cada peso." | — Cyn RM · Mexicali [JSON] | — Cyn RM · Local Guide · Google |

Capturas: `fuente/capturas/resena-t1|t2|t3-{light,dark}.png`, `resenas-*.png`.

## 10. Reservar (CTA de la home)

- Eyebrow: Reserva tu lugar [JSON]
- Título: **Cuatro asientos.** / *Solo dos días por semana.* [JSON `reservar.h2`] · *Antes:* Cuatro asientos. / Dos noches por semana.
- Lead: El menú se construye pieza por pieza el día del servicio. [JSON `reservar.lead`] · *Antes:* …el día del servicio. Por eso pedimos un anticipo del 50% al reservar — se aplica directamente a tu cuenta final, no es un cargo adicional.
- Botón: Ver fechas disponibles → (abre `/?reservar=1`) [HTML]
- Ficha:

| Concepto | Valor | Origen |
|---|---|---|
| Servicio | Sáb · Dom | [JSON label / HTML valor] |
| Capacidad | 4 asientos | [HTML] |
| Tiempos | 14 | [HTML] |
| Precio | $1,850 MXN p/p | [HTML] |
| Anticipo | 50% | [JSON] · *Antes:* 50% Stripe |

Captura limpia: `fuente/capturas/home-reservar-resumen-{light,dark}-limpia.png` (copiada a `assets/fotos/web/captura-reserva-resumen-{claro,oscuro}.png`).

## 11. FAQ ("Antes de reservar")

- Eyebrow: Antes de reservar [HTML]
- Título: **Lo que** / *conviene saber.* [HTML]
- Lead: Si tu pregunta no está aquí, escríbenos por WhatsApp. Respondemos personalmente. [HTML]

| Pregunta [HTML] | Respuesta en vivo | Origen |
|---|---|---|
| ¿Por qué solo abren sábado y domingo? | Trabajamos con producto fresco seleccionado pieza por pieza. Mantener el estándar requiere ciclos de servicio acotados. Dos noches por semana es lo que nos permite no comprometer la calidad. | [HTML `faq.a1`]. Sigue diciendo "noches", aunque los pilares ya dicen "días". |
| ¿El anticipo es reembolsable? | Reembolsable hasta 48 horas antes del servicio. Después de ese momento, el anticipo se aplica al producto que ya separamos para tu sesión. | [JSON `faq.a2`] · *Antes:* 72 horas … para tu mesa. |
| ¿Puedo elegir lo que voy a comer? | No hay carta. El menú lo construye el chef según el mejor producto del día. Si tienes alergias o restricciones, indícalas al reservar y se adapta el menú sin sacrificar la experiencia. | [HTML `faq.a3`] |
| ¿Cuánto dura la cena? | Aproximadamente dos horas. Cada uno de los 14 tiempos se prepara a la vista y se sirve en su momento. Es una experiencia para disfrutar sin prisa. | [HTML `faq.a4`] |
| ¿Hay código de vestimenta? | No hay código formal. Sugerimos vestir cómodo pero cuidado. La barra es íntima — vístete como te vestirías para una cena que importa. | [HTML `faq.a5`] |
| ¿Incluye bebidas? | Si, tu sesión de 14 tiempos incluye bebidas sin alcohol ilimitadas. [sic: "Si" sin tilde] | [JSON `faq.a6`] · *Antes:* El precio del Omakase es solo el menú de 14 tiempos. Bebidas (sake, vino de Valle, agua, etc.) se cobran aparte. Te recomendamos el sake del chef. |

## 12. Flujo de reserva (`/?reservar=1`) [HTML + JS, sin override]

Barra de progreso: 1 Comensales · 2 Fecha · 3 Horario · 4 Reservar, con un contador "8:00 restantes". El contador **solo existe en el navegador**: al expirar sale "El tiempo para completar tu reservación expiró. Tu lugar ha sido liberado.", pero el backend no aparta lugares mientras corre.

1. **Comensales:** "Paso 01 · Comensales" · **¿Cuántos asientos este día?** · *Máximo 4 personas por servicio.* · "Número de comensales" con − 2 + (2 por defecto). Pistas: "2 personas. Te mostramos las fechas con lugar disponible." / con 1: "Mesa para una persona." / con 4: "Mesa completa · toda la barra para tu grupo." · Botones: "← Volver" · "Ver fechas disponibles →".
2. **Fecha:** "Paso 02 · Elige una fecha" · calendario mensual (Dom–Sáb), leyenda: Disponible · Lleno · Cerrado. Solo se pueden elegir sábados y domingos.
3. **Horario:** "Paso 03 · Horario" · **Elige tu servicio.** · *Mostramos solo los horarios con lugares para tu grupo.* Tarjetas:
   - **1:00 pm** · COMIDA TEMPRANA
   - **3:30 pm** · SOBREMESA
   - **6:00 pm** · CENA OMAKASE
   - Cada una con 4 puntos y "N de 4 disponibles". Sin cupo: "Lleno / Sin cupo". Con 1 o 2 lugares sale la insignia "Últimos lugares" (automática, con datos reales).
4. **Reservar (checkout):** "Paso 04 · Reservar" · **Completa tu reserva.** · Contador "10:00 para completar · si expira se libera tu lugar" · Formulario "Tus datos": por comensal, "Nombre completo *" y "Alergias / restricciones (opcional)" (ejemplo: "Mariscos, gluten, lactosa…"); "WhatsApp *", "Email *", "Motivo (opcional)" (ejemplo: "Aniversario, cumpleaños…") · Resumen: "Omakase · 14 tiempos", Fecha, Horario, Comensales, "Por persona $1,850", "Total experiencia", "Anticipo hoy · 50% · Vía Stripe", "El 50% restante … se paga en el restaurante después del servicio." · Botón "Pagar anticipo →". El pago es con tarjeta en Stripe Checkout.
5. **Confirmación:** sello "森" · "Reservación confirmada" · **Te esperamos en Morishita 🍣** · "Hemos recibido tu anticipo. Recibirás confirmación por email y WhatsApp en breve." · Detalles: Fecha, Horario, Comensales, Menú "Omakase · 14 tiempos", Anticipo pagado, Saldo en restaurante, Referencia · "Hacer otra reservación →".

Capturas (sin completar nada): `fuente/capturas/reserva-1-comensales-*`, `reserva-2-fechas-*`, `reserva-2-calendario-*-recorte`, `reserva-3-horarios-*`.

## 13. Footer

- Marca: 森下 Morishita / Authentic Japanese Cuisine [HTML]
- Descripción: 1 barra de 4 asientos. 14 tiempos. Pescado y mariscos de temporada. Carne Wagyu A5 importada de Japón. [JSON `footer.desc`] · *Antes:* Una barra de cuatro asientos. Catorce tiempos. Wagyu A5, Kobe importado de Japón y pescado de temporada. Sábados y domingos en Baja California.
- **Visítanos:** Ensenada, Baja California, México [JSON `footer.location`] · Sáb · Dom [HTML] · Servicio por reservación [HTML]
- **Contacto:**
  - WhatsApp → `https://wa.me/+526462454294` [JSON `footer.whatsapp_url`]
  - Instagram → `https://instagram.com/morishita.japanesecuisine` [JSON] · *Antes:* `instagram.com/morishitajapanesecuisine`
  - Email → `mailto:reservas@morishitajapanesecuisine.com` [HTML]
- **Reservar:** Ver disponibilidad · La experiencia · El producto · Preguntas frecuentes [HTML]
- Pie: © 2026 森下 Morishita · Authentic Japanese Cuisine [HTML] · Pagos seguros · SSL [JSON] · *Antes:* Pagos seguros vía Stripe · SSL

## 14. Imágenes en vivo → archivo local (verificado por hash MD5)

| Clave | Sección | Archivo local (`assets/fotos/web/`) |
|---|---|---|
| `img.hero` | Hero | `hero-comensales-generated.jpg` (**IA**, "Generated_Image") |
| `img.chef` | Chef | `vero_v2.jpg` |
| `custom.csmowqknu37iw.image` | Omakase Experience | `vero_v3.jpg` |
| `custom.csmot6cqlyzxu.image` | Morishita Meat | `WAGYU_FRAN_VF3.jpg` |
| `img.wagyu` | Producto (principal) | `wagyu-hero.jpg` |
| `img.pescado` | Producto · Pescado | `producto-pescado-v2-live.jpg` |
| `img.base` | Producto · Base | `producto-base.jpg` |
| `img.carne` | Producto · Carne | `producto-carne.jpg` |
| `custom.csmowt1n3juvx.image` | Menú 14 tiempos | `menu_14_tiempos-mjc.jpg` |
| (no se ven en vivo) | repo `/img/` | `hero-bar.jpg`, `chef-morishita.jpg`, `producto-pescado.jpg` |

## 15. Erratas visibles en la web en vivo (para que el dueño las corrija; en los reels se escriben bien)

- "Confia en el chef" → **Confía** (hero).
- "¿Como funciona la expericia Omakase?" → **¿Cómo** … **experiencia**.
- "degustaras", "viviras" → **degustarás**, **vivirás**.
- "junto la carne más exclusiva" → **junto con** la carne…
- "Kobe autentico" → **auténtico**; dobles espacios y " , " en el párrafo de Morishita Meat; le falta el punto final.
- "Carne Wagyu A5 certificada, importadas" → **importada**.
- "Si, tu sesión…" → **Sí**.
- "Angelica Serrano." (punto suelto en el autor).
- Imagen del menú: "QUISINE" → **CUISINE**; "\*\*Precio"; "pensado un entorno" → **pensado en un entorno**.
- Escritorio: eyebrow "ETIQUETA" (relleno de plantilla) en la sección del menú, y firma "Chef Morishita" que no coincide con el título "Chef Vero Morishita".
- Botones "Saber más" con URL `#` (menú) o `#/?reservar=1` (Omakase Experience en móvil).

## 16. Nota de privacidad (fuera del alcance de los reels, pero conviene saberlo)

`GET /api/content` es público y además del contenido de la web devuelve `evaluacion_miyagi_respuestas` y `evaluacion_miyagi_session__alfonso_varela`: calificaciones y comentarios internos de platillos, con el nombre de un evaluador. No se copiaron aquí. Se recomienda sacarlos de ese endpoint público.
