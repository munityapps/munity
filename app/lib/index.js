import { jsx as _jsx } from "react/jsx-runtime";
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
ReactDOM.render(_jsx(Providers, { children: _jsx(React.StrictMode, { children: _jsx(MunityRouter, {}, void 0) }, void 0) }, void 0), document.getElementById('root'));
// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals(console.log);
