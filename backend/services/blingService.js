const axios = require('axios');

const updateBlingProductPrice = async (productId, newPrice) => {
    const apikey = 'YOUR_BLING_API_KEY'; // Substituir pela sua chave API do Bling
    const url = `https://bling.com.br/Api/v2/produto/${productId}/json?apikey=${apikey}`;
    const xmlData = `<produto><preco>${newPrice}</preco></produto>`;

    try {
        const response = await axios.post(url, xmlData, {
            headers: { 'Content-Type': 'application/xml' }
        });
        console.log('Response from Bling:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error updating price in Bling: ', error);
        throw error;
    }
};

module.exports = { updateBlingProductPrice };