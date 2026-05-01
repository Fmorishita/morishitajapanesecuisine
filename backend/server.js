// ================================================================
// MORISHITA — Backend de reservas
// Vercel Serverless (Node.js + Express)
// ================================================================

const express = require('express');
const cors = require('cors');
const Stripe = require('stripe');
const { createClient } = require('@supabase/supabase-js');

// ----------------------------------------------------------------
// VARIABLES DE ENTORNO (configuradas en Vercel)
// ----------------------------------------------------------------
const STRIPE_SECRET_KEY        = process.env.STRIPE_SECRET_KEY;
const STRIPE_WEBHOOK_SECRET    = process.env.STRIPE_WEBHOOK_SECRET;
const SUPABASE_URL             = process.env.SUPABASE_URL;
const SUPABASE_SERVICE_ROLE    = process.env.SUPABASE_SERVICE_ROLE_KEY;
const PRECIO_POR_PERSONA_MXN   = parseInt(process.env.PRECIO_POR_PERSONA_MXN || '1850', 10);
const PORCENTAJE_ANTICIPO      = parseFloat(process.env.PORCENTAJE_ANTICIPO || '0.5');
const CAPACIDAD_MAXIMA_SESION  = parseInt(process.env.CAPACIDAD_MAXIMA_SESION || '4', 10);

// Validar config crítica al arranque
if (!STRIPE_SECRET_KEY || !SUPABASE_URL || !SUPABASE_SERVICE_ROLE) {
  console.error('❌ Faltan variables de entorno críticas');
}

const stripe = Stripe(STRIPE_SECRET_KEY);

// Service role: solo en backend, nunca expuesta al cliente.
// Permite escribir en la base de datos saltándose RLS (necesario para reservas web).
const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE, {
  auth: { persistSession: false }
});

// ----------------------------------------------------------------
// HELPERS
// ----------------------------------------------------------------

/**
 * Mapea el horario que viene del frontend (ej. "13:00") al enum de la BD.
 * La BD acepta: COMIDA, TARDE, CENA, NOCHE.
 */
function mapearHorario(horarioInput) {
  if (!horarioInput) return null;
  const h = String(horarioInput).trim().toUpperCase();

  // Si ya viene como enum válido, lo respetamos
  if (['COMIDA', 'TARDE', 'CENA', 'NOCHE'].includes(h)) return h;

  // Si viene como hora (ej "13:00", "1:00 PM", "15:30")
  const match = h.match(/(\d{1,2})/);
  if (match) {
    const hora = parseInt(match[1], 10);
    if (hora >= 12 && hora < 14) return 'COMIDA';   // 1:00 pm
    if (hora >= 14 && hora < 17) return 'TARDE';    // 3:30 pm
    if (hora >= 17 && hora < 20) return 'CENA';     // 6:00 pm
    if (hora >= 20 || hora < 6)  return 'NOCHE';
  }
  return null;
}

/**
 * Cuenta cuántas personas ya están reservadas para una fecha + horario.
 * Suma numero_personas de reservas Confirmada/Pendiente/Completada.
 */
async function personasReservadas(fecha, horario) {
  const { data, error } = await supabase
    .from('reservations')
    .select('numero_personas')
    .eq('fecha', fecha)
    .eq('horario', horario)
    .in('estado', ['Confirmada', 'Pendiente', 'Completada']);

  if (error) {
    console.error('Error consultando ocupación:', error);
    throw error;
  }

  return (data || []).reduce((sum, r) => sum + (r.numero_personas || 0), 0);
}

/**
 * Revisa si la fecha+horario está bloqueado (time_blocks o DIA_COMPLETO).
 */
async function estaBloqueado(fecha, horario) {
  const { data, error } = await supabase
    .from('time_blocks')
    .select('id, horario')
    .eq('fecha', fecha)
    .in('horario', [horario, 'DIA_COMPLETO']);

  if (error) {
    console.error('Error consultando bloqueos:', error);
    throw error;
  }
  return (data || []).length > 0;
}

// ----------------------------------------------------------------
// APP EXPRESS
// ----------------------------------------------------------------
const app = express();
app.use(cors());

// Logger sencillo
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  next();
});

// ⚠️ Importante: el webhook de Stripe necesita el body RAW (sin parsear).
// Por eso el middleware express.json() se aplica DESPUÉS de la ruta /stripe-webhook.
// Límite de 10mb para permitir upload de imágenes en base64 desde el admin panel.
app.use((req, res, next) => {
  if (req.originalUrl === '/stripe-webhook') return next();
  express.json({ limit: '10mb' })(req, res, next);
});

// ----------------------------------------------------------------
// ADMIN MIDDLEWARE
// ----------------------------------------------------------------
const ADMIN_TOKEN = process.env.ADMIN_TOKEN || '1850';

function requireAdmin(req, res, next) {
  if (req.headers['x-admin-token'] !== ADMIN_TOKEN) {
    return res.status(401).json({ error: 'No autorizado' });
  }
  next();
}

// ================================================================
// ENDPOINT: Consultar disponibilidad de una fecha
// GET /disponibilidad?fecha=YYYY-MM-DD
// ================================================================
app.get('/disponibilidad', async (req, res) => {
  try {
    const { fecha } = req.query;
    if (!fecha) return res.status(400).json({ error: 'Falta parámetro fecha' });

    const horarios = ['COMIDA', 'TARDE', 'CENA'];
    const resultado = {};

    for (const h of horarios) {
      const bloqueado = await estaBloqueado(fecha, h);
      const ocupados = bloqueado ? CAPACIDAD_MAXIMA_SESION : await personasReservadas(fecha, h);
      const disponibles = Math.max(0, CAPACIDAD_MAXIMA_SESION - ocupados);
      resultado[h] = {
        bloqueado,
        ocupados,
        disponibles,
        capacidad: CAPACIDAD_MAXIMA_SESION
      };
    }

    res.json({ fecha, sesiones: resultado });
  } catch (error) {
    console.error('Error en /disponibilidad:', error);
    res.status(500).json({ error: error.message });
  }
});

// ================================================================
// ENDPOINT: Crear sesión de checkout en Stripe
// POST /create-checkout-session
// Body: { date, time, guests, nombre, email, whatsapp, alergias?, motivo? }
// ================================================================
app.post('/create-checkout-session', async (req, res) => {
  try {
    const { date, time, guests, nombre, email, whatsapp, alergias = '', motivo = '' } = req.body;

    // 1. Validar input
    if (!date || !time || !guests || !nombre || !email) {
      return res.status(400).json({ error: 'Faltan campos obligatorios' });
    }

    const numGuests = parseInt(guests, 10);
    if (isNaN(numGuests) || numGuests < 1 || numGuests > CAPACIDAD_MAXIMA_SESION) {
      return res.status(400).json({ error: `Número de personas debe ser entre 1 y ${CAPACIDAD_MAXIMA_SESION}` });
    }

    const horario = mapearHorario(time);
    if (!horario) {
      return res.status(400).json({ error: `Horario inválido: ${time}` });
    }

    // 2. Verificar disponibilidad (no vender cupos llenos)
    if (await estaBloqueado(date, horario)) {
      return res.status(409).json({ error: 'Esta sesión no está disponible.' });
    }

    const ocupados = await personasReservadas(date, horario);
    const disponibles = CAPACIDAD_MAXIMA_SESION - ocupados;
    if (numGuests > disponibles) {
      return res.status(409).json({
        error: `Solo quedan ${disponibles} asientos disponibles en esta sesión.`,
        disponibles
      });
    }

    // 3. Crear sesión de Stripe
    const unit_amount = Math.round(PRECIO_POR_PERSONA_MXN * PORCENTAJE_ANTICIPO * 100); // centavos MXN

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      customer_email: email,
      line_items: [{
        price_data: {
          currency: 'mxn',
          product_data: {
            name: 'Anticipo Reservación Omakase — Morishita',
            description: `${numGuests} personas | ${date} | ${horario} | ${nombre}`,
          },
          unit_amount,
        },
        quantity: numGuests,
      }],
      mode: 'payment',
      metadata: {
        date,
        horario,
        guests: String(numGuests),
        nombre,
        email,
        whatsapp: whatsapp || '',
        alergias,
        motivo
      },
      success_url: `https://${req.get('host')}/?status=success&session_id={CHECKOUT_SESSION_ID}`,
      cancel_url:  `https://${req.get('host')}/?status=cancel`,
    });

    res.json({ url: session.url });
  } catch (error) {
    console.error('Error en /create-checkout-session:', error);
    res.status(500).json({ error: error.message });
  }
});

// ================================================================
// ENDPOINT: Webhook de Stripe (confirmación de pago)
// POST /stripe-webhook
// ================================================================
app.post('/stripe-webhook', express.raw({ type: 'application/json' }), async (req, res) => {
  const sig = req.headers['stripe-signature'];

  let event;
  try {
    event = stripe.webhooks.constructEvent(req.body, sig, STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    console.error(`❌ Webhook signature verification failed: ${err.message}`);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  if (event.type === 'checkout.session.completed') {
    const session = event.data.object;
    const meta = session.metadata || {};
    const sessionId = session.id;

    console.log('✅ Pago confirmado por Stripe:', sessionId, meta);

    try {
      // Idempotencia: si ya existe una reserva con este stripe_session_id, no insertar otra.
      const { data: existing } = await supabase
        .from('reservations')
        .select('id, estado')
        .eq('stripe_session_id', sessionId)
        .maybeSingle();

      if (existing) {
        // Asegurar que esté Confirmada
        if (existing.estado !== 'Confirmada' && existing.estado !== 'Completada') {
          await supabase
            .from('reservations')
            .update({ estado: 'Confirmada' })
            .eq('id', existing.id);
        }
        console.log('Reserva ya existía, actualizada:', existing.id);
      } else {
        // Insertar reserva nueva
        const montoMXN = (session.amount_total || 0) / 100;
        const { error } = await supabase
          .from('reservations')
          .insert([{
            fecha: meta.date,
            horario: meta.horario,
            numero_personas: parseInt(meta.guests, 10),
            nombre_cliente: meta.nombre,
            whatsapp: meta.whatsapp || null,
            email: meta.email || null,
            motivo_visita: meta.motivo || null,
            alergias: meta.alergias || null,
            tipo_menu: 'Omakase 14 tiempos',
            estado: 'Confirmada',
            origen: 'web',
            metodo_pago: 'Stripe',
            monto_pagado: montoMXN,
            fecha_pago: new Date().toISOString(),
            stripe_session_id: sessionId,
            notas_internas: 'Reserva automática desde web'
          }]);

        if (error) {
          console.error('❌ Error guardando reserva:', error);
          // Devolvemos 500 para que Stripe reintente el webhook
          return res.status(500).json({ error: error.message });
        }
        console.log('✅ Reserva guardada en Supabase');
      }
    } catch (err) {
      console.error('❌ Error procesando webhook:', err);
      return res.status(500).json({ error: err.message });
    }
  }

  res.json({ received: true });
});

// ================================================================
// ENDPOINT: Confirmación al regresar a la web (UX)
// GET /stripe-webhook-client?session_id=xxx
// Solo lee la sesión de Stripe para mostrar al cliente sus datos.
// NO escribe en BD — eso lo hace el webhook real (más confiable).
// ================================================================
app.get('/stripe-webhook-client', async (req, res) => {
  try {
    const { session_id } = req.query;
    if (!session_id) return res.status(400).json({ error: 'Falta session_id' });

    const session = await stripe.checkout.sessions.retrieve(session_id);
    const meta = session.metadata || {};

    res.json({
      fecha: meta.date,
      horario: meta.horario,
      comensales: meta.guests,
      nombre: meta.nombre,
      pagado: session.payment_status === 'paid'
    });
  } catch (error) {
    console.error('Error en /stripe-webhook-client:', error);
    res.status(500).json({ error: error.message });
  }
});

// ================================================================
// ENDPOINTS: Contenido editable del sitio (site_content)
// ================================================================

// GET /api/content — público, devuelve todo como objeto key→value
app.get('/api/content', async (req, res) => {
  try {
    const { data, error } = await supabase
      .from('site_content')
      .select('key, value');
    if (error) throw error;
    const obj = {};
    (data || []).forEach(r => { obj[r.key] = r.value; });
    res.setHeader('Cache-Control', 'public, s-maxage=30');
    res.json(obj);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST /api/content/update — admin: upserta un campo de texto
app.post('/api/content/update', requireAdmin, async (req, res) => {
  try {
    const { key, value } = req.body;
    if (!key) return res.status(400).json({ error: 'Falta key' });
    const { error } = await supabase
      .from('site_content')
      .upsert({ key, value: value ?? '', updated_at: new Date().toISOString() });
    if (error) throw error;
    res.json({ ok: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST /api/content/upload-image — admin: sube imagen y guarda URL en site_content
// Body: { key, filename, data (base64), type (mime) }
app.post('/api/content/upload-image', requireAdmin, async (req, res) => {
  try {
    const { key, filename, data, type } = req.body;
    if (!key || !filename || !data) {
      return res.status(400).json({ error: 'Faltan campos: key, filename, data' });
    }
    const buffer = Buffer.from(data, 'base64');
    const storagePath = `${Date.now()}-${filename.replace(/[^a-zA-Z0-9._-]/g, '_')}`;

    const { error: uploadError } = await supabase.storage
      .from('site-images')
      .upload(storagePath, buffer, { contentType: type || 'image/jpeg', upsert: true });

    if (uploadError) throw uploadError;

    const { data: { publicUrl } } = supabase.storage
      .from('site-images')
      .getPublicUrl(storagePath);

    await supabase
      .from('site_content')
      .upsert({ key, value: publicUrl, updated_at: new Date().toISOString() });

    res.json({ ok: true, url: publicUrl });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ----------------------------------------------------------------
// HEALTH CHECK (útil para verificar que todo está bien configurado)
// ----------------------------------------------------------------
app.get('/health', async (req, res) => {
  const checks = {
    stripe: !!STRIPE_SECRET_KEY,
    supabase_url: !!SUPABASE_URL,
    supabase_key: !!SUPABASE_SERVICE_ROLE,
    webhook_secret: !!STRIPE_WEBHOOK_SECRET,
  };
  const ok = Object.values(checks).every(Boolean);
  res.status(ok ? 200 : 500).json({ ok, checks });
});

// ----------------------------------------------------------------
// Local dev only
// ----------------------------------------------------------------
const PORT = process.env.PORT || 3000;
if (process.env.NODE_ENV !== 'production') {
  app.listen(PORT, () => console.log(`Servidor local en :${PORT}`));
}

module.exports = app;
