import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import CarriersPage from './pages/CarriersPage';
import LoadsPage from './pages/LoadsPage';
import ProduceItemsPage from './pages/ProduceItemsPage';

const App = () => {
    return (
        <Router>
            <div>
                <Switch>
                    <Route path="/carriers" component={CarriersPage} />
                    <Route path="/loads" component={LoadsPage} />
                    <Route path="/produce-items" component={ProduceItemsPage} />
                </Switch>
            </div>
        </Router>
    );
};

export default App;
//PS: I forgot of implemented the LoadsPage method.
