// Libs
import PrimeReact from 'primereact/api';

// Configuration
import i18n from './i18n';
import { I18nextProvider } from 'react-i18next';
import { BrowserRouter } from 'react-router-dom';
import ThemeManager from './layouts/themeManager';

PrimeReact.ripple = true;

const Providers = (props : { children: object }) =>
    <BrowserRouter>
        <I18nextProvider i18n={i18n}>
            <ThemeManager>
                {props.children}
            </ThemeManager>
        </I18nextProvider>
    </BrowserRouter>;

export default Providers;