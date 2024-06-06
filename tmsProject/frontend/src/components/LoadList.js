//responsible for fetching and displaying a list of loads from an API.
// When the component is mounted, it makes a request to the /api/loads route,
//converts the response to JSON and updates the loads state with the data received. 
//The list of loads is then rendered into an unordered list (<ul>), with each load displayed
// as a list item (<li>), showing the customer and status of the load.
import React, { useEffect, useState } from 'react';

// useState hook
// to manage the local state, which in this case is the load list.
const LoadList = () => {
    const [loads, setLoads] = useState([]);

    //hook useEffect
    // to perform side effects, such as fetching data from an API when the component is mounted.
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
