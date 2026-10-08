# SFX sintetizados (kit propio de Morishita)

- **Fuente:** generados el 2026-10-08 con `reels/audio/_src/gen_sfx.py` (numpy/scipy: osciladores, ruido filtrado, síntesis modal, Karplus-Strong y reverb con IR sintética). No se usó ninguna muestra grabada, banco de sonidos ni IA de terceros.
- **Licencia:** obra original, generada internamente para Morishita Japanese Cuisine. Sin terceros, sin atribución obligatoria; se puede usar en reels orgánicos y pagados. Si cambias el script, vuelve a correrlo y se regeneran iguales (semillas fijas).
- **Formato:** WAV 48 kHz, estéreo, 24 bits, **pico de muestra −3.0 dBFS** en todos. El `glitch-zap` y los `pop` llegan a ~−1.7 dBTP por picos entre muestras: bájalos en la mezcla como cualquier SFX.
- **"Pico en"** = segundo del archivo donde está el golpe. **Resta ese valor al `data-start`** para que el golpe caiga en el corte o en la palabra.
- Volumen sugerido en HyperFrames: SFX entre 0.3 y 0.6 bajo la voz; los booms 0.35–0.5; el rin 0.3–0.4 (es brillante). Nunca encima de una palabra importante de la voz.
- Datos medidos de cada archivo: `manifest.json`.

| Archivo | Duración | Pico en | LUFS | Uso en reels de Morishita |
|---|---|---|---|---|
| `whoosh-corto-01.wav` | 0.25 s | 0.14 s | −15.6 | Transición rápida: corte, punch-in, flash. |
| `whoosh-medio-02.wav` | 0.36 s | 0.23 s | −16.7 | Whip pan, cambio de bloque. Paneo izq → der. |
| `whoosh-suave-03.wav` | 0.50 s | 0.32 s | −15.4 | Transición elegante y más oscura: entrada a la reseña o al momento estrella. |
| `pop-texto-suave-01.wav` | 0.18 s | 0.00 s | −12.7 | Aparece la palabra clave del subtítulo. Suave, no tapa la voz. |
| `pop-texto-agudo-02.wav` | 0.14 s | 0.00 s | −12.1 | Cifra grande ("14 TIEMPOS", "4 LUGARES"). |
| `click-texto-madera-03.wav` | 0.08 s | 0.00 s | −11.8 | Click seco de madera: textos que entran en ritmo, listas. |
| `boom-grave-01.wav` | 2.20 s | 0.04 s | −17.8 | Golpe grave del gancho (frame 0) y de la revelación. |
| `boom-taiko-02.wav` | 2.60 s | 0.01 s | −18.7 | Impacto grave con cuerpo de taiko: revelación, cambio de sección, arranque del CTA. |
| `riser-1-5s.wav` | 1.50 s | 1.47 s | −17.8 | Riser corto: arráncalo 1.5 s antes del golpe; corta en seco en el golpe. |
| `riser-2-5s.wav` | 2.50 s | 2.44 s | −16.6 | Riser largo antes de la revelación (2.5 s antes del golpe). |
| `glitch-zap.wav` | 0.16 s | 0.00 s | −11.2 | Glitch corto **solo sobre texto o gráfico** (≤ 3 frames de efecto), nunca sobre comida. |
| `tick-obturador.wav` | 0.12 s | 0.03 s | −18.7 | Tick de cámara: entra una captura (p. ej. la del flujo de reserva) o una foto fija. |
| `hyoshigi-2-golpes.wav` | 1.30 s | 0.00 s y 0.42 s | −19.1 | Claves de madera japonesas, 2 golpes (el 2º a 0.42 s). Firma sonora: "empieza el servicio", o marcar el CTA. |
| `shing-metal.wav` | 2.20 s | 0.12 s | −17.9 | Destello metálico **sintético** (no es sonido real de cuchillo; no lo presentes como tal): brillo sobre título o sello del cierre. |
| `rin-resena.wav` | 4.00 s | 0.17 s | −13.4 | Campanita "rin" suave al aparecer una reseña de Google (estrellas). Volumen 0.3–0.4. |
| `tap-cta.wav` | 0.09 s | 0.00 s | −13.6 | Toque de dedo en pantalla: botón "Reservar", link del perfil, captura del flujo de reserva. |

Notas honestas:
- Son sonidos sintéticos limpios, no grabaciones. Los mejor logrados (por diseño y espectrograma) son whooshes, booms, risers, pops, tap y rin. El `hyoshigi` y el `shing` son aproximaciones por síntesis modal: suenan a madera y a metal, pero no a una grabación real.
- CLAUDE.md pide **sonidos reales de cocina** (cuchillo, soplete, chisporroteo) cuando haya: no están aquí y no se deben simular. Esos salen del audio de las tomas del restaurante.
