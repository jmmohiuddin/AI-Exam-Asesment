import { newCorrelationId } from './ids';
import { ApiError, errorFromResponse, networkError, SESSION_EXPIRED } from './problem';
import { clearAccessToken, getAccessToken, setAccessToken } from './tokenStore';

export const API_BASE = '/v1';
export const REFRESH_PATH = '/auth/refresh';

/** Paths where a 401 means "wrong credentials", not "token expired". */
const NO_REFRESH_PATHS = ['/auth/login', '/auth/otp/verify', '/auth/otp/resend', REFRESH_PATH, '/auth/logout'];

export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

export interface RequestOptions {
  method?: HttpMethod;
  body?: unknown;
  headers?: Record<string, string>;
  /** Send `Idempotency-Key` (use newIdempotencyKey() once per user intent). */
  idempotencyKey?: string;
  signal?: AbortSignal;
  /** Do not attach the bearer token (public endpoints). */
  anonymous?: boolean;
}

type AuthFailureListener = () => void;
const authFailureListeners = new Set<AuthFailureListener>();

/** Called when a refresh fails: the session is over and the UI must go to /login. */
export function onAuthFailure(listener: AuthFailureListener): () => void {
  authFailureListeners.add(listener);
  return () => authFailureListeners.delete(listener);
}

function notifyAuthFailure(): void {
  clearAccessToken();
  for (const listener of authFailureListeners) listener();
}

function absoluteUrl(path: string): string {
  const origin = typeof window === 'undefined' ? 'http://localhost' : window.location.origin;
  return new URL(`${API_BASE}${path}`, origin).toString();
}

function buildHeaders(options: RequestOptions): Headers {
  const headers = new Headers(options.headers);
  headers.set('Accept', 'application/json, application/problem+json');
  headers.set('X-Client', 'web');
  headers.set('X-Correlation-ID', newCorrelationId());
  if (options.body !== undefined) headers.set('Content-Type', 'application/json');
  if (options.idempotencyKey) headers.set('Idempotency-Key', options.idempotencyKey);
  const token = options.anonymous ? null : getAccessToken();
  if (token) headers.set('Authorization', `Bearer ${token}`);
  return headers;
}

async function send(path: string, options: RequestOptions): Promise<Response> {
  try {
    return await fetch(absoluteUrl(path), {
      method: options.method ?? 'GET',
      headers: buildHeaders(options),
      body: options.body === undefined ? undefined : JSON.stringify(options.body),
      credentials: 'include',
      signal: options.signal,
    });
  } catch (cause) {
    if (cause instanceof DOMException && cause.name === 'AbortError') throw cause;
    throw networkError(cause);
  }
}

async function parseBody<T>(response: Response): Promise<T> {
  if (response.status === 204) return undefined as T;
  const text = await response.text();
  if (!text) return undefined as T;
  try {
    return JSON.parse(text) as T;
  } catch (cause) {
    throw new ApiError(response.status, { code: 'INVALID_RESPONSE' }, undefined, { cause });
  }
}

interface RefreshResponse {
  access_token: string;
  expires_in: number;
}

let refreshInFlight: Promise<boolean> | null = null;

async function doRefresh(): Promise<boolean> {
  const response = await send(REFRESH_PATH, { method: 'POST', anonymous: true });
  if (!response.ok) return false;
  const body = await parseBody<RefreshResponse>(response);
  if (!body?.access_token) return false;
  setAccessToken(body.access_token);
  return true;
}

/**
 * Exchange the HttpOnly refresh cookie for a new access token. Concurrent
 * callers share one request (single flight). Resolves false when there is no
 * valid session; rejects only on network failure.
 */
export function refreshAccessToken(): Promise<boolean> {
  refreshInFlight ??= doRefresh().finally(() => {
    refreshInFlight = null;
  });
  return refreshInFlight;
}

/**
 * Typed JSON request against /v1. On 401 it refreshes once and retries;
 * if the refresh fails the session ends (listeners route to /login).
 * Errors are thrown as ApiError with the parsed problem details.
 */
export async function apiFetch<T>(path: string, options: RequestOptions = {}): Promise<T> {
  let response = await send(path, options);

  const mayRefresh = !options.anonymous && !NO_REFRESH_PATHS.includes(path);
  if (response.status === 401 && mayRefresh) {
    // A network failure here propagates as NETWORK_ERROR and keeps the session:
    // being offline is not the same as being signed out.
    const refreshed = await refreshAccessToken();
    if (!refreshed) {
      notifyAuthFailure();
      throw new ApiError(401, { code: SESSION_EXPIRED });
    }
    response = await send(path, options);
    if (response.status === 401) {
      notifyAuthFailure();
      throw await errorFromResponse(response);
    }
  }

  if (!response.ok) throw await errorFromResponse(response);
  return parseBody<T>(response);
}
