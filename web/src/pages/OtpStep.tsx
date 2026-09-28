import {
  useEffect,
  useRef,
  useState,
  type FormEvent,
  type ReactNode,
} from "react";
import { useTranslation } from "react-i18next";
import { resendOtp, verifyOtp } from "../auth/authApi";
import { describeDevice, saveDeviceId } from "../auth/device";
import { isApiError } from "../api/problem";
import { Spinner } from "../components/Spinner/Spinner";

const CODE_LENGTH = 6;
const RESEND_COOLDOWN_SECONDS = 30;

export interface OtpStepProps {
  challengeId: string;
  /** Shown back to the user so they know which number to check. */
  mobile: string;
  onVerified: (accessToken: string) => Promise<void>;
  onCancel: () => void;
}

/**
 * The second factor for a device the account has never used.
 *
 * The code is one field, not six boxes: a single input is what an SMS
 * autofill fills, what a password manager understands, and what a screen
 * reader announces once instead of six times.
 */
export function OtpStep({
  challengeId,
  mobile,
  onVerified,
  onCancel,
}: OtpStepProps): ReactNode {
  const { t, i18n } = useTranslation(["auth", "common"]);
  const [code, setCode] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [cooldown, setCooldown] = useState(RESEND_COOLDOWN_SECONDS);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  useEffect(() => {
    if (cooldown <= 0) return;
    const timer = window.setTimeout(() => setCooldown((s) => s - 1), 1000);
    return () => window.clearTimeout(timer);
  }, [cooldown]);

  function describe(error: unknown): string {
    return isApiError(error)
      ? (error.serverMessage(i18n.language) ?? error.message)
      : t("common:states.offline");
  }

  async function onSubmit(event: FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();
    setNotice(null);
    if (code.length !== CODE_LENGTH) {
      setError(t("auth:otp.incomplete"));
      return;
    }
    setError(null);
    setSubmitting(true);
    try {
      const result = await verifyOtp({
        challenge_id: challengeId,
        code,
        device_name: describeDevice(navigator.userAgent),
      });
      // Stored before the session loads: this is what skips the code next time.
      saveDeviceId(result.device_id);
      await onVerified(result.access_token);
    } catch (error) {
      setCode("");
      setError(describe(error));
      inputRef.current?.focus();
    } finally {
      setSubmitting(false);
    }
  }

  async function onResend(): Promise<void> {
    setError(null);
    setNotice(null);
    try {
      await resendOtp(challengeId);
      setCode("");
      setCooldown(RESEND_COOLDOWN_SECONDS);
      setNotice(t("auth:otp.resent"));
      inputRef.current?.focus();
    } catch (error) {
      setError(describe(error));
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
          <h1>{t("auth:otp.title")}</h1>
          <p className="hint">{t("auth:otp.newDevice")}</p>
          <p className="hint">{t("auth:otp.sent", { mobile })}</p>
        </div>

        {error ? (
          <p className="banner banner--danger" role="alert">
            {error}
          </p>
        ) : null}
        {notice ? (
          <p className="banner banner--info" role="status">
            {notice}
          </p>
        ) : null}

        <div className="field">
          <label htmlFor="otp-code">{t("auth:otp.label")}</label>
          <input
            id="otp-code"
            ref={inputRef}
            className="input"
            name="one-time-code"
            type="text"
            inputMode="numeric"
            autoComplete="one-time-code"
            maxLength={CODE_LENGTH}
            value={code}
            onChange={(e) =>
              setCode(e.target.value.replace(/\D/g, "").slice(0, CODE_LENGTH))
            }
            aria-invalid={error ? "true" : undefined}
          />
        </div>

        <button type="submit" className="button" disabled={submitting}>
          {submitting ? <Spinner label={t("auth:otp.verifying")} /> : null}
          {submitting ? t("auth:otp.verifying") : t("auth:otp.verify")}
        </button>

        <button
          type="button"
          className="button button--secondary"
          onClick={() => void onResend()}
          disabled={cooldown > 0}
        >
          {cooldown > 0
            ? t("auth:otp.resendIn", { seconds: cooldown })
            : t("auth:otp.resend")}
        </button>

        <button
          type="button"
          className="button button--secondary"
          onClick={onCancel}
        >
          {t("auth:otp.changeNumber")}
        </button>
      </form>
    </main>
  );
}
