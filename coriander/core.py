from abc import ABC, abstractmethod
from typing import List, Optional


class BaseMessageWithTemplateMatcher(ABC):
    @abstractmethod
    def match_message_with_template(
        self,
        message: str,
        template: str,
    ) -> bool:
        """Match message and template."""


class BaseToken(ABC):
    @abstractmethod
    def match_with_message(
        self,
        message: str,
    ) -> List[int]:
        """Match token with start of message. Return variants ending of token."""

    @abstractmethod
    def generate_message(self) -> str:
        """Generate message."""


class BaseMessageWithTokensMatcher(ABC):
    @abstractmethod
    def match_message_with_tokens(
        self,
        message: str,
        tokens: List[BaseToken],
    ) -> bool:
        """Match message and tokens."""


class BaseTemplateTokenizer(ABC):
    @abstractmethod
    def template_tokenize(self, template: str) -> List[BaseToken]:
        """Convert template to list of tokens."""


class FindTokenInTemplateResult:
    def __init__(self, token: BaseToken, end: int) -> None:
        self.token = token
        self.end = end


class BaseTokenInTemplateFinder(ABC):
    @abstractmethod
    def find_token_in_template(
        self,
        template: str,
        template_tokenizer: BaseTemplateTokenizer,
    ) -> Optional[FindTokenInTemplateResult]:
        """Find token in start of template."""


class BaseMessageFromTemplateGenerator(ABC):
    @abstractmethod
    def generate_message_from_template(
        self,
        template: str,
    ) -> str:
        """Generate message from template."""
