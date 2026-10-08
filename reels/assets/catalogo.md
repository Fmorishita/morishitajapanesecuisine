# Catálogo de assets visuales · Morishita (森下)

> Revisado el 2026-10-08, imagen por imagen: abrí cada archivo, revisé las cuatro esquinas, hice recortes de detalle y leí los bytes de la imagen. Nada se catalogó por el nombre del archivo.
> Carpeta revisada: `assets/fotos/web/`, con 20 archivos: 11 fotos o gráficos de la web y 9 capturas del flujo de reserva. **No hay videos.**
> Recortes 9:16 listos para editar: `assets/recortes/` (37 JPG de 1080x1920). Hoja de contacto: `assets/recortes/_contacto.jpg`.
> Tomas que faltan para el próximo servicio: `assets/lista-de-tomas.md`.

## 0. Lo accionable primero

1. **De la web no hay ni una foto de comida, de barra, de chef ni de comensales que sea real y esté verificada.** Lo único 100 % real son las **capturas del flujo de reserva** (UI de la web en vivo).
2. **Seis imágenes del repo son IA confirmada por metadatos.** Sus originales en git (commit `6fa0762`, 2026-05-01, "Add high-res brand imagery…") traen un manifiesto **C2PA firmado por Google** con estos datos: `c2pa.created` → "Created by Google Generative AI", `digitalSourceType` → `http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia` y `c2pa.edited` → "Applied imperceptible SynthID watermark". Son `chef-morishita`, `hero-bar`, `producto-base`, `producto-carne`, `producto-pescado` y `wagyu-hero`. El commit `c2d95bf` ("Optimize images") recomprimió los archivos y les quitó esos metadatos. Por eso las copias actuales parecen limpias.
3. **Tres imágenes llevan la marca ✦ de Gemini a la vista:** `hero-comensales-generated` (además, en el servidor se llama `Generated_Image_May_02__2026_-_1_54AM.jpg`), `vero_v2` y `vero_v3`. La escena de `vero_v3` es idéntica a la de `chef-morishita`, que es IA confirmada: misma lámpara, puerta, barra, platos apilados y toalla. Es decir, a la Chef Vero la pusieron en una escena generada.
4. Las imágenes que sirve el servidor (Supabase `site-images`) son idénticas byte por byte a las de `assets/fotos/web/` (md5 verificado) y **no traen metadatos**: el panel de admin los quita al subirlas. Por eso `producto-pescado-v2-live` y `WAGYU_FRAN_VF3` quedan como "posible IA". No se puede probar en ninguno de los dos sentidos.
5. Consecuencia para este lote (reels sin wagyu). La regla de CLAUDE.md dice: "solo material real; la IA no genera platos, interiores ni al chef". Con esa regla, **solo las capturas de reserva son usables sin condiciones.** Las fotos de producto y de la chef quedan como **"condicional"**: se usan solo si tú (dueño) lo apruebas y con el rótulo en pantalla "Imagen ilustrativa generada con IA". La mejor salida es grabar este fin de semana (ver `lista-de-tomas.md`).
6. Las personas de `hero-comensales-generated.jpg` no existen y `chef-morishita.jpg` no es la Chef Vero. Esas dos **no se usan nunca**. Wagyu y Kobe (`wagyu-hero`, `producto-carne`, `WAGYU_FRAN_VF3`) **quedan fuera de este lote**.

Cómo reproducir la prueba de IA:
`git show 6fa0762:img/hero-bar.jpg | grep -a -c trainedAlgorithmicMedia` → mayor que 0 (lo mismo con los otros 5).

## 1. Tabla de assets

Leyenda de autenticidad:
- **REAL**: captura propia de la web en vivo.
- **IA CONFIRMADA**: C2PA de Google o ✦ de Gemini, con la evidencia anotada.
- **POSIBLE IA**: indicios visuales, sin prueba en metadatos.

Leyenda de uso en el lote:
- **SÍ**: se puede usar.
- **CONDICIONAL**: solo con tu aprobación y el rótulo "Imagen ilustrativa (IA)". Nunca decir "así es nuestra barra" ni "este es nuestro pescado de hoy".
- **NO**: no se usa.

Las cajas de recorte están en px de la fuente: (x0,y0)–(x1,y1).

| Archivo | Qué se ve (producto · técnica · momento) | Encuadre | Resolución | Calidad | ¿Gancho? | Vertical / recorte 9:16 | Autenticidad (evidencia) | ¿Usable en este lote? | Notas |
|---|---|---|---|---|---|---|---|---|---|
| `producto-pescado-v2-live.jpg` | Caja de madera clara con la selección de pescado sobre papel y hojas de shiso. Trae atún en 3 cortes (akami, chutoro, otoro), salmón, pescado blanco, calamar, pulpo cocido, 2 camarones enteros, katsuo tataki (piel sellada) y un cuenco de negitoro. Arriba a la derecha hay **raíz de wasabi fresco con rallador metálico**. Momento: producto del día / sashimi. | Cenital, cuadrado, fondo de pizarra negra | 1920x1920 | Alta: nítida, color vivo, acabado algo "de render" | **Sí**: la variedad y el color en un cuadro ("lo que llegó esta semana"); el wasabi fresco funciona como detalle de golpe | Cuadrada. 9:16 central (420,0)–(1500,1920), 1080 px de ancho, escala 1:1 | **POSIBLE IA**. Sin metadatos (el servidor los quitó). Texto ilegible en el rallador, antenas y patas de los camarones fundidas, ventosas del pulpo anómalas. Mismo estilo que las 6 con C2PA. | CONDICIONAL. Sin wagyu ✓ | Es la foto "Pescado" de la web en vivo (servidor: `1777695942315-producto-pescado.jpg`). **Confirmar qué especies sirven de verdad** (salmón, camarón, pulpo) antes de nombrarlas. |
| `vero_v3.jpg` | **Chef Vero** con filipina negra y lentes, cortando un bloque de **atún rojo** con cuchillo largo sobre tabla de madera clara. Hay otro cuchillo sobre la tabla, toalla blanca enrollada, platitos de soya y gari, plato negro, lámpara colgante y la barra al fondo. Momento: chef cortando. | Plano medio frontal 3:4, con **marco negro de ~46 px** | 1792x2390 | Alta | **Sí**: manos, cuchillo y pescado; cara concentrada | Casi vertical. 9:16 (300,46)–(1591,2342), dentro del marco y sin la ✦ | **IA CONFIRMADA (escena)**. ✦ de Gemini abajo a la derecha (~x1640–1720, y2235–2325). La escena es idéntica a `chef-morishita.jpg` (IA con C2PA). La cara es de Vero; el lugar no es el restaurante. | CONDICIONAL. Es la chef real en un entorno falso: no decir "nuestra barra". | Es "Omakase Experience" en vivo. Recortar siempre el marco y la ✦. |
| `hero-bar.jpg` | Barra de madera clara en **terraza de noche**, lámpara colgante encendida, cielo con estrellas, **skyline de rascacielos** con luces rojas, barandal de troncos y plantas. Una mano de chef (manga blanca) forma un nigiri junto a un cuchillo. En primer plano hay un nigiri desenfocado en plato plateado. Momento: llegada/barra y nigiri. | Vertical 4:5, en el eje de la barra, profundidad de campo | 928x1152 | Media: 928 px y artefactos JPEG en el cielo | **Sí**: atmósfera nocturna, "la barra te espera" | 9:16 (140,0)–(788,1152), 648 px → apenas sobre el límite | **IA CONFIRMADA**: C2PA de Google en el original git (928x1152). Además, ese skyline **no es Ensenada**. | CONDICIONAL. Nunca presentarla como el lugar real. | No está en la web en vivo (solo en el repo `/img/`). |
| `producto-pescado.jpg` | Sashimi de **otoro** (ventresca de atún, vetas de grasa) sobre rodaja de daikon, hoja de shiso, montículo de wasabi rallado, plato celadón craquelado y fondo de piedra gris. Momento: sashimi. | 3/4 (≈45°), cuadrado, desenfoque suave | 1600x1600 (original git 2048x2048) | Alta, limpia, elegante | Medio: bonita pero calmada; sirve más para el "respiro" del plato estrella | 9:16 (390,0)–(1290,1600), 900 px | **IA CONFIRMADA**: C2PA de Google en el original git. | CONDICIONAL | No está en vivo. |
| `producto-base.jpg` | **Nigiri** de pescado blanco con marcas de soplete (aburi) y brillo de nikiri. El **arroz es color ámbar** (vinagre añejado) y va sobre tabla de madera oscura. Macro. Momento: nigiri / arroz. | Macro lateral bajo, desenfoque fuerte | 1024x1024 | Buena a tamaño completo. **A más de 2x los granos se ven cerosos y deformes, como larvas.** | **Sí**: textura de grano ("la base que la mayoría descuida") | 9:16 (352,0)–(928,1024), 576 px → **baja res** | **IA CONFIRMADA**: C2PA de Google en el original git. | CONDICIONAL. No hacer zoom de más de 2x. | Es "Base · Arroz, vinagre, dashi" en vivo (servida desde el repo). |
| `vero_v2.jpg` | **Chef Vero**, retrato de medio cuerpo con brazos cruzados y sonrisa, lentes y filipina negra con logo **森下 MORISHITA · AUTHENTIC JAPANESE CUISINE**. Al fondo: muro de estuco con luz cálida, panel de madera, rama de cerezo, cuchillos en barra magnética, botella ámbar y mortero de piedra. Momento: presentación de la chef. | Retrato vertical 3:4 | 896x1193 | Media (baja res para recortes) | Medio: cara humana, confianza; no es acción | 9:16 (100,0)–(771,1193), 671 px. **Mantener x ≤ 800** para no meter la ✦. | **IA CONFIRMADA (al menos edición)**. ✦ de Gemini (~x815–865, y1110–1160). El logo es plano (no parece bordado) y los cuchillos "flotan". Cara real probable; el entorno puede ser generado. | CONDICIONAL. Es la chef real; mejor reemplazar con un retrato real (toma 3 de la lista). | Es "Chef" en vivo. |
| `captura-reserva-resumen-oscuro.png` | Bloque "RESERVA TU LUGAR". Titular "**Cuatro asientos.** *Solo dos días por semana.*" y debajo "El menú se construye pieza por pieza el día del servicio.", botón dorado "VER FECHAS DISPONIBLES →". Tabla: Servicio Sáb · Dom / Capacidad 4 asientos / Tiempos 14 / Precio $1,850 MXN p/p / Anticipo 50%. Momento: reserva. | Pantalla móvil, fondo negro | 1082x1877 | Alta (texto nítido) | No como imagen inicial; **sí como texto del gancho** ("Cuatro asientos.") recreado en grande | 9:16 (13,0)–(1069,1877) o por bloques (ver recortes) | **REAL**: captura de la web en vivo del 2026-10-08 | **SÍ** (CTA y prueba de datos) | Si sale el precio, agregar "bebidas sin alcohol ilimitadas incluidas" (hechos A3/B4). |
| `captura-reserva-resumen-claro.png` | Lo mismo en tema claro (crema #faf8f4, acentos rosa) | Pantalla móvil | 1082x1877 | Alta | Ídem | Ídem | **REAL** | **SÍ** | Combina con el fondo crema de la marca. |
| `captura-reserva-fechas-oscuro.png` | Paso 02 "ELIGE UNA FECHA". Calendario de **octubre 2026** con sábados y domingos marcados disponibles (10, 17, 18, 24, 25, 31); el 11 sale sin lugar. Abajo: "VISÍTANOS · ENSENADA, BAJA CALIFORNIA, MÉXICO". Barra de pasos con 50 % y temporizador "7:52 RESTANTES". | Pantalla móvil | 1082x2402 | Alta | No | 9:16 (0,300)–(1082,2224) o el recorte `calendario` (41,380)–(1041,2158), **sin el temporizador** | **REAL** (2026-10-08) | **SÍ** | La disponibilidad cambia: **volver a capturar el día que se publique** y no decir "quedan X" sin tu confirmación. **No mostrar el temporizador** (hechos B15: no es escasez real). |
| `captura-reserva-fechas-claro.png` | Ídem en tema claro | Pantalla móvil | 1082x2402 | Alta | No | Ídem | **REAL** | **SÍ** | Ídem |
| `captura-reserva-horarios-oscuro.png` | Paso 03 "**Elige tu servicio.**" con chip "SÁBADO 10 DE OCTUBRE · 2P · HORARIO". Opciones: **1:00 pm** comida temprana (4 de 4 disponibles), **3:30 pm** sobremesa (4 de 4 disponibles) y 6:00 pm (cortado abajo). | Pantalla móvil | 1082x2402 | Alta | No | 9:16 recorte `horarios` (41,611)–(1041,2389) | **REAL** (2026-10-08) | **SÍ**, pero los horarios todavía **no se citan** (hechos D2) | Sirve de "prueba de que reservar es fácil". |
| `captura-reserva-comensales-oscuro.png` | Paso 01 "¿Cuántos asientos este día?" con la línea "*Máximo 4 personas por servicio.*", contador "2" con botones − / + y botón dorado "VER FECHAS DISPONIBLES →". Temporizador 7:57 arriba. | Pantalla móvil | 1082x2402 | Alta | No; apoya "solo 4 personas" | 9:16 (0,380)–(1082,2304), **sin el temporizador** | **REAL** | **SÍ** | Prueba visual real de "máximo 4". |
| `captura-reserva-comensales-claro.png` | Ídem en tema claro (rosa/negro) | Pantalla móvil | 1082x2402 | Alta | No | Ídem | **REAL** | **SÍ** | — |
| `captura-reserva-calendario-oscuro.png` | Solo la tarjeta del calendario de octubre 2026 (sin pasos ni temporizador), con leyenda Disponible / Lleno / Cerrado | Horizontal casi cuadrada | 935x1055 | Alta | No | **No cabe en 9:16 sin cortar los sábados**: usarla como tarjeta sobre fondo (letterbox) o dentro de un mockup de teléfono | **REAL** | **SÍ** | Ideal como overlay animado en el CTA. |
| `menu_14_tiempos-mjc.jpg` | **Gráfico** (no es foto): logo 森下 MORISHITA, cerezos, tinta sumi y marco dorado. Texto: precio $1,850 MXN, 14 tiempos en formato degustación, ingredientes premium, bebidas ilimitadas sin alcohol, 1 postre especial del chef, chef's table, máximo 4 comensales. | Vertical ≈9:16 | 1206x2143 | Baja-media: texto suave, parece captura reescalada | No | Ya es ≈9:16: (0,0)–(1206,2143) | Diseño del negocio; es real como documento | **Solo como referencia de datos**: no mostrar en pantalla | Erratas: "QUISINE", "\*\*Precio", "pensado un entorno". Retipografiar los datos con la marca. |
| `chef-morishita.jpg` | Mujer de **cabello canoso, que no es la Chef Vero**, con filipina blanca estilo japonés, cortando un pescado de piel plateada. Misma escena que `vero_v3` (lámpara, barra, platos). | Plano medio 3/4 | 1600x1986 (original 1856x2304) | Alta | Lo sería, pero no aplica | 9:16 (380,0)–(1497,1986) | **IA CONFIRMADA**: C2PA de Google en el original git. Además, al cortar, los dedos quedan sobre el filo. | **NO**: no es la chef y es IA | Nunca presentarla como la chef. |
| `hero-comensales-generated.jpg` | **4 comensales (2 parejas) que no existen**, riendo en una mesa larga con nigiri, sashimi, edamame, tokkuri de sake, jugos, velas y piñas. Techo de lona y celosía de madera. | Vertical 9:16 nativo | 1536x2752 | Alta | Lo sería (risas), pero es engañoso | Ya es 9:16; la ✦ queda adentro | **IA CONFIRMADA**: ✦ de Gemini (~x1380–1475, y2595–2690) y nombre en el servidor "Generated_Image_May_02__2026". | **NO**: clientes falsos = publicidad engañosa. Además es mesa (no barra de 4) y sale sake. | Es el **hero en vivo** de la web. Riesgo de la web, fuera del alcance de los reels: ver hechos D13. |
| `WAGYU_FRAN_VF3.jpg` | **Fran Morishita** (fundador) detrás de una barra de granito con 4 cortes de wagyu empacados al vacío, caja "有田牛 ARITA WAGYU", trofeo dorado con cabeza de res y certificado. Texto añadido "**Wagyu A5 & Kobe Beef 100% Certified**" con flecha dorada y fondo de shoji. | Vertical 3:4 | 1792x2390 | Alta, con retoque fuerte | Sí, pero excluido | 9:16 (224,0)–(1568,2390) | **Fotomontaje**: texto y flecha añadidos. Tiene las mismas dimensiones que `vero_v3` (posible paso por Gemini); sin ✦ a la vista. Persona real probable. | **NO** (wagyu y Kobe como protagonistas) | Sección "Morishita Meat". "Arita Wagyu" no es Kobe: revisar el respaldo de "Kobe" (CLAUDE.md, cuidados). |
| `wagyu-hero.jpg` | Corte crudo de **wagyu** con marmoleo extremo, hoja de shiso, sal en hojuelas y humo sobre pizarra negra | Vertical 4:5 | 1600x1986 (original 1856x2304) | Alta | Sí, pero excluido | 9:16 (350,0)–(1467,1986) | **IA CONFIRMADA** (C2PA) | **NO** (wagyu) | En vivo como "Producto principal" con la etiqueta "Wagyu A5 · Origen Japón · Certificado". |
| `producto-carne.jpg` | **Nigiri de wagyu** sellado, con wasabi y hoja de oro, en plato negro | 3/4, cuadrado | 1600x1600 (original 2048x2048) | Alta | Sí, pero excluido | 9:16 (450,0)–(1350,1600) | **IA CONFIRMADA** (C2PA) | **NO** (wagyu) | En vivo como "Carne · Nigiri de Wagyu A5". |

Detalle técnico común:
- Todos los JPG comparten la misma tabla de cuantización (≈ calidad 80): los recomprimió el mismo proceso (la optimización del repo o el panel de admin).
- No tienen EXIF de cámara. Ninguno trae marca de teléfono o cámara.
- Las capturas PNG no tienen metadatos.

## 2. Ranking para un reel sin wagyu (de más a menos fuerza visual)

| # | Archivo | Mejores tomas | Uso | Autenticidad |
|---|---|---|---|---|
| 1 | `producto-pescado-v2-live.jpg` | caja-cenital, atun-tres-cortes, wasabi-rallador | CONDICIONAL | POSIBLE IA |
| 2 | `vero_v3.jpg` | manos-cortando, filo-atun, rostro-concentrada | CONDICIONAL | IA CONFIRMADA (escena; cara real) |
| 3 | `hero-bar.jpg` | barra-completa, lampara-noche | CONDICIONAL | IA CONFIRMADA (y skyline que no es Ensenada) |
| 4 | `producto-pescado.jpg` | otoro-vetas, shiso, wasabi-rallado | CONDICIONAL | IA CONFIRMADA |
| 5 | `producto-base.jpg` | nigiri-completo (no pasar de 2x) | CONDICIONAL | IA CONFIRMADA |
| 6 | `vero_v2.jpg` | retrato, logo-filipina | CONDICIONAL | IA CONFIRMADA (edición; cara real) |
| 7 | `captura-reserva-resumen-oscuro.png` / `-claro` | titular, tabla-datos | **SÍ** | REAL |
| 8 | `captura-reserva-fechas-*`, `-horarios-oscuro`, `-comensales-*`, `-calendario-oscuro` | calendario, horarios, maximo-4, contador | **SÍ** | REAL |
| — | `menu_14_tiempos-mjc.jpg` | — (retipografiar) | Solo referencia | Documento real con erratas |

Si solo cuenta lo real verificado, el orden es: 7 → 8. Con eso no alcanza para la parte de "Experiencia" (3–20 s): hay que grabar o aprobar el rótulo IA.

## 3. Tomas de detalle (recortes 9:16 ya generados)

Todas están en `assets/recortes/<archivo>__<toma>.jpg`, en 1080x1920 y escaladas con LANCZOS.
- **baja res**: el recorte en la fuente mide menos de 600 px de ancho. Úsalas como plano corto (≤ 0.8 s) o detrás de texto, nunca como plano largo.
- **pad**: región exacta de la UI, escalada y centrada sobre el color de fondo del propio screenshot.

| Recorte | Caja en la fuente (px) | Ancho fuente → escala | Qué muestra (verificado en la hoja de contacto) | Uso sugerido |
|---|---|---|---|---|
| `producto-pescado-v2-live__caja-cenital` | (420,0)–(1500,1920) | 1080 → 1.0x | Centro de la caja: negitoro, salmón, pescado blanco, atún, pulpo, katsuo | Plano general / gancho |
| `producto-pescado-v2-live__atun-tres-cortes` | (310,249)–(930,1351) | 620 → 1.74x | Akami, chutoro y otoro en escalera sobre shiso | "Un mismo pez, tres cortes" |
| `producto-pescado-v2-live__otoro-y-katsuo` | (340,717)–(940,1784) | 600 → 1.8x | Akami, otoro marmoleado y katsuo tataki con piel sellada | Corte rápido de textura |
| `producto-pescado-v2-live__wasabi-rallador` | (1210,4)–(1690,857) | 480 → 2.25x **baja res** | Raíz de wasabi fresco, rallador metálico y salmón | Detalle artesanal (0.6–0.8 s). Ojo: texto ilegible en el rallador. |
| `producto-pescado-v2-live__camaron-y-calamar` | (1170,847)–(1770,1914) | 600 → 1.8x | 2 camarones enteros, calamar, shiso | Corte de variedad (confirmar que se sirven) |
| `producto-pescado-v2-live__pescado-blanco` | (690,399)–(1310,1501) | 620 → 1.74x | Pescado blanco en láminas, cuenco de negitoro y salmón | Corte de variedad |
| `producto-pescado__plato-completo` | (390,0)–(1290,1600) | 900 → 1.2x | Plato celadón con otoro, daikon, shiso y wasabi | Respiro del plato estrella |
| `producto-pescado__otoro-vetas` | (630,261)–(1270,1399) | 640 → 1.69x | Otoro con vetas de grasa sobre daikon | Punch-in de textura |
| `producto-pescado__shiso` | (940,87)–(1540,1154) | 600 → 1.8x | Hoja de shiso dentada con el borde del otoro | Plano de transición verde |
| `producto-pescado__wasabi-rallado` | (1000,533)–(1600,1600) | 600 → 1.8x | Montículo de wasabi rallado, daikon y plato craquelado | Detalle |
| `producto-base__nigiri-completo` | (352,0)–(928,1024) | 576 → 1.88x **baja res** | Nigiri entero: neta con aburi y arroz ámbar | "El arroz" (la mejor de esta foto) |
| `producto-base__arroz-granos` | (470,214)–(770,747) | 300 → 3.6x **baja res** | Granos de shari en macro | **No recomendado**: a 3.6x los granos parecen larvas. Solo flash de 0.3 s o descartar. |
| `producto-base__neta-aburi` | (610,0)–(910,533) | 300 → 3.6x **baja res** | Superficie del pescado con marcas de soplete y brillo de nikiri, arroz abajo | Flash de 0.4 s |
| `producto-base__tabla-madera` | (40,209)–(480,991) | 440 → 2.45x **baja res** | Borde de la tabla de madera oscura y orilla del nigiri | Transición / fondo de texto |
| `hero-bar__barra-completa` | (140,0)–(788,1152) | 648 → 1.67x | Barra en perspectiva, lámpara, ciudad, mano formando nigiri, plato al frente | Ambiente (no decir que es el lugar) |
| `hero-bar__lampara-noche` | (260,0)–(660,711) | 400 → 2.7x **baja res** | Lámpara encendida, cielo con estrellas, barandal | Fondo para el texto del gancho |
| `hero-bar__manos-nigiri` | (0,357)–(420,1104) | 420 → 2.57x **baja res** | Manos formando nigiri, cuchillo y plato desenfocado | Corte rápido |
| `hero-bar__luces-ciudad` | (0,154)–(300,687) | 300 → 3.6x **baja res** | Luces de la ciudad (rascacielos) y barandal | **Ojo**: el skyline no es Ensenada; solo como bokeh abstracto |
| `vero_v2__retrato` | (150,126)–(750,1193) | 600 → 1.8x | Chef Vero de brazos cruzados, sonriendo, logo en la filipina | "Quién cocina" |
| `vero_v2__rostro-sonrisa` | (270,100)–(630,740) | 360 → 3.0x **baja res** | Cara de Vero con lentes, sonrisa | Punch-in (≤ 0.8 s) |
| `vero_v2__logo-filipina` | (390,464)–(690,997) | 300 → 3.6x **baja res** | Logo 森下 MORISHITA en la filipina | Firma de marca (0.5 s) |
| `vero_v2__cuchillos-cerezo` | (624,340)–(896,824) | 272 → 3.97x **baja res** | Cuchillos en barra magnética, rama de cerezo, botella ámbar | Transición (0.4 s); se ve suave |
| `vero_v3__plano-medio-chef` | (360,400)–(1440,2320) | 1080 → 1.0x | Vero cortando atún en la tabla, con lámpara | Plano de establecimiento de la chef |
| `vero_v3__manos-cortando` | (600,1200)–(1240,2338) | 640 → 1.69x | Manos de Vero, cuchillo entrando al atún, soya | Momento técnica (gancho alterno) |
| `vero_v3__filo-atun` | (680,1445)–(1080,2156) | 400 → 2.7x **baja res** | Filo del cuchillo dentro del bloque de atún | Punch-in sobre el corte |
| `vero_v3__rostro-concentrada` | (630,167)–(1230,1234) | 600 → 1.8x | Cara concentrada mirando el corte | Corte de emoción |
| `vero_v3__lampara` | (150,46)–(630,899) | 480 → 2.25x **baja res** | Lámpara colgante cálida sobre muro | Fondo de texto / transición |
| `vero_v3__soya-y-gari` | (1060,1489)–(1540,2342) | 480 → 2.25x **baja res** | Platitos de soya y gari sobre la tabla | Detalle de mesa |
| `captura-reserva-resumen-oscuro__pantalla` | (13,0)–(1069,1877) | 1056 → 1.02x | Pantalla completa "Cuatro asientos. Solo dos días por semana." con tabla | CTA |
| `captura-reserva-resumen-oscuro__tabla-datos` | pad (152,760)–(930,1740) | 778 → 1.39x | Botón dorado y tabla Sáb·Dom / 4 asientos / 14 / $1,850 MXN p/p / 50% | Prueba de datos |
| `captura-reserva-resumen-oscuro__titular` | pad (100,190)–(985,640) | 885 → 1.22x | "Reserva tu lugar · Cuatro asientos. Solo dos días por semana." | Texto del gancho o del cierre |
| `captura-reserva-resumen-claro__pantalla` | (13,0)–(1069,1877) | 1056 → 1.02x | Versión crema/rosa | CTA en tema claro |
| `captura-reserva-comensales-oscuro__maximo-4` | (41,600)–(1041,2378) | 1000 → 1.08x | "¿Cuántos asientos este día? Máximo 4 personas por servicio." con contador y botón (sin temporizador) | "Solo 4 personas" con prueba real |
| `captura-reserva-comensales-oscuro__contador` | pad (74,1116)–(1007,2004) | 933 → 1.16x | Contador "2" con − / + | Animación de "elige cuántos" |
| `captura-reserva-fechas-oscuro__calendario` | (41,380)–(1041,2158) | 1000 → 1.08x | Paso 02 y calendario de octubre 2026 con sábados y domingos disponibles | CTA (recapturar el día de publicación) |
| `captura-reserva-fechas-claro__calendario` | (41,380)–(1041,2158) | 1000 → 1.08x | Ídem en tema claro | CTA |
| `captura-reserva-horarios-oscuro__horarios` | (41,611)–(1041,2389) | 1000 → 1.08x | "Elige tu servicio." 1:00 pm / 3:30 pm / 6:00 pm, 4 de 4 disponibles | Paso de reserva (no citar los horarios hasta D2) |

Sin recortes, a propósito: `chef-morishita`, `hero-comensales-generated`, `WAGYU_FRAN_VF3`, `wagyu-hero` y `producto-carne` (no usables), `menu_14_tiempos-mjc` (retipografiar) y `captura-reserva-calendario-oscuro` (ya es un recorte; usarla como tarjeta).

## 4. Cobertura por momento del omakase

| Momento | Material actual | Estado |
|---|---|---|
| Llegada / barra de 4 lugares | `hero-bar` (IA, otra ciudad) | **FALTA real** |
| Chef cortando | `vero_v3` (escena IA), `chef-morishita` (IA, no es Vero) | **FALTA real** |
| Nigiri (formado y entrega) | `producto-base` (IA), `hero-bar` (IA, desenfocado) | **FALTA real** |
| Sashimi / pescado de temporada | `producto-pescado-v2-live` (posible IA), `producto-pescado` (IA) | **FALTA real** |
| Arroz (shari, vinagre) | `producto-base` (IA, baja res) | **FALTA real** |
| Soplete / aburi (fuego sin wagyu) | Nada (solo marcas de soplete en una imagen IA) | **FALTA** |
| Platillo caliente (dashi, sopa) | Nada | **FALTA** |
| Postre especial del chef | Nada | **FALTA** |
| Bebidas sin alcohol ilimitadas | Nada (solo jugos y sake en la imagen IA de comensales) | **FALTA** |
| Comensales reales (reacción, risas) | Nada (`hero-comensales` es IA) | **FALTA** (con permiso firmado) |
| Chef Vero (cara, voz, explicando) | `vero_v2` y `vero_v3` (cara real en edición/escena IA) | **FALTA real** |
| Reserva (flujo, calendario, 4 lugares) | 9 capturas reales | **CUBIERTO**. Falta una grabación de pantalla en video del flujo (se puede hacer ya). |
| Datos (precio, 14 tiempos, máximo 4) | Capturas reales y gráfico del menú | **CUBIERTO** (retipografiar) |

Otras fuentes de material real que hay que pedir (sin scrapear nada):
1. Fotos y videos del celular del equipo o de los posts propios de Instagram @morishita.japanesecuisine: que el dueño **envíe los archivos originales**.
2. Las fotos por platillo de la **hoja de evaluación** (`evaluacion/`, commit `a636824`: "Foto obligatoria por platillo (cámara nativa en móvil), guardadas en la BD"). Están detrás del PIN de admin, así que no entré. Si son de platillos reales del menú, el dueño puede exportarlas y serían el primer material real de comida.
3. Una grabación de pantalla del flujo `?reservar=1` en un teléfono: es material real y se puede producir sin grabar en el restaurante.

## 5. Reglas de uso de este catálogo

- Sin tu "sí" explícito, ninguna imagen marcada CONDICIONAL entra a un reel. Si das el sí, lleva el rótulo "Imagen ilustrativa generada con IA" (pequeño, dentro del área útil, todo el tiempo que esté en pantalla) y la voz no dice "nuestro" ni "hoy" sobre esa imagen.
- Nunca entran: `chef-morishita` (no es la chef), `hero-comensales-generated` (clientes falsos) ni wagyu/Kobe en este lote.
- Capturas: no mostrar el temporizador "RESTANTES" (no es escasez real, hechos B15). Recapturar el calendario el día de publicación.
- Al reemplazar una foto IA por una real, actualizar esta tabla y marcar la vieja como "retirada".
