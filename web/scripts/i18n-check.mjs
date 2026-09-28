/**
 * Fails when the Bangla and English bundles have drifted apart.
 *
 * Bangla is the default language, so a key that exists only in English silently
 * renders English text to a Bangla-speaking teacher. That is a product defect,
 * not a translation nicety, so it fails the build.
 *
 *   node scripts/i18n-check.mjs
 */

import { readdirSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const I18N_DIR = resolve(HERE, "..", "src", "i18n");
const LOCALES = ["bn", "en"];

/** Every leaf path in a nested resource, as dotted keys. */
function leafKeys(value, prefix = "") {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    return [prefix];
  }
  return Object.entries(value).flatMap(([key, child]) =>
    leafKeys(child, prefix ? `${prefix}.${key}` : key),
  );
}

function namespacesOf(locale) {
  const dir = join(I18N_DIR, locale);
  return readdirSync(dir)
    .filter((name) => name.endsWith(".json"))
    .map((name) => name.replace(/\.json$/, ""))
    .sort();
}

function load(locale, namespace) {
  return JSON.parse(
    readFileSync(join(I18N_DIR, locale, `${namespace}.json`), "utf8"),
  );
}

/** i18next interpolation placeholders, which must match across locales. */
function placeholders(text) {
  if (typeof text !== "string") return [];
  return [...text.matchAll(/\{\{\s*([\w.]+)\s*\}\}/g)].map((m) => m[1]).sort();
}

function flatten(value, prefix = "", into = new Map()) {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    into.set(prefix, value);
    return into;
  }
  for (const [key, child] of Object.entries(value)) {
    flatten(child, prefix ? `${prefix}.${key}` : key, into);
  }
  return into;
}

const problems = [];

const [base, ...others] = LOCALES;
const baseNamespaces = namespacesOf(base);

for (const locale of others) {
  const theirs = namespacesOf(locale);
  for (const missing of baseNamespaces.filter((ns) => !theirs.includes(ns))) {
    problems.push(`${locale}: missing namespace ${missing}.json`);
  }
  for (const extra of theirs.filter((ns) => !baseNamespaces.includes(ns))) {
    problems.push(`${base}: missing namespace ${extra}.json`);
  }
}

for (const namespace of baseNamespaces) {
  const bundles = new Map(
    LOCALES.map((locale) => [locale, flatten(load(locale, namespace))]),
  );
  const allKeys = new Set([...bundles.values()].flatMap((m) => [...m.keys()]));

  for (const key of [...allKeys].sort()) {
    const present = LOCALES.filter((locale) => bundles.get(locale).has(key));
    if (present.length !== LOCALES.length) {
      const absent = LOCALES.filter((locale) => !present.includes(locale));
      problems.push(`${namespace}.${key}: missing in ${absent.join(", ")}`);
      continue;
    }
    const signatures = LOCALES.map((locale) =>
      placeholders(bundles.get(locale).get(key)).join(","),
    );
    if (new Set(signatures).size > 1) {
      problems.push(
        `${namespace}.${key}: placeholders differ (${LOCALES.map(
          (locale, i) => `${locale}=[${signatures[i]}]`,
        ).join(" ")})`,
      );
    }
  }
}

const totalKeys = baseNamespaces.reduce(
  (sum, ns) => sum + leafKeys(load(base, ns)).length,
  0,
);

if (problems.length > 0) {
  console.error(`i18n check failed (${problems.length} problems):`);
  for (const problem of problems) console.error(`  ${problem}`);
  process.exit(1);
}

console.log(
  `i18n OK — ${totalKeys} keys across ${baseNamespaces.length} namespaces, ${LOCALES.join(" and ")} in step.`,
);
