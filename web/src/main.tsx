import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "@fontsource/noto-sans/400.css";
import "@fontsource/noto-sans/500.css";
import "@fontsource/noto-sans/600.css";
import "@fontsource/noto-sans-bengali/400.css";
import "@fontsource/noto-sans-bengali/500.css";
import "@fontsource/noto-sans-bengali/600.css";
import "./styles/tokens.css";
import "./styles/app.css";
import "./i18n";
import { App } from "./app/App";

const container = document.getElementById("root");
if (!container) throw new Error("#root is missing from index.html");

function mount(): void {
  createRoot(container!).render(
    <StrictMode>
      <App />
    </StrictMode>,
  );
}

/**
 * Start MSW before the first render when `pnpm dev:mock` is running.
 *
 * The import is dynamic and guarded by a compile-time constant, so the mock
 * handlers are tree-shaken out of a production build entirely rather than
 * shipped and merely left unregistered.
 */
if (import.meta.env.VITE_USE_MOCKS === "1") {
  void import("./mocks/browser")
    .then(({ worker }) =>
      worker.start({ onUnhandledRequest: "bypass", quiet: true }),
    )
    .finally(mount);
} else {
  mount();
}
