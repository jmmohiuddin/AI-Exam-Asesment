/**
 * Pseudo-locale (en-XA) for spotting hard-coded strings, truncation and
 * concatenation bugs. Every translated string gets accented letters, ~35%
 * padding and ⟦ ⟧ brackets; interpolation placeholders are kept intact.
 */
export const PSEUDO_LOCALE = 'en-XA';

const ACCENTS: Record<string, string> = {
  a: 'á', b: 'ƀ', c: 'ç', d: 'ď', e: 'é', f: 'ƒ', g: 'ğ', h: 'ĥ', i: 'î', j: 'ĵ',
  k: 'ķ', l: 'ľ', m: 'ɱ', n: 'ñ', o: 'ö', p: 'þ', q: 'ǫ', r: 'ŕ', s: 'š', t: 'ţ',
  u: 'û', v: 'ṽ', w: 'ŵ', x: 'ẋ', y: 'ý', z: 'ž',
  A: 'Á', B: 'Ɓ', C: 'Ç', D: 'Ď', E: 'É', F: 'Ƒ', G: 'Ğ', H: 'Ĥ', I: 'Î', J: 'Ĵ',
  K: 'Ķ', L: 'Ľ', M: 'Ṁ', N: 'Ñ', O: 'Ö', P: 'Þ', Q: 'Ǫ', R: 'Ŕ', S: 'Š', T: 'Ţ',
  U: 'Û', V: 'Ṽ', W: 'Ŵ', X: 'Ẋ', Y: 'Ý', Z: 'Ž',
};

const PLACEHOLDER = /(\{\{[^}]+\}\}|\$t\([^)]*\))/;
const IS_PLACEHOLDER = /^(\{\{[^}]+\}\}|\$t\([^)]*\))$/;
const PADDING_RATIO = 0.35;

export function pseudoString(input: string): string {
  const parts = input.split(PLACEHOLDER);
  const body = parts
    .map((part) =>
      IS_PLACEHOLDER.test(part) ? part : part.replace(/[A-Za-z]/g, (ch) => ACCENTS[ch] ?? ch),
    )
    .join('');
  const pad = '~'.repeat(Math.ceil(input.length * PADDING_RATIO));
  return `⟦${body}${pad}⟧`;
}

export type Resource = { [key: string]: string | Resource };

export function pseudoResource(resource: Resource): Resource {
  return Object.fromEntries(
    Object.entries(resource).map(([key, value]) => [
      key,
      typeof value === 'string' ? pseudoString(value) : pseudoResource(value),
    ]),
  );
}
