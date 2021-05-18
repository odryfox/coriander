from abc import ABC, abstractmethod
from typing import List, Optional


class BaseToken(ABC):
    @abstractmethod
    def match(
        self,
        message: str,
    ) -> List[int]:
        """Match token with start of message. Return variants ending of token."""


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


class BaseMatcher(ABC):
    @abstractmethod
    def match(
        self,
        message: str,
        tokens: List[BaseToken],
    ) -> bool:
        """Match message and tokens."""
