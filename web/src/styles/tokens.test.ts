import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { contrastRatio, WCAG_TEXT, WCAG_UI, parseHex, relativeLuminance } from '../lib/contrast';

const css = readFileSync(resolve(__dirname, 'tokens.css'), 'utf8');

function block(selector: string): string {
  const start = css.indexOf(`${selector} {`);
  if (start < 0) throw new Error(`missing ${selector}`);
  return css.slice(start, css.indexOf('\n}', start));
}

function colours(source: string): Record<string, string> {
  const out: Record<string, string> = {};
  for (const m of source.matchAll(/--(color-[a-z-]+):\s*(#[0-9a-f]{3,6});/gi)) {
    out[m[1] as string] = m[2] as string;
  }
  return out;
}

const light = colours(block(':root'));
const dim = { ...light, ...colours(block("[data-dim='true']")) };

type Pair = [fg: string, bg: string];

const TEXT_PAIRS: Pair[] = [
  ['text', 'bg'],
  ['text', 'surface'],
  ['text', 'surface-sunken'],
  ['text', 'chip-bg'],
  ['text', 'primary-subtle'],
  ['text-muted', 'bg'],
  ['text-muted', 'surface'],
  ['on-primary', 'primary'],
  ['on-primary', 'primary-hover'],
  ['on-primary', 'primary-active'],
  ['on-danger', 'danger'],
  ['on-danger', 'danger-hover'],
  ['primary-text', 'bg'],
  ['primary-text', 'surface'],
  ['primary-text', 'primary-subtle'],
  ['criterion-met', 'surface'],
  ['criterion-partly-text', 'surface'],
  ['criterion-not', 'surface'],
  ['criterion-unknown', 'surface'],
  ['risk-high-text', 'risk-high-bg'],
  ['risk-medium-text', 'risk-medium-bg'],
  ['risk-low-text', 'risk-low-bg'],
  ['ai-level-text', 'ai-level-bg'],
  ['verify-text', 'verify-bg'],
  ['text', 'info-bg'],
  ['text', 'warning-bg'],
  ['text', 'danger-bg'],
  ['text', 'masked-bg'],
  ['text', 'instruction-bg'],
];

const UI_PAIRS: Pair[] = [
  ['border-strong', 'surface'],
  ['border-strong', 'bg'],
  ['focus', 'bg'],
  ['focus', 'surface'],
  ['primary', 'bg'],
  ['primary', 'surface'],
  ['criterion-met', 'bg'],
  ['criterion-partly', 'surface'],
  ['criterion-partly', 'bg'],
  ['criterion-not', 'bg'],
  ['criterion-unknown', 'bg'],
  ['risk-high', 'risk-high-bg'],
  ['risk-medium', 'risk-medium-bg'],
  ['risk-low', 'risk-low-bg'],
  ['ai-level', 'ai-level-bg'],
  ['verify', 'verify-bg'],
  ['info', 'info-bg'],
  ['warning', 'warning-bg'],
  ['danger', 'danger-bg'],
  ['masked', 'masked-bg'],
  ['instruction', 'instruction-bg'],
];

function check(palette: Record<string, string>, pairs: Pair[], min: number): string[] {
  return pairs.flatMap(([fg, bg]) => {
    const f = palette[`color-${fg}`];
    const b = palette[`color-${bg}`];
    if (!f || !b) return [`missing token ${!f ? fg : bg}`];
    const ratio = contrastRatio(f, b);
    return ratio >= min ? [] : [`${fg} on ${bg}: ${ratio.toFixed(2)} < ${min}`];
  });
}

describe('contrast helpers', () => {
  it('computes known WCAG reference ratios', () => {
    expect(contrastRatio('#000000', '#ffffff')).toBeCloseTo(21, 5);
    expect(contrastRatio('#fff', '#fff')).toBe(1);
    expect(relativeLuminance('#ffffff')).toBe(1);
    expect(parseHex('#0F6E6E')).toEqual([15, 110, 110]);
  });

  it('rejects malformed colours', () => {
    expect(() => parseHex('teal')).toThrow('Not a hex colour');
  });
});

describe('design tokens', () => {
  it('keeps the fixed hex values from 05 §4.3', () => {
    expect(light['color-bg']).toBe('#fafaf7');
    expect(light['color-text']).toBe('#1f2328');
    expect(light['color-primary']).toBe('#0f6e6e');
    expect(light['color-criterion-met']).toBe('#2e7d32');
    expect(light['color-criterion-partly']).toBe('#b26a00');
    expect(light['color-criterion-not']).toBe('#b3261e');
    expect(light['color-criterion-unknown']).toBe('#5f6b7a');
  });

  it.each([
    ['light', light],
    ['dim', dim],
  ])('%s palette: text pairs meet 4.5:1', (_name, palette) => {
    expect(check(palette, TEXT_PAIRS, WCAG_TEXT)).toEqual([]);
  });

  it.each([
    ['light', light],
    ['dim', dim],
  ])('%s palette: UI glyph pairs meet 3:1', (_name, palette) => {
    expect(check(palette, UI_PAIRS, WCAG_UI)).toEqual([]);
  });

  it('never uses a green hue for AI level', () => {
    const [r, g, b] = parseHex(light['color-ai-level'] as string);
    expect(g).toBeLessThanOrEqual(Math.max(r, b));
  });

  it('defines the spacing, radius and motion scale from 05 §4.1', () => {
    for (const v of ['4px', '8px', '12px', '16px', '24px', '32px', '48px']) {
      expect(css).toContain(`: ${v};`);
    }
    expect(css).toContain('--radius-control: 6px');
    expect(css).toContain('--radius-card: 10px');
    expect(css).toContain('--radius-sheet: 16px');
    expect(css).toContain('--motion-micro: 120ms');
    expect(css).toContain('--motion-panel: 200ms');
    expect(css).toContain('--focus-width: 2px');
    expect(css).toContain('--focus-offset: 2px');
  });
});
