import React, { useEffect, useState } from 'react';

const ProduceItemList = () => {
    const [produceItems, setProduceItems] = useState([]);

    useEffect(() => {
        fetch('/api/produce')
            .then(response => response.json())
            .then(data => setProduceItems(data));
    }, []);

    return (
        <div>
            <h1>Produce Items</h1>
            <ul>
                {produceItems.map(item => (
                    <li key={item.id}>{item.name} - {item.category}</li>
                ))}
            </ul>
        </div>
    );
};

export default ProduceItemList;
