// Launches the React application.
// Renders the main App component inside the DOM element with the ID root.
// Uses React.StrictMode to help detect potential issues during development.

import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

ReactDOM.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>,
    document.getElementById('root')
);
