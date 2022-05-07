from abc import ABC, abstractmethod
from typing import Any, List, Optional


class FindTokenInTemplateResult:
    def __init__(self, token: 'BaseToken', end: int) -> None:
        self.token = token
        self.end = end


class BaseTokenFinder(ABC):
    @abstractmethod
    def find_in_template(
        self,
        template: str,
        tokenizer: 'BaseTokenizer',
    ) -> Optional[FindTokenInTemplateResult]:
        """Find token in start of template."""


class MatchTokenWithMessageResult:
    def __init__(
        self,
        end: int,
        value: Any = None,
        context: Optional[dict] = None,
    ) -> None:
        self.end = end
        self.value = value
        self.context = context


class BaseToken(ABC):
    associate_name: Optional[str] = None

    @abstractmethod
    def match_with_message(
        self,
        message: str,
        matcher: 'BaseMatcher',
    ) -> List[MatchTokenWithMessageResult]:
        """Match token with start of message. Return variants ending of token."""

    @abstractmethod
    def generate_message(
        self,
        generator: 'BaseGenerator',
        value: Any,
        context: dict,
    ) -> str:
        """Generate message."""


class BaseTokenizer(ABC):
    @abstractmethod
    def tokenize(self, template: str) -> List[BaseToken]:
        """Convert template to list of tokens."""


class MatchTokensWithMessageResult:
    def __init__(self, end: int, context: dict) -> None:
        self.end = end
        self.context = context


class MatchResult:
    def __init__(self, success: bool, context: dict) -> None:
        self.success = success
        self.context = context

    def __bool__(self) -> bool:
        return self.success


class BaseMatcher(ABC):
    @abstractmethod
    def match(
        self,
        message: str,
        template: str,
    ) -> MatchResult:
        """Match message and template."""

    @abstractmethod
    def match_with_tokens(
        self,
        message: str,
        tokens: List['BaseToken'],
    ) -> List[MatchTokensWithMessageResult]:
        """Match tokens with start of message. Return variants ending of tokens."""


class BaseGenerator(ABC):
    @abstractmethod
    def generate(
        self,
        template: str,
        context: Optional[dict] = None,
    ) -> str:
        """Generate message from template."""

    @abstractmethod
    def generate_from_tokens(
        self,
        tokens: List['BaseToken'],
        context: dict,
    ) -> str:
        """Generate message from tokens."""
