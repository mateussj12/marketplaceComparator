import React, { useEffect, useState } from 'react';
import { getPriceDifferences } from '../services/api';

const PriceDifference = () => {
    const [differences, setDifferences] = useState([]);

    useEffect(() => {
        const fetchDifferences = async () => {
            try {
                const priceDifferences = await getPriceDifferences();
                setDifferences(priceDifferences);
            } catch (error) {
                console.error('Error fetching price differences:', error);
            }
        };

        fetchDifferences();
    }, []);

    return (
        <div>
            <h2>Price Differences</h2>
            <ul>
                {differences.map((difference, index) => (
                    <li key={index}>
                        <strong>{difference.name}</strong> - Marketplace: ${difference.marketplace_price} | Bling: ${difference.bling_price}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default PriceDifference;