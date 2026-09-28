import { setupWorker } from "msw/browser";
import { handlers } from "./handlers";

/** Browser worker for `pnpm dev:mock`. Never registered in a production build. */
export const worker = setupWorker(...handlers);
