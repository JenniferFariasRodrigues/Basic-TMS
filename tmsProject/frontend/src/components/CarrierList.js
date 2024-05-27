import React, { useEffect, useState } from 'react';

const CarrierList = () => {
    const [carriers, setCarriers] = useState([]);

    useEffect(() => {
        fetch('/api/carriers')
            .then(response => response.json())
            .then(data => setCarriers(data));
    }, []);

    return (
        <div>
            <h1>Carriers</h1>
            <ul>
                {carriers.map(carrier => (
                    <li key={carrier.id}>{carrier.name} - {carrier.company}</li>
                ))}
            </ul>
        </div>
    );
};

export default CarrierList;
