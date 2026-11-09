# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""A bounded, thread-safe result cache with stale-while-revalidate semantics.

Used for local-dashboard placement runs (``/api/report-specs/execute`` with ``cache: true``): every
placement runs a report that can take 20-35 s because each run hits Egeria, so a revisit should be
instant and refresh in the background.

States (``lookup``):
  fresh -- stored less than ``ttl`` seconds ago: return it, run nothing.
  stale -- older than ``ttl`` but younger than ``max_stale``: return it now and refresh once in the
           background (``claim_refresh`` is true for exactly one caller per key until it is released).
  miss  -- absent, or older than ``max_stale``: the caller runs the report itself.

Same shape as operations_handler's non-blocking cache: the check-and-claim is atomic (one lock), so
two requests for the same key can never both start a refresh. The store is LRU-bounded, so memory
cannot grow without limit. Callers store only successful results: an error, a refusal or a token
failure is never put here.

Sync on purpose: ``execute_spec`` is a sync route (it runs in a worker thread), so a ``threading``
lock is the right primitive and no asyncio loop is involved.
"""
import threading
import time
from collections import OrderedDict
from typing import Any, Callable, Hashable, Optional, Tuple

FRESH, STALE, MISS = "fresh", "stale", "miss"


class ResultCache:
    def __init__(self, ttl: float = 300.0, max_stale: float = 3600.0, max_entries: int = 256,
                 refresh_backoff: float = 30.0, clock: Callable[[], float] = time.time):
        self.ttl = ttl
        self.max_stale = max_stale
        self.max_entries = max_entries
        self.refresh_backoff = refresh_backoff
        self._clock = clock
        self._lock = threading.Lock()
        self._data: "OrderedDict[Hashable, Tuple[Any, float]]" = OrderedDict()
        self._refreshing: set = set()
        self._failed_at: dict = {}

    def lookup(self, key) -> Tuple[str, Any, Optional[float]]:
        """(state, value, stored_at). Touches the entry's LRU position on a hit."""
        with self._lock:
            entry = self._data.get(key)
            if entry is None:
                return MISS, None, None
            value, stored_at = entry
            age = self._clock() - stored_at
            if age >= self.max_stale:
                del self._data[key]
                return MISS, None, None
            self._data.move_to_end(key)
            return (FRESH if age < self.ttl else STALE), value, stored_at

    def put(self, key, value) -> float:
        """Store a SUCCESSFUL result; returns its stored_at."""
        now = self._clock()
        with self._lock:
            self._data[key] = (value, now)
            self._data.move_to_end(key)
            self._failed_at.pop(key, None)
            while len(self._data) > self.max_entries:
                self._data.popitem(last=False)
        return now

    def claim_refresh(self, key) -> bool:
        """True for exactly one caller until release_refresh(key); also false for a short back-off
        after a failed refresh, so a broken report is not hammered on every stale hit."""
        with self._lock:
            if key in self._refreshing:
                return False
            failed = self._failed_at.get(key)
            if failed is not None and self._clock() - failed < self.refresh_backoff:
                return False
            self._refreshing.add(key)
            return True

    def release_refresh(self, key, failed: bool = False) -> None:
        with self._lock:
            self._refreshing.discard(key)
            if failed:
                self._failed_at[key] = self._clock()

    def __len__(self) -> int:
        with self._lock:
            return len(self._data)

    def clear(self) -> None:
        with self._lock:
            self._data.clear()
            self._refreshing.clear()
            self._failed_at.clear()
