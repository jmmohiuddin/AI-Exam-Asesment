/** Auth contract types (backend /v1/auth/*, /v1/me). */

export type Role =
  | 'org_owner'
  | 'school_admin'
  | 'exam_coordinator'
  | 'hod'
  | 'teacher'
  | 'capture_operator'
  | 'principal';

export interface AuthUser {
  id: string;
  name: string;
  locale: string;
}

export interface LoginRequest {
  mobile: string;
  password: string;
  device_id?: string;
}

export interface LoginOtpRequired {
  status: 'otp_required';
  challenge_id: string;
  otp_expires_at: string;
}

export interface LoginOk {
  status: 'ok';
  access_token: string;
  expires_in: number;
  user: AuthUser;
}

export type LoginResponse = LoginOtpRequired | LoginOk;

export interface OtpVerifyRequest {
  challenge_id: string;
  code: string;
  device_name: string;
}

export interface OtpVerifyResponse {
  status: 'ok';
  access_token: string;
  expires_in: number;
  device_id: string;
  user: AuthUser;
}

export interface TokenResponse {
  access_token: string;
  expires_in: number;
}

export interface Membership {
  tenant_id: string;
  org_name: string;
  school_id: string;
  school_name_bn: string;
  school_name_en: string;
  roles: Role[];
}

export type Density = 'comfortable' | 'compact';

export interface ServerPreferences {
  locale?: string;
  dim_mode?: boolean;
  density?: Density;
}

export interface Me {
  id: string;
  name: string;
  mobile_masked: string;
  locale: string;
  preferences: ServerPreferences | null;
  platform_role: string | null;
  memberships: Membership[];
  active_tenant_id: string | null;
}
