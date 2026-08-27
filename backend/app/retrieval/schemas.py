from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalResult:
    tenant_id: str
    document_id: str
    version_id: str
    chunk_id: str
    score: float
    metadata: dict
