import bnCommon from "./bn/common.json";
import enComponents from "./en/components.json";
import bnComponents from "./bn/components.json";
import {
  htmlLang,
  i18n,
  initialLanguage,
  isLocale,
  setLocale,
  LOCALE_STORAGE_KEY,
} from ".";
import { PSEUDO_LOCALE, pseudoResource, pseudoString } from "./pseudo";

describe("i18n setup", () => {
  it("defaults to Bangla when nothing is stored", () => {
    window.localStorage.clear();
    expect(initialLanguage()).toBe("bn");
  });

  it("restores a stored language", () => {
    window.localStorage.setItem(LOCALE_STORAGE_KEY, "en");
    expect(initialLanguage()).toBe("en");
    window.localStorage.setItem(LOCALE_STORAGE_KEY, "fr");
    expect(initialLanguage()).toBe("bn");
  });

  it("picks the pseudo-locale from ?lng= outside production", () => {
    window.history.pushState({}, "", `/?lng=${PSEUDO_LOCALE}`);
    expect(initialLanguage()).toBe(PSEUDO_LOCALE);
    window.history.pushState({}, "", "/");
  });

  it("persists the language and sets <html lang>", async () => {
    await setLocale("bn");
    expect(document.documentElement.lang).toBe("bn");
    expect(window.localStorage.getItem(LOCALE_STORAGE_KEY)).toBe("bn");
    await setLocale("en");
    expect(document.documentElement.lang).toBe("en");
  });

  it("maps pseudo to an English lang attribute", () => {
    expect(htmlLang(PSEUDO_LOCALE)).toBe("en");
    expect(isLocale("bn")).toBe(true);
    expect(isLocale("xx")).toBe(false);
  });
});

describe("glossary and copy rules (05 §7, §11)", () => {
  it("uses the approved Bangla glossary terms", () => {
    expect(bnCommon.glossary).toMatchObject({
      question: "প্রশ্ন",
      stimulus: "উদ্দীপক",
      knowledge: "জ্ঞানমূলক",
      comprehension: "অনুধাবনমূলক",
      application: "প্রয়োগমূলক",
      higherOrder: "উচ্চতর দক্ষতা",
      marks: "নম্বর",
      script: "খাতা",
      recheck: "পুনর্নিরীক্ষণ",
      moderation: "মডারেশন",
    });
  });

  it("uses the approved risk labels", () => {
    expect(bnComponents.risk).toMatchObject({
      high: "সতর্কভাবে দেখুন",
      medium: "একবার দেখে নিন",
      low: "সাধারণ",
    });
    expect(enComponents.risk).toMatchObject({
      high: "Check carefully",
      medium: "Worth a look",
      low: "Looks routine",
    });
  });

  it('never says the AI "graded" or shows confidence percentages', () => {
    const all = JSON.stringify(i18n.store.data);
    expect(all).not.toMatch(/AI (graded|marked)/i);
    expect(all).not.toMatch(/confidence/i);
    expect(all).not.toMatch(/\d+\s?%/);
  });

  it('says "Your mark" / "আপনার নম্বর"', () => {
    expect(i18n.getFixedT("en")("common:marks.yourMark")).toBe("Your mark");
    expect(i18n.getFixedT("bn")("common:marks.yourMark")).toBe("আপনার নম্বর");
  });
});

describe("pseudo-locale", () => {
  it("accents, pads and brackets strings but keeps placeholders", () => {
    const out = pseudoString("Hello {{name}}");
    expect(out.startsWith("⟦Ĥéľľö {{name}}")).toBe(true);
    expect(out.endsWith("⟧")).toBe(true);
    expect(out.length).toBeGreaterThan("Hello {{name}}".length);
  });

  it("transforms nested resources", () => {
    expect(pseudoResource({ a: { b: "Hi" } })).toEqual({
      a: { b: pseudoString("Hi") },
    });
  });

  it("is registered with every namespace", () => {
    expect(i18n.getFixedT(PSEUDO_LOCALE)("nav:home")).toBe(
      pseudoString("Home"),
    );
  });
});
