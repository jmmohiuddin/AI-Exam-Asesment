import type { ReactNode } from "react";
import { Navigate, Outlet, useLocation } from "react-router";
import { useSession } from "./SessionContext";
import { FullPageSpinner } from "../components/Spinner/Spinner";
import { ErrorView } from "../pages/ErrorView";
import type { Role } from "./types";

interface RequireAuthProps {
  /** When given, the active membership must hold at least one of these roles. */
  roles?: Role[];
  children?: ReactNode;
}

export interface LoginLocationState {
  from?: string;
}

/** Route guard: signed-in users pass; others go to /login and come back after. */
export function RequireAuth({ roles, children }: RequireAuthProps): ReactNode {
  const session = useSession();
  const location = useLocation();

  if (session.status === "loading") return <FullPageSpinner />;
  if (session.status === "error") {
    return (
      <ErrorView error={session.error} onRetry={() => void session.reload()} />
    );
  }
  if (session.status === "unauthenticated") {
    const state: LoginLocationState = {
      from: `${location.pathname}${location.search}`,
    };
    return <Navigate to="/login" replace state={state} />;
  }
  if (roles && !session.hasRole(...roles)) return <Navigate to="/" replace />;
  return children ?? <Outlet />;
}
