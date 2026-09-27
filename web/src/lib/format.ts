/**
 * Number and marks formatting (05 §4.2, §4.7, §11).
 * - Marks may use Bangla digits (০–৯) or Latin digits, per setting.
 * - Absent is always "ABS", never 0.
 * - No percentages for single items.
 */

const BN_DIGITS = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'] as const;
const BN_DIGIT_RE = /[০-৯]/g;
const LATIN_DIGIT_RE = /[0-9]/g;

export type Numerals = 'bn' | 'latin';
export type NumeralSetting = 'auto' | Numerals;

export const ABSENT = 'ABS' as const;
export type MarkValue = number | typeof ABSENT | null | undefined;

export function toBanglaDigits(input: string): string {
  return input.replace(LATIN_DIGIT_RE, (d) => BN_DIGITS[Number(d)] ?? d);
}

/** Normalise Bangla digits to Latin, e.g. for OTP codes and phone numbers. */
export function toLatinDigits(input: string): string {
  return input.replace(BN_DIGIT_RE, (d) => String(d.charCodeAt(0) - 0x09e6));
}

export function resolveNumerals(setting: NumeralSetting, language: string): Numerals {
  if (setting !== 'auto') return setting;
  return language === 'bn' ? 'bn' : 'latin';
}

export interface NumberFormatOptions {
  numerals: Numerals;
  maximumFractionDigits?: number;
  useGrouping?: boolean;
}

export function formatNumber(value: number, options: NumberFormatOptions): string {
  if (!Number.isFinite(value)) throw new RangeError(`Cannot format ${value}`);
  const latin = new Intl.NumberFormat('en-US', {
    maximumFractionDigits: options.maximumFractionDigits ?? 2,
    useGrouping: options.useGrouping ?? false,
  }).format(value);
  return options.numerals === 'bn' ? toBanglaDigits(latin) : latin;
}

/** One mark: number → digits; absent → "ABS"; unknown → "—". */
export function formatMark(value: MarkValue, numerals: Numerals): string {
  if (value === ABSENT) return ABSENT;
  if (value === null || value === undefined) return '—';
  return formatNumber(value, { numerals, maximumFractionDigits: 2 });
}

/** "২/৩" or "2/3". Absent → "ABS" (the max is not shown for an absent student). */
export function formatMarkOutOf(value: MarkValue, max: number, numerals: Numerals): string {
  if (value === ABSENT) return ABSENT;
  return `${formatMark(value, numerals)}/${formatNumber(max, { numerals })}`;
}
