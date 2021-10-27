import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import XHR from 'i18next-xhr-backend';
import LanguageDetector from 'i18next-browser-languagedetector';

import translationFiles from './translations/index.json';

// the translations
// (tip move them in a JSON file and import them)
const resources: {[key: string]: {[key:string]: object}} = { fr: {}, en: {} };

translationFiles.forEach((langFile: {lang:string, category:string[]}) => {
    langFile.category.forEach(cat => {
        const json = require(`./translations/${langFile.lang}/${cat}.json`); // eslint-disable-line
        resources[langFile.lang][cat] = json;
    });
});

i18n
    .use(XHR)
    .use(LanguageDetector)
    .use(initReactI18next)
    .init({
        fallbackLng: 'en',
        resources,
        debug: false,
        react: {
            useSuspense: false
        },
        interpolation: {
            escapeValue: false,
            formatSeparator: ',',
            format(value, format) {
                if (format === 'uppercase') {
                    return value.toUpperCase();
                }
                return value;
            }
        }
    });

export default i18n;
