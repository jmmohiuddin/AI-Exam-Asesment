/**
 * Access token lives in memory only — never localStorage/sessionStorage —
 * so a script-injection bug cannot read a persisted token. The refresh token
 * is an HttpOnly cookie that JavaScript never sees.
 */
let accessToken: string | null = null;

export function getAccessToken(): string | null {
  return accessToken;
}

export function setAccessToken(token: string): void {
  if (!token) throw new Error("Refusing to store an empty access token");
  accessToken = token;
}

export function clearAccessToken(): void {
  accessToken = null;
}
