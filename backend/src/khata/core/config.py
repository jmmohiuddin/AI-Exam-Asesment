"""Application settings (pydantic-settings, env prefix ``KHATA_``).

Fails fast: required secrets have no defaults, the KMS key must decode to 32 bytes,
and ``ENV=production`` rejects placeholder/dev secrets and dev-only adapters.
"""

from __future__ import annotations

import base64
import binascii
from enum import StrEnum
from functools import lru_cache
from pathlib import Path
from typing import Literal, Self

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

MIN_SECRET_BYTES = 32
KMS_KEY_BYTES = 32
# Substrings that mark a secret as a placeholder or a local development value.
INSECURE_SECRET_MARKERS = ("change_me", "changeme", "dev-", "insecure", "example", "secret")
DEV_ONLY_SMS_GATEWAYS = frozenset({"console", "memory"})

BACKEND_DIR = Path(__file__).resolve().parents[3]


class Environment(StrEnum):
    DEV = "dev"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


class ConfigurationError(RuntimeError):
    """Raised at startup when the configuration is unsafe or incomplete."""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="KHATA_",
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    env: Environment = Environment.DEV
    log_level: str = "INFO"

    database_url_app: str
    database_url_owner: str | None = None
    db_pool_size: int = Field(default=10, ge=1, le=100)
    db_statement_timeout_ms: int = Field(default=30_000, ge=1_000)

    jwt_secret: SecretStr
    otp_pepper: SecretStr
    kms_master_key: SecretStr

    access_token_ttl_seconds: int = 15 * 60
    refresh_idle_web_seconds: int = 12 * 3600
    refresh_idle_capture_seconds: int = 30 * 86400
    session_absolute_seconds: int = 90 * 86400
    step_up_ttl_seconds: int = 5 * 60

    otp_ttl_seconds: int = 5 * 60
    otp_max_attempts: int = 5
    otp_sends_per_hour: int = 5

    lockout_threshold: int = 10
    lockout_window_seconds: int = 15 * 60
    lockout_duration_seconds: int = 15 * 60

    rate_limit_ip_per_minute: int = 60
    rate_limit_account_per_minute: int = 10
    trust_forwarded_for: bool = False

    sms_gateway: Literal["console", "memory"] = "console"
    dev_otp_file: Path = Path("var/dev-otp.log")

    cors_origins: list[str] = []
    expose_docs: bool = True

    #: Password the dev seed gives every seeded account. The seed script refuses
    #: to run outside dev/test, so this never reaches a deployed database.
    seed_dev_password: str = "Khata-dev-2027!"  # noqa: S105 - dev seed only; see above

    @property
    def is_production(self) -> bool:
        return self.env == Environment.PRODUCTION

    @property
    def cookie_secure(self) -> bool:
        return self.env not in (Environment.DEV, Environment.TEST)

    def kms_master_key_bytes(self) -> bytes:
        return _decode_kms_key(self.kms_master_key.get_secret_value())

    @model_validator(mode="after")
    def _validate_security(self) -> Self:
        _decode_kms_key(self.kms_master_key.get_secret_value())
        for name in ("jwt_secret", "otp_pepper"):
            value: SecretStr = getattr(self, name)
            if len(value.get_secret_value().encode()) < MIN_SECRET_BYTES:
                raise ConfigurationError(f"{name} must be at least {MIN_SECRET_BYTES} bytes")
        if self.env in (Environment.STAGING, Environment.PRODUCTION):
            self._validate_deployed()
        return self

    def _validate_deployed(self) -> None:
        for name in ("jwt_secret", "otp_pepper", "kms_master_key"):
            value = getattr(self, name).get_secret_value().lower()
            if any(marker in value for marker in INSECURE_SECRET_MARKERS):
                raise ConfigurationError(f"{name} looks like a placeholder or dev value")
        decoded_kms = self.kms_master_key_bytes().lower()
        if any(marker.encode() in decoded_kms for marker in INSECURE_SECRET_MARKERS):
            raise ConfigurationError("kms_master_key is a placeholder value")
        if self.jwt_secret.get_secret_value() == self.otp_pepper.get_secret_value():
            raise ConfigurationError("jwt_secret and otp_pepper must differ")
        if self.sms_gateway in DEV_ONLY_SMS_GATEWAYS:
            raise ConfigurationError(f"sms_gateway={self.sms_gateway} is dev-only")
        if any(not origin.startswith("https://") for origin in self.cors_origins):
            raise ConfigurationError("cors_origins must be https in deployed environments")
        if self.is_production and self.expose_docs:
            raise ConfigurationError("expose_docs must be false in production")


def _decode_kms_key(raw: str) -> bytes:
    try:
        key = base64.b64decode(raw, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ConfigurationError("kms_master_key must be base64") from exc
    if len(key) != KMS_KEY_BYTES:
        raise ConfigurationError(f"kms_master_key must decode to {KMS_KEY_BYTES} bytes")
    return key


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]  # values come from the environment
