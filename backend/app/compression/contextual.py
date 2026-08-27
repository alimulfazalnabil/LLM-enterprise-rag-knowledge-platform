from __future__ import annotations

from typing import Any


def compress_context(chunks: list[dict[str, Any]], max_chars: int = 1500) -> tuple[list[dict[str, Any]], dict[str, float]]:
    compressed: list[dict[str, Any]] = []
    original_tokens = 0
    compressed_tokens = 0

    for chunk in chunks:
        content = str(chunk.get('content', ''))
        original_tokens += len(content.split())
        clipped = content[:max_chars]
        compressed_tokens += len(clipped.split())
        compressed.append({**chunk, 'content': clipped})

    ratio = (compressed_tokens / original_tokens) if original_tokens else 1.0
    return compressed, {
        'original_context_tokens': original_tokens,
        'compressed_context_tokens': compressed_tokens,
        'compression_ratio': round(ratio, 4),
    }
