from app.retrieval.schemas import RetrievalResult
from app.retrieval.tenant_filter import authorize_results
from app.citations.verification import Citation, verify_citations


def test_authorize_results_filters_cross_tenant_records() -> None:
    results = [
        RetrievalResult('tenant_a', 'doc_a', 'v1', 'c1', 0.8, {}),
        RetrievalResult('tenant_b', 'doc_b', 'v1', 'c2', 0.7, {}),
    ]
    filtered = authorize_results(results, tenant_id='tenant_a')
    assert [r.document_id for r in filtered] == ['doc_a']


def test_citation_verification_flags_unauthorized_and_invalid() -> None:
    citations = [
        Citation('tenant_a', 'doc_a', 'v1', 'c1'),
        Citation('tenant_b', 'doc_b', 'v1', 'c2'),
        Citation('tenant_a', 'doc_a', 'v1', 'missing'),
    ]
    out = verify_citations(citations, tenant_id='tenant_a', existing_chunk_ids={'c1'})
    assert out == {'valid': 1, 'invalid': 1, 'unauthorized': 1}
