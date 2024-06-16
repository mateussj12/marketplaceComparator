const express = require('express');
const router = express.Router();
const blingService = require('../services/blingService');

router.post('/update/:id', async (req, res) => {
    const productId = req.params.id;
    const newPrice = req.body.price;

    try {
        await blingService.updateBlingProductPrice(productId, newPrice);
        res.status(200).send('Price updated successfully');
    } catch (error) {
        console.error('Error updating price: ', error);
        res.status(500).send('Error updating price');
    }
});

module.exports = router;