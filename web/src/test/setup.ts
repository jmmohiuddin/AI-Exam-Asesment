import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterAll, afterEach, beforeAll } from "vitest";
import { server } from "../mocks/server";
import { resetMockState } from "../mocks/handlers";
import { i18n } from "../i18n";
import { clearAccessToken } from "../api/tokenStore";

beforeAll(() => {
  server.listen({ onUnhandledRequest: "error" });
});

afterEach(async () => {
  cleanup();
  server.resetHandlers();
  resetMockState();
  clearAccessToken();
  window.localStorage.clear();
  window.sessionStorage.clear();
  await i18n.changeLanguage("en");
});

afterAll(() => {
  server.close();
});

// jsdom lacks these; Radix primitives and our layout code query them.
if (!window.matchMedia) {
  window.matchMedia = (query: string): MediaQueryList =>
    ({
      matches: false,
      media: query,
      onchange: null,
      addListener: () => undefined,
      removeListener: () => undefined,
      addEventListener: () => undefined,
      removeEventListener: () => undefined,
      dispatchEvent: () => false,
    }) as MediaQueryList;
}

// Assigning prototype methods is exactly what a jsdom polyfill does; the
// unbound-method rule is about passing them around, which we never do.
/* eslint-disable @typescript-eslint/unbound-method */
class ResizeObserverStub {
  observe(): void {}
  unobserve(): void {}
  disconnect(): void {}
}
globalThis.ResizeObserver ??=
  ResizeObserverStub as unknown as typeof ResizeObserver;
Element.prototype.scrollIntoView ??= function scrollIntoView(): void {};
Element.prototype.hasPointerCapture ??= function hasPointerCapture(): boolean {
  return false;
};
Element.prototype.releasePointerCapture ??=
  function releasePointerCapture(): void {};
