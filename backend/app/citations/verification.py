from dataclasses import dataclass

@dataclass(frozen=True)
class Citation:
    tenant_id: str
    document_id: str
    version_id: str
    chunk_id: str


def verify_citations(citations: list[Citation], tenant_id: str, existing_chunk_ids: set[str]) -> dict[str, int]:
    valid = 0
    invalid = 0
    unauthorized = 0
    for c in citations:
        if c.tenant_id != tenant_id:
            unauthorized += 1
            continue
        if c.chunk_id in existing_chunk_ids:
            valid += 1
        else:
            invalid += 1
    return {'valid': valid, 'invalid': invalid, 'unauthorized': unauthorized}
