// Component
import App from '../app';
import '../websocket';

// Hook
import { useTranslation } from 'react-i18next';

// SCSS
// import 'primeflex/primeflex.css';
import './style.scss';
import './_overrides.scss';
import 'primeflex/src/_variables.scss';
import 'primeflex/src/_grid.scss';
import 'primeflex/src/_formlayout.scss';
import 'primeflex/src/_display.scss';
import 'primeflex/src/_text.scss';
import 'primeflex/src/flexbox/_flexbox.scss';
import 'primeflex/src/_spacing.scss';
import 'primeflex/src/_elevation.scss';


const Core = () => {
    const { t } = useTranslation();
    return (
        <App>
            {t('common:graph')}
        </App>
    );
}

export default Core;
