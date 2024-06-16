const express = require('express');
const router = express.Router();
const { exec } = require('child_process');
const fs = require('fs');

router.get('/differences', (req, res) => {
    exec('python scripts/analysis.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).send('Error executing analysis');
        }

        fs.readFile('price_differences.json', 'utf8', (err, data) => {
            if (err) {
                console.error(`readFile error: ${err}`);
                return res.status(500).send('Error reading analysis output');
            }

            const differences = JSON.parse(data);
            res.json(differences);
        });
    });
});

module.exports = router;