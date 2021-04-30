// Libs
import { Provider } from 'react-redux'
import PrimeReact from 'primereact/api';

// Configuration
import store from './store'
import './i18n';

PrimeReact.ripple = true;

const Providers = (props: {children: object}) =>
    <Provider store={store}>
        {props.children}
    </Provider>;

export default Providers;