# morishitajapanesecuisine
MORISHITA JAPANESE CUISINE

## Variables de entorno (Vercel)

- `ADMIN_TOKEN`: token de los paneles `/admin`, `/admin/contenido` y `/evaluacion/admin`. Obligatorio, mínimo 16 caracteres (p. ej. `openssl rand -hex 24`). Sin él, los endpoints de admin responden 503.
