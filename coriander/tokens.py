from typing import Any, List, Optional

from coriander.core import BaseToken, BaseTokenFinder, BaseTokenizer, TokenFindResult


class AnyToken(BaseToken):
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__)

    def match(
        self,
        message: str,
    ) -> List[int]:
        """
        >>> AnyToken().match("hello")
        [1, 2, 3, 4, 5]
        """
        return list(range(1, len(message) + 1))


class AnyTokenFinder(BaseTokenFinder):
    def find(
        self,
        raw_template: str,
        tokenizer: BaseTokenizer,
    ) -> Optional[TokenFindResult]:
        if raw_template[0] == "*":
            token = AnyToken()
            return TokenFindResult(token=token, end=1)
        return None


class CharToken(BaseToken):
    def __init__(self, char: str) -> None:
        self.char = char

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and other.char == self.char

    def match(
        self,
        message: str,
    ) -> List[int]:
        """
        >>> CharToken(value="h").match("hello")
        [1]
        >>> CharToken(value="e").match("hello")
        []
        """
        if message[0] == self.char:
            return [1]
        return []


class CharTokenFinder(BaseTokenFinder):
    def find(
        self,
        raw_template: str,
        tokenizer: BaseTokenizer,
    ) -> Optional[TokenFindResult]:
        token = CharToken(char=raw_template[0])
        return TokenFindResult(token=token, end=1)
