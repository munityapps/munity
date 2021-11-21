import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useAppDispatch, useAppSelector } from '../hooks';
import { authenticate } from './slice';


import './style.scss';

const LoginForm:React.FC<{logo:string}> = props => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const { t } = useTranslation();
    const dispatch = useAppDispatch();
    const loginInProgress = useAppSelector(state => state.authentication.pending);

    const sendAuthentication = async () => {
        dispatch(authenticate({
            username: username,
            password: password,
        }))
    }

    return <form className="login-form" onSubmit={e => {
        e.preventDefault();
        sendAuthentication();
    }}>
        <div className="login-form-wrapper">
            <img src={props.logo} alt="Logo" className="logo"/>
            <div className="welcome">{t('app:welcome')}</div>
            <div className="welcome-text">{t('app:welcome_text')}</div>
            <div className="p-field">
                <label htmlFor="username" className="p-d-block">{t('common:user')}</label>
                <InputText autoComplete="username" id="username" value={username} onChange={(e) => setUsername(e.target.value)} />
            </div>
            <div className="p-field">
                <label htmlFor="password" className="p-d-block">{t('common:password')}</label>
                <InputText autoComplete="current-password" id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            </div>
            {
                <Button disabled={loginInProgress} type="submit" onSubmit={sendAuthentication}
                    icon="pi pi-arrow-right" iconPos="right" label={t('common:login')}
                    />
            }
        </div>
    </form>;
}

export default LoginForm;
