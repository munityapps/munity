import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import XHR from 'i18next-xhr-backend';
import LanguageDetector from 'i18next-browser-languagedetector';

// the translations
// (tip move them in a JSON file and import them)
const resources: {[key: string]: {[key:string]: string}} = { fr: {}, en: {} };
['common', 'app', 'errors'].forEach((local: string) => {
    try {
        resources.fr[local] = require(`./translations/fr/${local}.json`); // eslint-disable-line
        resources.en[local] = require(`./translations/en/${local}.json`); // eslint-disable-line
    } catch (e) {
        throw new Error(`i18n Error, the translation ${local} is not found and cannot be imported !: ${e}`);
    }
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