import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const getMarketplacePrices = async () => {
    try {
        const response = await axios.get(`${API_URL}/scraping/prices`);
        return response.data;
    } catch (error) {
        console.error('Error fetching marketplace prices:', error);
        throw error;
    }
};

const getPriceDifferences = async () => {
    try {
        const response = await axios.get(`${API_URL}/analysis/differences`);
        return response.data;
    } catch (error) {
        console.error('Error fetching price differences:', error);
        throw error;
    }
};

export { getMarketplacePrices, getPriceDifferences };