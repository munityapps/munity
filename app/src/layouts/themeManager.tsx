import { PropsWithChildren, useEffect } from 'react';

import {  useAppSelector } from '../hooks';

const ThemeManager:React.FunctionComponent<PropsWithChildren<{}>>  = props => {
    const { primaryColor, primaryColorText, secondaryColor,
        textColor, secondaryColorText,
        contentPadding, inlineSpacing,
        surfaceA, surfaceB, surfaceC, surfaceD,
        errorColor, validColor, navbarColor, navbarColorText
    } = useAppSelector(state => state.layout);

    useEffect(() => {
        if (primaryColor) document.documentElement.style.setProperty("--primary-color", primaryColor);
        if (primaryColorText) document.documentElement.style.setProperty("--primary-color-text", primaryColorText);
        if (secondaryColor) document.documentElement.style.setProperty("--secondary-color", secondaryColor);
        if (textColor) document.documentElement.style.setProperty("--text-color", textColor);
        if (secondaryColorText) document.documentElement.style.setProperty("--secondary-color-text", secondaryColorText);
        if (contentPadding) document.documentElement.style.setProperty("--content-padding", contentPadding);
        if (inlineSpacing) document.documentElement.style.setProperty("--inline-spacing", inlineSpacing);
        if (surfaceA) document.documentElement.style.setProperty("--surface-a", surfaceA);
        if (surfaceB) document.documentElement.style.setProperty("--surface-b", surfaceB);
        if (surfaceC) document.documentElement.style.setProperty("--surface-c", surfaceC);
        if (surfaceD) document.documentElement.style.setProperty("--surface-d", surfaceD);
        if (errorColor) document.documentElement.style.setProperty("--error-color", errorColor);
        if (validColor) document.documentElement.style.setProperty("--valid-color", validColor);
        if (navbarColor) document.documentElement.style.setProperty("--navbar-color", navbarColor);
        if (navbarColorText) document.documentElement.style.setProperty("--navbar-color-text", navbarColorText);
    }, [
        primaryColor, primaryColorText, secondaryColor,
        textColor, secondaryColorText,
        contentPadding, inlineSpacing,
        surfaceA, surfaceB, surfaceC, surfaceD,
        errorColor, validColor, navbarColor, navbarColorText
    ]);
    return <>{props.children}</>;
}

export default ThemeManager;