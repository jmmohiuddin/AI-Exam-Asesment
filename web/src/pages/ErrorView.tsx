import type { ReactNode } from "react";
import { useTranslation } from "react-i18next";
import { isApiError, NETWORK_ERROR } from "../api/problem";

interface ErrorViewProps {
  error: unknown;
  onRetry?: () => void;
}

/**
 * Shows the server's own message when it sent one, in the reader's language.
 * The support code is always shown when present: it is what a teacher reads out
 * on the phone, and it is what ties their report to the server log.
 */
export function ErrorView({ error, onRetry }: ErrorViewProps): ReactNode {
  const { t, i18n } = useTranslation(["errors", "common"]);

  const problem = isApiError(error) ? error : null;
  const offline = problem?.code === NETWORK_ERROR;
  const message =
    problem?.serverMessage(i18n.language) ??
    (offline
      ? t("common:states.offline")
      : t("errors:unexpected", { defaultValue: "Something went wrong." }));

  return (
    <div className="centered-page">
      <div className="stack" role="alert">
        <div className="banner banner--danger">
          <p>{message}</p>
        </div>
        {problem?.supportCode ? (
          <p className="hint">
            {t("common:supportCode", { code: problem.supportCode })}
          </p>
        ) : null}
        {onRetry ? (
          <button type="button" className="button" onClick={onRetry}>
            {t("common:actions.retry")}
          </button>
        ) : null}
      </div>
    </div>
  );
}
