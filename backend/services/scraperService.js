const axios = require('axios');
const cheerio = require('cheerio');

const scrapeMarketplace = async (url) => {
    try {
        const { data } = await axios.get(url);
        const $ = cheerio.load(data);
        let products = [];

        $('.product-item').each((index, element) => {
            const name = $(element).find('.product-name').text().trim();
            const price = parseFloat($(element).find('.product-price').text().replace('$', ''));
            products.push({ name, price });
        });

        return products;
    } catch (error) {
        console.error('Error scraping marketplace: ', error);
        return [];
    }
};

const scrapeAllMarketplaces = async () => {
    const urls = [
        "https://marketplace1.com",
        "https://marketplace2.com",
        // adicionar mais URLs aqui
    ];

    let allProducts = [];
    for (let url of urls) {
        const products = await scrapeMarketplace(url);
        allProducts = [...allProducts, ...products];
    }

    return allProducts;
};

module.exports = { scrapeAllMarketplaces };