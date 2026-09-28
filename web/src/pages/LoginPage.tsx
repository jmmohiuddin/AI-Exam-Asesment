import { useState, type FormEvent, type ReactNode } from "react";
import { useTranslation } from "react-i18next";
import { Navigate, useLocation } from "react-router";
import { login } from "../auth/authApi";
import { normalizeMobile } from "../auth/mobile";
import { useSession } from "../auth/SessionContext";
import type { LoginLocationState } from "../auth/RequireAuth";
import { isApiError } from "../api/problem";
import { Spinner } from "../components/Spinner/Spinner";

export function LoginPage(): ReactNode {
  const { t, i18n } = useTranslation(["auth", "common"]);
  const session = useSession();
  const location = useLocation();

  const [mobile, setMobile] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [fieldError, setFieldError] = useState<string | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  if (session.status === "authenticated") {
    const from = (location.state as LoginLocationState | null)?.from;
    return <Navigate to={from ?? "/"} replace />;
  }

  async function onSubmit(event: FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();
    setFormError(null);

    const e164 = normalizeMobile(mobile);
    if (!e164) {
      setFieldError(
        mobile.trim() ? t("auth:mobile.invalid") : t("auth:mobile.required"),
      );
      return;
    }
    if (!password) {
      setFieldError(null);
      setFormError(t("auth:password.required"));
      return;
    }
    setFieldError(null);

    setSubmitting(true);
    try {
      const result = await login({ mobile: e164, password });
      if (result.status === "ok") {
        await session.completeLogin(result.access_token);
        return;
      }
      // OTP sign-in is specified but not built yet; say so rather than fail silently.
      setFormError(t("auth:otp.newDevice"));
    } catch (error) {
      setFormError(
        isApiError(error)
          ? (error.serverMessage(i18n.language) ?? error.message)
          : t("common:states.offline"),
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="centered-page" id="main">
      <form
        className="card stack"
        onSubmit={(e) => void onSubmit(e)}
        noValidate
      >
        <div>
          <h1>{t("auth:title")}</h1>
          <p className="hint">{t("auth:subtitle")}</p>
        </div>

        {session.endedByExpiry ? (
          <p className="banner banner--info">{t("auth:sessionEnded")}</p>
        ) : null}

        {formError ? (
          <p className="banner banner--danger" role="alert">
            {formError}
          </p>
        ) : null}

        <div className="field">
          <label htmlFor="mobile">{t("auth:mobile.label")}</label>
          <input
            id="mobile"
            className="input"
            name="mobile"
            type="tel"
            inputMode="tel"
            autoComplete="username"
            value={mobile}
            onChange={(e) => setMobile(e.target.value)}
            aria-invalid={fieldError ? "true" : undefined}
            aria-describedby={fieldError ? "mobile-error" : "mobile-hint"}
          />
          {fieldError ? (
            <p className="hint" id="mobile-error" role="alert">
              {fieldError}
            </p>
          ) : (
            <p className="hint" id="mobile-hint">
              {t("auth:mobile.hint")}
            </p>
          )}
        </div>

        <div className="field">
          <label htmlFor="password">{t("auth:password.label")}</label>
          <input
            id="password"
            className="input"
            name="password"
            type={showPassword ? "text" : "password"}
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button
            type="button"
            className="button button--secondary"
            onClick={() => setShowPassword((shown) => !shown)}
          >
            {showPassword ? t("auth:password.hide") : t("auth:password.show")}
          </button>
        </div>

        <button type="submit" className="button" disabled={submitting}>
          {submitting ? <Spinner label={t("auth:submitting")} /> : null}
          {submitting ? t("auth:submitting") : t("auth:submit")}
        </button>

        <details>
          <summary>{t("auth:forgot")}</summary>
          <p className="hint">{t("auth:forgotHelp")}</p>
        </details>
      </form>
    </main>
  );
}
