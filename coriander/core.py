from abc import ABC, abstractmethod
from typing import List, Optional


class FindTokenInTemplateResult:
    def __init__(self, token: "BaseToken", end: int) -> None:
        self.token = token
        self.end = end


class BaseTokenFinder(ABC):
    @abstractmethod
    def find_in_template(
        self,
        template: str,
        tokenizer: "BaseTokenizer",
    ) -> Optional[FindTokenInTemplateResult]:
        """Find token in start of template."""


class BaseToken(ABC):
    @abstractmethod
    def match_with_message(
        self,
        message: str,
        matcher: "BaseMatcher",
    ) -> List[int]:
        """Match token with start of message. Return variants ending of token."""

    @abstractmethod
    def generate_message(
        self,
        generator: "BaseGenerator",
    ) -> str:
        """Generate message."""


class BaseTokenizer(ABC):
    @abstractmethod
    def tokenize(self, template: str) -> List[BaseToken]:
        """Convert template to list of tokens."""


class BaseMatcher(ABC):
    @abstractmethod
    def match(
        self,
        message: str,
        template: str,
    ) -> bool:
        """Match message and template."""

    @abstractmethod
    def match_with_tokens(
        self,
        message: str,
        tokens: List["BaseToken"],
    ) -> List[int]:
        """Match tokens with start of message. Return variants ending of tokens."""


class BaseGenerator(ABC):
    @abstractmethod
    def generate(
        self,
        template: str,
    ) -> str:
        """Generate message from template."""

    @abstractmethod
    def generate_from_tokens(
        self,
        tokens: List["BaseToken"],
    ) -> str:
        """Generate message from tokens."""
