// Libs
import { Provider as ReduxProvider } from 'react-redux'
import PrimeReact from 'primereact/api';

// Configuration
import store from './store'
import i18n from './i18n';
import { I18nextProvider } from 'react-i18next';
import { BrowserRouter } from 'react-router-dom';

PrimeReact.ripple = true;

const Providers = (props: { children: object }) =>
    <BrowserRouter>
        <I18nextProvider i18n={i18n}>
            <ReduxProvider store={store}>
                {props.children}
            </ReduxProvider>
        </I18nextProvider>
    </BrowserRouter>;

export default Providers;