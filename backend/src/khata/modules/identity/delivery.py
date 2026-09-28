"""OTP delivery (TR-BE-06).

The SMS gateway is a Phase-1 dependency that does not exist yet, so there is one
sender: it writes codes to a local file for a developer to read. A deployed
environment must refuse to start rather than accept passwords and silently never
send the second factor — the same rule ``build_marking_provider`` applies to the
Fake marking provider.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from khata.core.config import Environment, Settings


@runtime_checkable
class OtpSender(Protocol):
    name: str

    def send(self, mobile: str, code: str, purpose: str) -> None:
        """Deliver one code, or raise."""
        ...


class DevFileOtpSender:
    """Appends ``<mobile> <purpose> <code>`` to a file. Dev and test only."""

    name = "dev-file"

    def __init__(self, path: Path) -> None:
        self._path = path

    @property
    def path(self) -> Path:
        return self._path

    def send(self, mobile: str, code: str, purpose: str) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(f"{mobile} {purpose} {code}\n")

    def last_code(self) -> str:
        """The most recently delivered code. Used by tests and local sign-in."""
        lines = [line for line in self._path.read_text(encoding="utf-8").splitlines() if line]
        if not lines:
            raise LookupError(f"no OTP has been delivered to {self._path}")
        return lines[-1].rsplit(" ", 1)[1]


def build_otp_sender(settings: Settings) -> OtpSender:
    if settings.env in (Environment.STAGING, Environment.PRODUCTION):
        raise RuntimeError(
            "No SMS gateway is configured; refusing to start with the dev-file OTP sender"
        )
    return DevFileOtpSender(settings.dev_otp_file)
