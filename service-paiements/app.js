require('dotenv').config(); //
const express = require('express');
const helmet = require('helmet'); // [cite: 174, 222]
const cors = require('cors'); //
const rateLimit = require('express-rate-limit'); // [cite: 208]
const paymentsRouter = require('./payments_service');

const app = express();

// CORRECTION V12 : Headers de sécurité (Helmet) et CORS restrictif
app.use(helmet()); //
app.use(cors({
    origin: ['https://app.neobank.fr'], // Whitelist (V12)
    methods: ['GET', 'POST']
}));

// CORRECTION V11 : Validation du Content-Type et limitation de taille
app.use(express.json({ limit: '10kb' }));

// CORRECTION V7 : Rate Limiting contre le brute force [cite: 209]
const loginLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 5,
    message: { error: "Trop de tentatives de connexion (V7)." },
    standardHeaders: true,
    legacyHeaders: false,
});

app.post('/login', loginLimiter, (req, res) => {
    res.json({ message: "Tentative d'authentification" });
});

app.use('/api/payments', paymentsRouter);

// CORRECTION V10 : Gestion d'erreurs sans stack trace [cite: 143, 223]
app.use((err, req, res, next) => {
    // V9 : Logging structuré en interne [cite: 226]
    console.error(`[ERROR] ${new Date().toISOString()}: ${err.message}`);

    res.status(500).json({
        error: "Une erreur interne est survenue.",
        code: "INTERNAL_ERROR"
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Service Paiements sur le port ${PORT}`));