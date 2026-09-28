/**
 * localStorage access that never throws (private mode, blocked storage).
 * Only non-secret values belong here — never tokens.
 */
export function readStorage(key: string): string | null {
  try {
    return window.localStorage.getItem(key);
  } catch {
    return null;
  }
}

export function writeStorage(key: string, value: string): boolean {
  try {
    window.localStorage.setItem(key, value);
    return true;
  } catch {
    return false;
  }
}

export function removeStorage(key: string): void {
  try {
    window.localStorage.removeItem(key);
  } catch {
    // Storage unavailable: nothing was stored, so there is nothing to remove.
  }
}

export function readJson<T>(
  key: string,
  guard: (value: unknown) => value is T,
): T | null {
  const raw = readStorage(key);
  if (raw === null) return null;
  try {
    const parsed: unknown = JSON.parse(raw);
    return guard(parsed) ? parsed : null;
  } catch {
    return null;
  }
}
