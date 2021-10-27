import { useEffect } from 'react';

import {  useAppSelector } from '../hooks';

const ThemeManager = (props: { children: object }) => {
    const { primaryColor, primaryColorText, secondaryColor,
        textColor, textColorSecondary,
        contentPadding, inlineSpacing,
        surfaceA, surfaceB, surfaceC, surfaceD,
        errorColor, validColor,
    } = useAppSelector(state => state.layout);

    useEffect(() => {
        if (primaryColor) document.documentElement.style.setProperty("--primary-color", primaryColor);
        if (primaryColorText) document.documentElement.style.setProperty("--primary-color-text", primaryColorText);
        if (secondaryColor) document.documentElement.style.setProperty("--secondary-color", secondaryColor);
        if (textColor) document.documentElement.style.setProperty("--text-color", textColor);
        if (textColorSecondary) document.documentElement.style.setProperty("--text-color-secondary", textColorSecondary);
        if (contentPadding) document.documentElement.style.setProperty("--content-padding", contentPadding);
        if (inlineSpacing) document.documentElement.style.setProperty("--inline-spacing", inlineSpacing);
        if (surfaceA) document.documentElement.style.setProperty("--surface-a", surfaceA);
        if (surfaceB) document.documentElement.style.setProperty("--surface-b", surfaceB);
        if (surfaceC) document.documentElement.style.setProperty("--surface-c", surfaceC);
        if (surfaceD) document.documentElement.style.setProperty("--surface-d", surfaceD);
        if (errorColor) document.documentElement.style.setProperty("--error-color", errorColor);
        if (validColor) document.documentElement.style.setProperty("--valid-color", validColor);
    }, [
        primaryColor, primaryColorText, secondaryColor,
        textColor, textColorSecondary,
        contentPadding, inlineSpacing,
        surfaceA, surfaceB, surfaceC, surfaceD,
        errorColor, validColor,
    ]);
    return <>{props.children}</>;
}

export default ThemeManager;