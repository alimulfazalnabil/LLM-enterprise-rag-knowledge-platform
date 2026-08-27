from __future__ import annotations

import re
from typing import Any


class CitationVerifier:
    @staticmethod
    def verify_citations(answer: str, retrieved_chunks: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]], float]:
        matches = re.findall(r'\[(\d+)\]', answer)
        ref_indices = {int(m) for m in matches}
        valid_citations: list[dict[str, Any]] = []
        unsupported = 0

        chunk_map = {i + 1: chunk for i, chunk in enumerate(retrieved_chunks)}

        for idx in ref_indices:
            if idx in chunk_map:
                chunk = chunk_map[idx]
                valid_citations.append(
                    {
                        'citation_index': idx,
                        'document_id': chunk.get('document_id'),
                        'chunk_id': chunk.get('chunk_id'),
                        'section': chunk.get('section_title'),
                        'page': chunk.get('page_number'),
                    }
                )
            else:
                unsupported += 1

        total = len(ref_indices) if ref_indices else 1
        confidence = max(0.0, 1.0 - (unsupported / total))
        return answer, valid_citations, round(confidence, 2)
