import React, { useEffect, useState } from 'react';
import CarrierCard from './CarrierCard';
import './CarrierList.css';

const CarrierList = () => {
    //useState hook
    // to manage local state, such as the list of carriers and loading or error states.
    const [carriers, setCarriers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    //hook useEffect
    // to perform side effects, such as fetching data from an API when the component is mounted.
    useEffect(() => {
        fetch('/api/carriers')
            .then(response => response.json())
            .then(data => setCarriers(data));
    }, []);
    
//Rendering the carrier list using the CarrierCard component for each carrier in the list.
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
