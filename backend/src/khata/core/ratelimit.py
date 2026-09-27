"""In-process token-bucket rate limiter (TR-SEC-05).

Limitation: buckets live in one API process, so the effective limit is
``limit × instances``. The WAF/CDN limits and the per-account lockout and OTP send
caps (which are stored in PostgreSQL) are the durable controls; this limiter only
blunts bursts. Replace with a Postgres/edge limiter when running >1 instance.
"""

from __future__ import annotations

import threading
import time
from collections.abc import Callable
from dataclasses import dataclass

from khata.core.errors import DomainError

MAX_BUCKETS = 50_000
SECONDS_PER_MINUTE = 60.0


@dataclass(slots=True)
class _Bucket:
    tokens: float
    updated: float


class RateLimiter:
    def __init__(self, clock: Callable[[], float] = time.monotonic) -> None:
        self._clock = clock
        self._buckets: dict[str, _Bucket] = {}
        self._lock = threading.Lock()

    def hit(self, key: str, per_minute: int) -> float | None:
        """Consume one token. Returns ``None`` if allowed, else seconds until a token frees."""
        capacity = float(per_minute)
        refill = capacity / SECONDS_PER_MINUTE
        now = self._clock()
        with self._lock:
            bucket = self._buckets.get(key)
            if bucket is None:
                self._evict_if_full()
                bucket = _Bucket(tokens=capacity, updated=now)
                self._buckets[key] = bucket
            bucket.tokens = min(capacity, bucket.tokens + (now - bucket.updated) * refill)
            bucket.updated = now
            if bucket.tokens >= 1.0:
                bucket.tokens -= 1.0
                return None
            return (1.0 - bucket.tokens) / refill

    def enforce(self, key: str, per_minute: int) -> None:
        retry_after = self.hit(key, per_minute)
        if retry_after is not None:
            seconds = max(1, int(retry_after + 0.999))
            raise DomainError(
                "RATE_LIMITED",
                extra={"retry_after_seconds": seconds},
                headers={"Retry-After": str(seconds)},
            )

    def reset(self) -> None:
        with self._lock:
            self._buckets.clear()

    def _evict_if_full(self) -> None:
        if len(self._buckets) < MAX_BUCKETS:
            return
        # Drop the least recently updated half; full buckets carry no state worth keeping.
        ordered = sorted(self._buckets.items(), key=lambda item: item[1].updated)
        for key, _ in ordered[: len(ordered) // 2]:
            del self._buckets[key]
