"""Benchmark entry point. Results are only reported after actual execution."""
import statistics


def percentiles(values: list[float]) -> dict[str, float]:
    if not values:
        return {"p50": 0.0, "p95": 0.0, "p99": 0.0}
    ordered = sorted(values)
    return {name: ordered[min(len(ordered) - 1, int(len(ordered) * fraction))] for name, fraction in (("p50", .50), ("p95", .95), ("p99", .99))}

if __name__ == '__main__':
    print('Benchmark harness ready. Run against configured services; no fabricated results are emitted.')
