from app.retrieval.schemas import RetrievalResult


def authorize_results(results: list[RetrievalResult], tenant_id: str) -> list[RetrievalResult]:
    return [r for r in results if r.tenant_id == tenant_id]
