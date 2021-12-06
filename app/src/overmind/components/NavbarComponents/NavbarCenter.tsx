import { Button } from 'primereact/button';

import { Route, Switch } from 'react-router';
import { useAppDispatch } from '../../../hooks';
import { addNotification } from '../../../notifications/slice';

import munityLogo from '../../../assets/logoIcon.png';
import { useTranslation } from 'react-i18next';

const NavbarCenter = () => {
    const dispatch = useAppDispatch();
    const { t } = useTranslation();
    const featureInative = () => {
        dispatch(addNotification({
            type: 'info',
            message: <div style={{display:'flex', alignItems: 'center'}}>
                <img style={{height:'60px'}} src={munityLogo} alt="munityLogo"/>
                <div>{t('app:you_need')}<a href="https://munityapps.com">
                    Munity Portal</a> {t('app:to_access_feature')}.
                </div>
            </div>
        }));
    };

    return <div className="middle-part">
        <Switch>
            <Route path="/">
                <Button onClick={featureInative} className={`p-button-link`}>{t('common:projects')}</Button>
                <Button onClick={featureInative} className={`p-button-link`}>{t('common:boilerplates')}</Button>
                <Button onClick={featureInative} className={`p-button-link`}>{t('common:developers')}</Button>
                <Button onClick={featureInative} className={`p-button-link`}>{t('common:learn')}</Button>
                <Button onClick={featureInative} className={`p-button-link`}>{t('common:feed')}</Button>
            </Route>
        </Switch>
    </div>;
}

export default NavbarCenter;