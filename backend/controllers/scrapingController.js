const express = require('express');
const router = express.Router();
const scraperService = require('../services/scraperService');

router.get('/prices', async (req, res) => {
    try {
        const products = await scraperService.scrapeAllMarketplaces();
        res.json(products);
    } catch (error) {
        console.error('Error scraping prices: ', error);
        res.status(500).send('Error scraping prices');
    }
});

module.exports = router;