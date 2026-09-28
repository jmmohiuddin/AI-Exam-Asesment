import {
  ABSENT,
  formatMark,
  formatMarkOutOf,
  formatNumber,
  resolveNumerals,
  toBanglaDigits,
  toLatinDigits,
} from "./format";

describe("digit conversion", () => {
  it("converts Latin digits to Bangla and back", () => {
    expect(toBanglaDigits("0123456789")).toBe("০১২৩৪৫৬৭৮৯");
    expect(toLatinDigits("০১২৩৪৫৬৭৮৯")).toBe("0123456789");
  });

  it("leaves other characters untouched", () => {
    expect(toLatinDigits("০১৭-১২ abc")).toBe("017-12 abc");
    expect(toBanglaDigits("Q2 (গ)")).toBe("Q২ (গ)");
  });
});

describe("resolveNumerals", () => {
  it("follows the language when set to auto", () => {
    expect(resolveNumerals("auto", "bn")).toBe("bn");
    expect(resolveNumerals("auto", "en")).toBe("latin");
  });

  it("respects an explicit setting", () => {
    expect(resolveNumerals("latin", "bn")).toBe("latin");
    expect(resolveNumerals("bn", "en")).toBe("bn");
  });
});

describe("formatNumber", () => {
  it("formats with Bangla digits", () => {
    expect(formatNumber(12.5, { numerals: "bn" })).toBe("১২.৫");
  });

  it("does not group by default and rounds to 2 decimals", () => {
    expect(formatNumber(1234.567, { numerals: "latin" })).toBe("1234.57");
  });

  it("rejects non-finite values", () => {
    expect(() => formatNumber(Number.NaN, { numerals: "latin" })).toThrow(
      RangeError,
    );
  });
});

describe("marks", () => {
  it("shows ABS for absent, never 0", () => {
    expect(formatMark(ABSENT, "bn")).toBe("ABS");
    expect(formatMarkOutOf(ABSENT, 3, "latin")).toBe("ABS");
  });

  it("shows a dash for an unknown mark", () => {
    expect(formatMark(null, "latin")).toBe("—");
    expect(formatMark(undefined, "bn")).toBe("—");
  });

  it("formats x/y in the chosen numerals", () => {
    expect(formatMarkOutOf(2, 3, "bn")).toBe("২/৩");
    expect(formatMarkOutOf(0, 3, "latin")).toBe("0/3");
    expect(formatMarkOutOf(2.5, 10, "latin")).toBe("2.5/10");
  });
});
