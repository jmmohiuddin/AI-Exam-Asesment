/**
 * RFC 9457 problem details, as the Khata API sends them:
 * { type, title, status, detail, code, message_bn, message_en, support_code, errors[] }
 */
export interface FieldError {
  field?: string;
  code?: string;
  message_bn?: string;
  message_en?: string;
  message?: string;
}

export interface ProblemDetails {
  type?: string;
  title?: string;
  status?: number;
  detail?: string;
  code?: string;
  message_bn?: string;
  message_en?: string;
  support_code?: string;
  errors?: FieldError[];
  retry_after_seconds?: number;
}

export const NETWORK_ERROR = "NETWORK_ERROR";
export const SESSION_EXPIRED = "SESSION_EXPIRED";

export class ApiError extends Error {
  readonly status: number;
  readonly code: string;
  readonly title: string | undefined;
  readonly detail: string | undefined;
  readonly type: string | undefined;
  readonly messageBn: string | undefined;
  readonly messageEn: string | undefined;
  readonly supportCode: string | undefined;
  readonly errors: readonly FieldError[];
  readonly retryAfterSeconds: number | undefined;

  constructor(
    status: number,
    problem: ProblemDetails,
    retryAfterHeader?: number,
    options?: { cause?: unknown },
  ) {
    super(
      problem.detail ?? problem.title ?? `Request failed with status ${status}`,
      options,
    );
    this.name = "ApiError";
    this.status = status;
    this.code = problem.code ?? codeForStatus(status);
    this.title = problem.title;
    this.detail = problem.detail;
    this.type = problem.type;
    this.messageBn = problem.message_bn;
    this.messageEn = problem.message_en;
    this.supportCode = problem.support_code;
    this.errors = Object.freeze([...(problem.errors ?? [])]);
    this.retryAfterSeconds = problem.retry_after_seconds ?? retryAfterHeader;
  }

  /** The server's message in the given language, if it sent one. */
  serverMessage(language: string): string | undefined {
    return language === "bn"
      ? (this.messageBn ?? this.messageEn)
      : (this.messageEn ?? this.messageBn);
  }
}

export function isApiError(value: unknown): value is ApiError {
  return value instanceof ApiError;
}

function codeForStatus(status: number): string {
  if (status === 0) return NETWORK_ERROR;
  if (status === 401) return SESSION_EXPIRED;
  if (status === 403) return "FORBIDDEN";
  if (status >= 500) return "SERVER_ERROR";
  return "UNKNOWN";
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function optionalString(value: unknown): string | undefined {
  return typeof value === "string" && value.length > 0 ? value : undefined;
}

function optionalNumber(value: unknown): number | undefined {
  return typeof value === "number" && Number.isFinite(value)
    ? value
    : undefined;
}

/** Validate untrusted JSON into ProblemDetails, dropping anything malformed. */
export function toProblem(body: unknown): ProblemDetails {
  if (!isRecord(body)) return {};
  const errors = Array.isArray(body.errors)
    ? body.errors.filter(isRecord).map((e): FieldError => ({
        field: optionalString(e.field),
        code: optionalString(e.code),
        message_bn: optionalString(e.message_bn),
        message_en: optionalString(e.message_en),
        message: optionalString(e.message),
      }))
    : undefined;
  return {
    type: optionalString(body.type),
    title: optionalString(body.title),
    status: optionalNumber(body.status),
    detail: optionalString(body.detail),
    code: optionalString(body.code),
    message_bn: optionalString(body.message_bn),
    message_en: optionalString(body.message_en),
    support_code: optionalString(body.support_code),
    errors,
    retry_after_seconds: optionalNumber(body.retry_after_seconds),
  };
}

function parseRetryAfter(header: string | null): number | undefined {
  if (!header) return undefined;
  const seconds = Number(header);
  if (Number.isFinite(seconds) && seconds >= 0) return seconds;
  const date = Date.parse(header);
  return Number.isNaN(date)
    ? undefined
    : Math.max(0, Math.round((date - Date.now()) / 1000));
}

export async function errorFromResponse(response: Response): Promise<ApiError> {
  let body: unknown = null;
  try {
    body = await response.json();
  } catch {
    body = null; // Non-JSON error body (e.g. proxy HTML page): status alone decides.
  }
  return new ApiError(
    response.status,
    toProblem(body),
    parseRetryAfter(response.headers.get("Retry-After")),
  );
}

export function networkError(cause: unknown): ApiError {
  return new ApiError(0, { code: NETWORK_ERROR }, undefined, { cause });
}
