from app.citations.verifier import CitationVerifier


def test_citation_verifier_returns_valid_citations_and_confidence() -> None:
    answer = 'See policy [1] and controls [3].'
    retrieved = [
        {'document_id': 'doc_1', 'chunk_id': 'c1', 'section_title': 'A', 'page_number': 1},
        {'document_id': 'doc_2', 'chunk_id': 'c2', 'section_title': 'B', 'page_number': 2},
    ]
    _, cites, confidence = CitationVerifier.verify_citations(answer, retrieved)

    assert len(cites) == 1
    assert cites[0]['citation_index'] == 1
    assert confidence < 1.0
