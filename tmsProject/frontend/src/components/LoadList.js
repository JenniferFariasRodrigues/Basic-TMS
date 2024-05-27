import React, { useEffect, useState } from 'react';

const LoadList = () => {
    const [loads, setLoads] = useState([]);

    useEffect(() => {
        fetch('/api/loads')
            .then(response => response.json())
            .then(data => setLoads(data));
    }, []);

    return (
        <div>
            <h1>Loads</h1>
            <ul>
                {loads.map(load => (
                    <li key={load.id}>{load.customer} - {load.status}</li>
                ))}
            </ul>
        </div>
    );
};

export default LoadList;
