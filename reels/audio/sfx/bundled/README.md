# SFX incluidos con HyperFrames (bundled)

Copia de la biblioteca que trae la skill `media-use` de HyperFrames 0.8.141
(`~/.claude/skills/media-use/audio/assets/sfx/`). Es la que usa `media-use` cuando **no** hay credencial de HeyGen.

- **Fuente y licencia:** Pixabay, bajo la [Pixabay Content License](https://pixabay.com/service/license-summary/): uso comercial y no comercial, modificación y redistribución dentro de obras derivadas (videos), **sin atribución obligatoria**. Detalle original en `CREDITS-original.md`; metadatos originales en `manifest.json`.
- **Ojo:** la licencia es la que declara el paquete de HyperFrames; Pixabay no da el nombre del autor de cada archivo. Para un anuncio pagado conviene guardar esta nota como prueba de origen.
- 19 archivos `.mp3`, pero **solo 17 sonidos distintos**: `click.mp3` = `click-soft.mp3` y `whoosh.mp3` = `whoosh-short.mp3` (mismo MD5).
- Medido aquí (ffprobe + pyloudnorm, 2026-10-08). "Pico en" = segundo del archivo donde está el golpe: **resta ese valor al `data-start`** para que el golpe caiga en el corte.

| Archivo | Duración | Pico en | Nivel (LUFS int. / pico) | Uso sugerido en reels de Morishita |
|---|---|---|---|---|
| `whoosh.mp3` | 0.57 s | 0.16 s | −16.8 / −2.1 dBFS | **Transición** (flash, whip, corte de bloque). Arranca 0.16 s antes del corte. Volumen 0.6–0.8. |
| `whoosh-short.mp3` | 0.57 s | 0.16 s | idéntico a `whoosh` | Igual que `whoosh` (es el mismo archivo). |
| `whoosh-cinematic.mp3` | 5.54 s | ~2.4 s (crece desde ~1.5 s) | −14.1 / 0.0 | Transición lenta a la "revelación" (plato estrella). Arranca ~2.4 s antes del corte. Volumen 0.4–0.6. |
| `impact-bass-1.mp3` | 2.12 s | 0.07 s | −6.5 / −0.4 | **Golpe grave** del gancho y de la revelación (cifra "14", "4"). Muy fuerte: volumen 0.3–0.4. |
| `impact-bass-2.mp3` | 2.59 s | 0.13 s | −4.5 / 0.0 | Golpe grave con pequeño "swell"; alternativa al anterior. Volumen 0.3. |
| `riser.mp3` | 10.03 s | **~3.5 s** (sube de 0 a 3.5 s y se apaga en ~4.3 s; lo demás es silencio) | −6.6 / 0.0 | **Riser antes de la revelación.** El manifest dice "pico al final, arranca 10 s antes": **es falso**, medido: arráncalo ~3.5 s antes del golpe y recórtalo con `data-duration="4.3"`. Volumen 0.3–0.5. |
| `pop.mp3` | 0.72 s | 0.12 s | −21.3 / −3.2 | **Texto que aparece** (palabra clave del subtítulo, cifra). Volumen 0.3–0.4. |
| `click.mp3` | 0.37 s | 0.05 s | −25.0 / −5.4 | Captura de la web: "pulsar" el botón + / "Ver fechas". Volumen 0.4. |
| `click-soft.mp3` | 0.37 s | 0.05 s | idéntico a `click` | Igual que `click`. |
| `key-press.mp3` | 0.43 s | 0.07 s | −35.9 / −5.7 | Tecla suelta (poco útil; casi inaudible). |
| `typing.mp3` | 1.54 s | 0.46 s | −30.6 / −9.0 | Tipeo (no encaja con la marca; evitar). |
| `sparkle.mp3` | 1.80 s | 0.03 s | −11.2 / 0.0 | Brillo sobre el sello/logo del cierre, con moderación. Volumen 0.2–0.3. |
| `chime.mp3` | 2.54 s | 0.42 s | −28.0 / −9.3 | Confirmación suave (p. ej. "reserva lista" en la captura del resumen). |
| `notification.mp3` | 2.46 s | 0.23 s | −19.3 / −2.7 | Notificación (DM con el link). Solo si el CTA es de palabra clave. |
| `ping.mp3` | 1.32 s | 0.32 s | −25.5 / −6.2 | Acento electrónico. Poco premium; evitar. |
| `glitch-1.mp3` | 2.64 s | 0.74 s | −13.2 / 0.0 | Glitch de **texto** (≤ 3 frames, marca: nunca sobre comida). Recorta con `data-duration` ~0.4 s. |
| `glitch-2.mp3` | 3.50 s | 0.02 s | −4.6 / 0.0 | Glitch largo y áspero: **no** para Morishita. |
| `glitch-3.mp3` | 3.10 s | 1.82 s | −22.4 / −4.6 | Textura digital suave. Evitar. |
| `error.mp3` | 1.62 s | 0.74 s | −29.3 / −21.2 | Tono de error. No usar. |

## Cómo se usan en un proyecto

Copia el archivo dentro del proyecto (`videos/<id>/assets/sfx/`) y colócalo con un `<audio>` con `id` (sin `id` el mezclador lo ignora y el render sale mudo):

```html
<!-- whoosh: pico a 0.16 s → arranca 0.16 s antes del corte de 2.40 s -->
<audio id="sfx-whoosh" src="assets/sfx/whoosh.mp3"
       data-start="2.24" data-duration="0.57" data-track-index="11" data-volume="0.8"></audio>
```

`media-use` recomienda volumen ~0.35 para SFX bajo voz y música. Con voz encima, nada por arriba de 0.5 salvo el whoosh de una transición sin voz.
Música y más SFX (catálogo de HeyGen) requieren el CLI `heygen` con sesión iniciada: **no** está configurado aquí.
