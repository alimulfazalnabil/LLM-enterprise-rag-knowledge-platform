from app.chunking.hierarchical import HierarchicalChunker


def test_hierarchical_chunker_produces_chunks_with_parent_id() -> None:
    chunker = HierarchicalChunker(parent_chunk_size=8, child_chunk_size=4, overlap=1)
    chunks = chunker.chunk_document('one two three four five six seven eight nine ten', {'tenant_id': 'tenant_a'})

    assert chunks
    assert all('parent_chunk_id' in c for c in chunks)
    assert all(c['tenant_id'] == 'tenant_a' for c in chunks)
