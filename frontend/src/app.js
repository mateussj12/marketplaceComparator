// frontend/src/App.js
import React from 'react';
import ProductList from './components/productList';
import PriceDifference from './components/priceDifference';

const App = () => {
    return (
        <div>
            <h1>Marketplace Comparator</h1>
            <ProductList />
            <PriceDifference />
        </div>
    );
};

export default App;
