import React, { useEffect, useState } from 'react';
import { getMarketplacePrices } from '../services/api';

const ProductList = () => {
    const [products, setProducts] = useState([]);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const marketplaceProducts = await getMarketplacePrices();
                setProducts(marketplaceProducts);
            } catch (error) {
                console.error('Error fetching products:', error);
            }
        };

        fetchProducts();
    }, []);

    return (
        <div>
            <h2>Product List</h2>
            <ul>
                {products.map((product, index) => (
                    <li key={index}>
                        <strong>{product.name}</strong> - ${product.price}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ProductList;