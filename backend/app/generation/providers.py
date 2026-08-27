from collections.abc import Iterable
from typing import Protocol


class LLMProvider(Protocol):
    def generate(self, prompt: str) -> str: ...
    def stream(self, prompt: str) -> Iterable[str]: ...
