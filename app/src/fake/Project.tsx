import { FunctionComponent } from "react";
import { Route, Switch } from 'react-router';
import { Button } from 'primereact/button';
import { useTranslation } from 'react-i18next';
import Navbar from "../overmind/components/Navbar";
import NavbarLeft from "../overmind/components/NavbarComponents/NavbarLeft";
import NavbarCenter from "../overmind/components/NavbarComponents/NavbarCenter";
import NavbarRight from "../overmind/components/NavbarComponents/NavbarRight";

const ProjectList: FunctionComponent<{}> = () => {
    const { t } = useTranslation();
    const MiddlePart = () => <div className="middle-part">
        <Switch>
            <Route path="/">
                <Button className={`p-button-link`} style={{fontWeight:'bold',color:'var(--primary-color)'}}>{t('common:projects')}</Button>
                <Button className={`p-button-link`}>{t('common:boilerplates')}</Button>
                <Button className={`p-button-link`}>{t('common:developers')}</Button>
                <Button className={`p-button-link`}>{t('common:learn')}</Button>
                <Button className={`p-button-link`}>{t('common:feed')}</Button>
            </Route>
        </Switch>
    </div>;
    return <div style={{backgroundColor:'#252A48', minHeight:'100%'}}>
        <Navbar
            leftPart={NavbarLeft}
            centerPart={MiddlePart}
            rightPart={NavbarRight}
        />
        <div className="main">
            <Button label="Create new project" />
        </div>
    </div>
}

export default ProjectList;
