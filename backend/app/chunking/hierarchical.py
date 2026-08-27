from __future__ import annotations

from typing import Any


class HierarchicalChunker:
    def __init__(self, parent_chunk_size: int = 1024, child_chunk_size: int = 256, overlap: int = 32):
        self.parent_size = parent_chunk_size
        self.child_size = child_chunk_size
        self.overlap = overlap

    def chunk_document(self, text: str, metadata: dict[str, Any]) -> list[dict[str, Any]]:
        words = text.split()
        chunks: list[dict[str, Any]] = []
        parent_index = 0

        step_parent = max(1, self.parent_size - self.overlap)
        step_child = max(1, self.child_size - self.overlap)

        for i in range(0, len(words), step_parent):
            parent_text = ' '.join(words[i:i + self.parent_size])
            parent_id = f'parent_{parent_index}'

            child_words = parent_text.split()
            for j in range(0, len(child_words), step_child):
                child_slice = child_words[j:j + self.child_size]
                child_text = ' '.join(child_slice)
                chunks.append({
                    'content': child_text,
                    'parent_content': parent_text,
                    'parent_chunk_id': parent_id,
                    'token_count': len(child_slice),
                    'chunk_index': len(chunks),
                    **metadata,
                })
            parent_index += 1

        return chunks
