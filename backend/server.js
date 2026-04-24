const express = require('express');
const stripe = require('stripe')('sk_test_51Smn0T4H8kzYeS9YRX43IXSEcCzP0Cpx32UzvW61BVkH79YkqlPFbOWjBPhyFw02Ay5NbC0qpPoOORUG1ceezTyt00CSUqzqCY');
const cors = require('cors');
const { createClient } = require('@supabase/supabase-js');

const supabase = createClient('https://tuygcyjdnylohjkuqojk.supabase.co', 'sb_publishable_bNgItpe84VinnweVCUTyGw_Z2EF-vvz');

const app = express();
app.use(express.static('../')); // Servir el frontend
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  next();
});
app.use((req, res, next) => {
  if (req.originalUrl === '/stripe-webhook') {
    next();
  } else {
    express.json()(req, res, next);
  }
});
app.use(cors());

app.post('/create-checkout-session', express.json(), async (req, res) => {
  const { date, time, guests, nombre, email, whatsapp } = req.body;
  const unit_amount = 1850 * 0.5 * 100; // Anticipo del 50% en centavos (MXN)

  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      customer_email: email,
      line_items: [{
        price_data: {
          currency: 'mxn',
          product_data: {
            name: `Anticipo Reservación Omakase - Morishita`,
            description: `${guests} personas | Fecha: ${date} | Hora: ${time} | Cliente: ${nombre}`,
          },
          unit_amount: unit_amount,
        },
        quantity: guests,
      }],
      mode: 'payment',
      metadata: {
        date, time, guests, nombre, email, whatsapp, alergias: req.body.alergias || '', motivo: req.body.motivo || ''
      },
      success_url: `https://${req.get('host')}/?status=success&session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `https://${req.get('host')}/?status=cancel`,
    });

    res.json({ url: session.url });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/stripe-webhook', express.raw({type: 'application/json'}), async (req, res) => {
  const sig = req.headers['stripe-signature'];
  const endpointSecret = 'whsec_zzkop1DfjGHachAb25hk3q3iZW97tvjX'; // Secreto Webhook Test
  let event;

  try {
    event = stripe.webhooks.constructEvent(req.body, sig, endpointSecret);
  } catch (err) {
    console.error(`Webhook signature verification failed: ${err.message}`);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  if (event.type === 'checkout.session.completed') {
    const session = event.data.object;
    const meta = session.metadata;
    
    console.log("Pago exitoso confirmado por Stripe. Guardando en Supabase...", meta);

    // Guardar en Supabase seguro vía Webhook
    const { error } = await supabase
      .from('Reservas')
      .upsert([
        { 
          fecha: meta.date, 
          hora: meta.time, 
          nombre: meta.nombre, 
          whatsapp: meta.whatsapp, 
          email: meta.email, 
          comensales: meta.guests,
          alergias: meta.alergias,
          motivo: meta.motivo,
          status: 'confirmada'
        }
      ], { onConflict: 'email,fecha,hora' });

    if (error) console.error("Error guardando en Supabase:", JSON.stringify(error));
  }

  res.json({received: true});
});

app.get('/stripe-webhook-client', async (req, res) => {
  const { session_id } = req.query;
  try {
    const session = await stripe.checkout.sessions.retrieve(session_id);
    const meta = session.metadata;

    // Forzar guardado en Supabase al regresar a la web
    const { error } = await supabase
      .from('Reservas')
      .upsert([
        { 
          fecha: meta.date, 
          hora: meta.time, 
          nombre: meta.nombre, 
          whatsapp: meta.whatsapp, 
          email: meta.email, 
          comensales: meta.guests,
          alergias: meta.alergias,
          motivo: meta.motivo,
          status: 'confirmada'
        }
      ], { onConflict: 'email,fecha,hora' });

    res.json({
      fecha: meta.date,
      hora: meta.time,
      comensales: meta.guests
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

const PORT = process.env.PORT || 3000;
if (process.env.NODE_ENV !== 'production') {
  app.listen(PORT, () => console.log(`Servidor local en ${PORT}`));
}
module.exports = app;
