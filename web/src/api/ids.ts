/** Random identifiers for correlation and idempotency headers. */
export function randomId(): string {
  if (
    typeof crypto !== "undefined" &&
    typeof crypto.randomUUID === "function"
  ) {
    return crypto.randomUUID();
  }
  // Fallback for non-secure contexts (http on a LAN IP): still random, not secret.
  const bytes = new Uint8Array(16);
  crypto.getRandomValues(bytes);
  return Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join("");
}

export const newCorrelationId = randomId;

/**
 * Create one key per user intent (e.g. per "Create exam" submission) and
 * reuse it on retries so the server applies the create at most once.
 */
export const newIdempotencyKey = randomId;
