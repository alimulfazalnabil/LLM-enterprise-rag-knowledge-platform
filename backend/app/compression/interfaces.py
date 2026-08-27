from dataclasses import dataclass


@dataclass(frozen=True)
class CompressionStats:
    original_context_tokens: int
    compressed_context_tokens: int

    @property
    def compression_ratio(self) -> float:
        if self.original_context_tokens == 0:
            return 1.0
        return self.compressed_context_tokens / self.original_context_tokens
