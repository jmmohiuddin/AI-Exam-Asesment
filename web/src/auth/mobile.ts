import { toLatinDigits } from '../lib/format';

/** Bangladeshi mobile: 01 + operator digit 3–9 + 8 digits. */
const LOCAL_RE = /^01[3-9]\d{8}$/;

/**
 * Normalise what a teacher types into E.164 (+8801XXXXXXXXX).
 * Accepts Bangla digits, spaces, dashes, and optional +880 / 880 / 0 prefixes.
 * Returns null when the input is not a valid Bangladeshi mobile number.
 */
export function normalizeMobile(input: string): string | null {
  let digits = toLatinDigits(input).replace(/[\s\-().]/g, '');
  if (digits.startsWith('+880')) digits = digits.slice(4);
  else if (digits.startsWith('880')) digits = digits.slice(3);
  if (!/^\d+$/.test(digits)) return null;
  const local = digits.startsWith('0') ? digits : `0${digits}`;
  return LOCAL_RE.test(local) ? `+88${local}` : null;
}

/** Display form: 017 1234 5678 → used in the OTP "sent to" line. */
export function displayMobile(e164: string): string {
  const local = e164.replace(/^\+88/, '');
  return `${local.slice(0, 3)} ${local.slice(3, 7)} ${local.slice(7)}`;
}
