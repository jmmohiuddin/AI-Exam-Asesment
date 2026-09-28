import type { ReactNode } from "react";
import { useTranslation } from "react-i18next";

/** A busy indicator that announces itself; never a bare animated div. */
export function Spinner({ label }: { label?: string }): ReactNode {
  const { t } = useTranslation();
  return (
    <span role="status">
      <span className="spinner" aria-hidden="true" />
      <span className="visually-hidden">{label ?? t("states.loading")}</span>
    </span>
  );
}

export function FullPageSpinner(): ReactNode {
  return (
    <div className="spinner--page">
      <Spinner />
    </div>
  );
}
