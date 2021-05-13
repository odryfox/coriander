from typing import Any, Optional

from coriander.core import BaseToken, BaseTokenFinder, BaseTokenizer, TokenFindResult


class AnyToken(BaseToken):
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__)


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


class CharTokenFinder(BaseTokenFinder):
    def find(
        self,
        raw_template: str,
        tokenizer: BaseTokenizer,
    ) -> Optional[TokenFindResult]:
        token = CharToken(char=raw_template[0])
        return TokenFindResult(token=token, end=1)
