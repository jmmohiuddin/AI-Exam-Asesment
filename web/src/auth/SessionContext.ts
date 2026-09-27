import { createContext, useContext } from 'react';
import type { ApiError } from '../api/problem';
import type { Me, Membership, Role } from './types';

export type SessionStatus = 'loading' | 'authenticated' | 'unauthenticated' | 'error';

export interface SessionValue {
  status: SessionStatus;
  me: Me | null;
  activeMembership: Membership | null;
  roles: readonly Role[];
  /** True when the active membership holds any of the given roles. */
  hasRole: (...roles: Role[]) => boolean;
  /** Set when the session ended on its own (refresh failed), for the login notice. */
  endedByExpiry: boolean;
  error: ApiError | null;
  completeLogin: (accessToken: string) => Promise<void>;
  logout: () => Promise<void>;
  switchTenant: (tenantId: string) => Promise<void>;
  reload: () => Promise<void>;
}

export const SessionContext = createContext<SessionValue | null>(null);

export function useSession(): SessionValue {
  const value = useContext(SessionContext);
  if (!value) throw new Error('useSession must be used inside <SessionProvider>');
  return value;
}

export function activeMembershipOf(me: Me | null): Membership | null {
  if (!me || me.memberships.length === 0) return null;
  return me.memberships.find((m) => m.tenant_id === me.active_tenant_id) ?? me.memberships[0] ?? null;
}
