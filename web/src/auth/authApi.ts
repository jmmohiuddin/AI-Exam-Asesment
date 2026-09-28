import { apiFetch } from "../api/client";
import type {
  LoginRequest,
  LoginResponse,
  Me,
  OtpVerifyRequest,
  OtpVerifyResponse,
  ServerPreferences,
  TokenResponse,
} from "./types";

export function login(body: LoginRequest): Promise<LoginResponse> {
  return apiFetch<LoginResponse>("/auth/login", {
    method: "POST",
    body,
    anonymous: true,
  });
}

export function verifyOtp(body: OtpVerifyRequest): Promise<OtpVerifyResponse> {
  return apiFetch<OtpVerifyResponse>("/auth/otp/verify", {
    method: "POST",
    body,
    anonymous: true,
  });
}

export function resendOtp(challengeId: string): Promise<void> {
  return apiFetch<void>("/auth/otp/resend", {
    method: "POST",
    body: { challenge_id: challengeId },
    anonymous: true,
  });
}

export function logout(): Promise<void> {
  return apiFetch<void>("/auth/logout", { method: "POST" });
}

export function getMe(): Promise<Me> {
  return apiFetch<Me>("/me");
}

export function patchPreferences(body: ServerPreferences): Promise<void> {
  return apiFetch<void>("/me/preferences", { method: "PATCH", body });
}

export function switchTenant(tenantId: string): Promise<TokenResponse> {
  return apiFetch<TokenResponse>("/auth/switch-tenant", {
    method: "POST",
    body: { tenant_id: tenantId },
  });
}
