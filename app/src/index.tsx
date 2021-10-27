// Libs
import React from 'react';
import ReactDOM from 'react-dom';

// Component
import Providers from './providers';
import MunityRouter from './router';

// Configuration
import reportWebVitals from './reportWebVitals';

// Style
import './styles.scss';


ReactDOM.render(
    <Providers>
        <React.StrictMode>
            <MunityRouter>
                {/* Custom routes */}
            </MunityRouter>
        </React.StrictMode>
    </Providers>,
    document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals(console.log);
