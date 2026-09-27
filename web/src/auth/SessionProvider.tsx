import { useCallback, useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { onAuthFailure, refreshAccessToken } from '../api/client';
import { ApiError, isApiError } from '../api/problem';
import { clearAccessToken, getAccessToken, setAccessToken } from '../api/tokenStore';
import * as authApi from './authApi';
import { SessionContext, activeMembershipOf, type SessionStatus, type SessionValue } from './SessionContext';
import type { Me, Role } from './types';

interface State {
  status: SessionStatus;
  me: Me | null;
  endedByExpiry: boolean;
  error: ApiError | null;
}

const SIGNED_OUT: State = { status: 'unauthenticated', me: null, endedByExpiry: false, error: null };

function toApiError(error: unknown): ApiError {
  return isApiError(error) ? error : new ApiError(0, { code: 'UNKNOWN' }, undefined, { cause: error });
}

export function SessionProvider({ children }: { children: ReactNode }): ReactNode {
  const queryClient = useQueryClient();
  const [state, setState] = useState<State>({ ...SIGNED_OUT, status: 'loading' });
  const booted = useRef(false);

  const loadMe = useCallback(async (): Promise<void> => {
    try {
      const me = await authApi.getMe();
      setState({ status: 'authenticated', me, endedByExpiry: false, error: null });
    } catch (error) {
      // 401 after a failed refresh is handled by the auth-failure listener.
      if (isApiError(error) && error.status === 401) return;
      setState({ status: 'error', me: null, endedByExpiry: false, error: toApiError(error) });
    }
  }, []);

  useEffect(
    () =>
      onAuthFailure(() => {
        queryClient.clear();
        setState({ ...SIGNED_OUT, endedByExpiry: true });
      }),
    [queryClient],
  );

  useEffect(() => {
    if (booted.current) return;
    booted.current = true;
    const boot = async (): Promise<void> => {
      if (getAccessToken()) {
        await loadMe();
        return;
      }
      try {
        const restored = await refreshAccessToken();
        if (restored) await loadMe();
        else setState(SIGNED_OUT);
      } catch {
        // Offline at start-up: we cannot restore the session, so show sign-in.
        setState(SIGNED_OUT);
      }
    };
    void boot();
  }, [loadMe]);

  const completeLogin = useCallback(
    async (accessToken: string): Promise<void> => {
      setAccessToken(accessToken);
      queryClient.clear();
      await loadMe();
    },
    [loadMe, queryClient],
  );

  const logout = useCallback(async (): Promise<void> => {
    try {
      await authApi.logout();
    } catch {
      // Sign out locally even if the server is unreachable; the refresh
      // token then expires on its idle timeout (ADR-001).
    } finally {
      clearAccessToken();
      queryClient.clear();
      setState(SIGNED_OUT);
    }
  }, [queryClient]);

  const switchTenant = useCallback(
    async (tenantId: string): Promise<void> => {
      const { access_token } = await authApi.switchTenant(tenantId);
      setAccessToken(access_token);
      queryClient.clear();
      await loadMe();
    },
    [loadMe, queryClient],
  );

  const value = useMemo<SessionValue>(() => {
    const activeMembership = activeMembershipOf(state.me);
    const roles: readonly Role[] = activeMembership?.roles ?? [];
    return {
      ...state,
      activeMembership,
      roles,
      hasRole: (...wanted: Role[]) => wanted.some((role) => roles.includes(role)),
      completeLogin,
      logout,
      switchTenant,
      reload: loadMe,
    };
  }, [state, completeLogin, logout, switchTenant, loadMe]);

  return <SessionContext value={value}>{children}</SessionContext>;
}
