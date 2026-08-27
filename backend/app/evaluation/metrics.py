from __future__ import annotations


def precision_at_k(relevant_hits: int, k: int) -> float:
    if k <= 0:
        return 0.0
    return relevant_hits / k


def recall_at_k(relevant_hits: int, total_relevant: int) -> float:
    if total_relevant <= 0:
        return 0.0
    return relevant_hits / total_relevant


def mrr(first_relevant_rank: int | None) -> float:
    if not first_relevant_rank or first_relevant_rank <= 0:
        return 0.0
    return 1.0 / first_relevant_rank
