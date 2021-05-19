import random
import string
from typing import Any, List, Optional

from coriander.core import (
    BaseTemplateTokenizer,
    BaseToken,
    BaseTokenInTemplateFinder,
    FindTokenInTemplateResult,
)


class AnyToken(BaseToken):
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__)

    def match_with_message(
        self,
        message: str,
    ) -> List[int]:
        """
        >>> AnyToken().match_with_message("hello")
        [1, 2, 3, 4, 5]
        """
        return list(range(1, len(message) + 1))

    def generate_message(
        self,
    ) -> str:
        n = random.randint(1, 10)
        alphabet = string.ascii_uppercase + string.digits
        return "".join(random.choice(alphabet) for _ in range(n))


class AnyTokenInTemplateFinder(BaseTokenInTemplateFinder):
    def find_token_in_template(
        self,
        template: str,
        template_tokenizer: BaseTemplateTokenizer,
    ) -> Optional[FindTokenInTemplateResult]:
        if template[0] == "*":
            token = AnyToken()
            return FindTokenInTemplateResult(token=token, end=1)
        return None


class CharToken(BaseToken):
    def __init__(self, char: str) -> None:
        self.char = char

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and other.char == self.char

    def match_with_message(
        self,
        message: str,
    ) -> List[int]:
        """
        >>> CharToken(value="h").match_with_message("hello")
        [1]
        >>> CharToken(value="e").match_with_message("hello")
        []
        """
        if message[0] == self.char:
            return [1]
        return []

    def generate_message(
        self,
    ) -> str:
        return self.char


class CharTokenInTemplateFinder(BaseTokenInTemplateFinder):
    def find_token_in_template(
        self,
        template: str,
        template_tokenizer: BaseTemplateTokenizer,
    ) -> Optional[FindTokenInTemplateResult]:
        token = CharToken(char=template[0])
        return FindTokenInTemplateResult(token=token, end=1)
