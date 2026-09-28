import { setupServer } from "msw/node";
import { handlers } from "./handlers";

/** Node-side MSW server used by vitest (started in src/test/setup.ts). */
export const server = setupServer(...handlers);
