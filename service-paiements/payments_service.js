const express = require('express');
const router = express.Router();
const cors = require('cors');
// On inclut dompurify pour maintenir la correction XSS (V5) du Livrable 1.2
const createDomPurify = require('dompurify');
const { JSDOM } = require('jsdom');

const window = new JSDOM('').window;
const DOMPurify = createDomPurify(window);

// Correction V12 : CORS restrictif avec whitelist (Phase 3 anticipée) [cite: 222]
router.use(cors({
    origin: ['https://app.neobank.fr']
}));

/**
 * CORRECTION V6 : Mass Assignment [cite: 109]
 * On extrait seulement les champs autorisés du corps de la requête.
 */
router.put('/user/profile', async (req, res) => {
    try {
        const userId = req.user.id;

        // WHITELIST : Seuls ces champs peuvent être modifiés par l'utilisateur
        const { first_name, last_name, bio } = req.body;

        // On crée un objet propre qui ignore tout champ superflu (comme 'role' ou 'balance')
        const safeData = { first_name, last_name, bio };

        // Simulation de mise à jour sécurisée
        // await db.users.update(userId, safeData);

        res.json({
            message: 'Profil mis à jour avec succès (champs autorisés uniquement)',
            data: safeData
        });
    } catch (error) {
        res.status(500).json({ error: "Erreur lors de la mise à jour" });
    }
});

/**
 * RAPPEL CORRECTION V5 : XSS Stored [cite: 191]
 */
router.post('/transfer', async (req, res) => {
    const { to_account, amount, description } = req.body;

    // Sanitization de l'entrée utilisateur pour bloquer les scripts [cite: 192]
    const cleanDescription = DOMPurify.sanitize(description);

    res.json({
        message: 'Transfert effectué',
        description: cleanDescription
    });
});

module.exports = router;