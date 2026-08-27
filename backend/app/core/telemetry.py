from __future__ import annotations

import time
from contextlib import contextmanager


@contextmanager
def span_timer(metrics: dict[str, float], key: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        metrics[key] = round((time.perf_counter() - start) * 1000, 3)
