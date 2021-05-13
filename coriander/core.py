from abc import ABC, abstractmethod
from typing import List, Optional


class BaseToken(ABC):
    pass


class BaseTokenizer(ABC):
    @abstractmethod
    def tokenize(self, raw_template: str) -> List[BaseToken]:
        """Convert raw_template to list of tokens."""


class TokenFindResult:
    def __init__(self, token: BaseToken, end: int) -> None:
        self.token = token
        self.end = end


class BaseTokenFinder(ABC):
    @abstractmethod
    def find(
        self,
        raw_template: str,
        tokenizer: BaseTokenizer,
    ) -> Optional[TokenFindResult]:
        """Find token in start of raw_template."""
