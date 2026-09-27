import i18next from 'i18next';
import { initReactI18next } from 'react-i18next';
import bnCommon from './bn/common.json';
import bnNav from './bn/nav.json';
import bnAuth from './bn/auth.json';
import bnErrors from './bn/errors.json';
import bnHome from './bn/home.json';
import bnPages from './bn/pages.json';
import bnComponents from './bn/components.json';
import enCommon from './en/common.json';
import enNav from './en/nav.json';
import enAuth from './en/auth.json';
import enErrors from './en/errors.json';
import enHome from './en/home.json';
import enPages from './en/pages.json';
import enComponents from './en/components.json';
import { PSEUDO_LOCALE, pseudoResource } from './pseudo';
import { readStorage, writeStorage } from '../lib/storage';

export const SUPPORTED_LOCALES = ['bn', 'en'] as const;
export type Locale = (typeof SUPPORTED_LOCALES)[number];
export const DEFAULT_LOCALE: Locale = 'bn';
export const LOCALE_STORAGE_KEY = 'khata.locale';
export const NAMESPACES = ['common', 'nav', 'auth', 'errors', 'home', 'pages', 'components'] as const;

const en = {
  common: enCommon,
  nav: enNav,
  auth: enAuth,
  errors: enErrors,
  home: enHome,
  pages: enPages,
  components: enComponents,
};

const bn = {
  common: bnCommon,
  nav: bnNav,
  auth: bnAuth,
  errors: bnErrors,
  home: bnHome,
  pages: bnPages,
  components: bnComponents,
};

const pseudoEnabled = import.meta.env.MODE !== 'production';

function pseudoBundle(): Record<string, ReturnType<typeof pseudoResource>> {
  return Object.fromEntries(Object.entries(en).map(([ns, res]) => [ns, pseudoResource(res)]));
}

export function isLocale(value: unknown): value is Locale {
  return typeof value === 'string' && (SUPPORTED_LOCALES as readonly string[]).includes(value);
}

/** Resolve the start-up language: ?lng= (pseudo, dev only) → stored → Bangla. */
export function initialLanguage(): string {
  const fromQuery =
    typeof window === 'undefined' ? null : new URLSearchParams(window.location.search).get('lng');
  if (pseudoEnabled && fromQuery === PSEUDO_LOCALE) return PSEUDO_LOCALE;
  const stored = readStorage(LOCALE_STORAGE_KEY);
  return isLocale(stored) ? stored : DEFAULT_LOCALE;
}

/** BCP-47 tag used for the `lang` attribute and Intl APIs. */
export function htmlLang(language: string): Locale {
  return language === 'bn' ? 'bn' : 'en';
}

export const i18n = i18next.createInstance();

void i18n.use(initReactI18next).init({
  resources: {
    bn,
    en,
    ...(pseudoEnabled ? { [PSEUDO_LOCALE]: pseudoBundle() } : {}),
  },
  lng: initialLanguage(),
  fallbackLng: 'en',
  supportedLngs: pseudoEnabled ? [...SUPPORTED_LOCALES, PSEUDO_LOCALE] : [...SUPPORTED_LOCALES],
  ns: [...NAMESPACES],
  defaultNS: 'common',
  interpolation: { escapeValue: false },
  returnNull: false,
  initAsync: false,
  react: { useSuspense: false },
});

function syncDocumentLang(language: string): void {
  if (typeof document !== 'undefined') {
    document.documentElement.lang = htmlLang(language);
  }
}

syncDocumentLang(i18n.language);
i18n.on('languageChanged', syncDocumentLang);

/** Change the UI language and remember it on this device. */
export async function setLocale(locale: Locale): Promise<void> {
  writeStorage(LOCALE_STORAGE_KEY, locale);
  await i18n.changeLanguage(locale);
}

export { PSEUDO_LOCALE };
