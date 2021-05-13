from typing import Iterable, List

from coriander.core import BaseToken, BaseTokenFinder, BaseTokenizer
from coriander.tokens import AnyTokenFinder, CharTokenFinder


class Tokenizer(BaseTokenizer):
    def __init__(self, token_finders: Iterable[BaseTokenFinder]) -> None:
        self.token_finders = token_finders

    def tokenize(self, raw_template: str) -> List[BaseToken]:
        tokens = []

        while raw_template:
            for token_finder in self.token_finders:
                token_find_result = token_finder.find(
                    raw_template=raw_template,
                    tokenizer=self,
                )
                if token_find_result:
                    tokens.append(token_find_result.token)
                    end = token_find_result.end
                    raw_template = raw_template[end:]

        return tokens


class DefaultTokenizer(Tokenizer):
    def __init__(self) -> None:
        token_finders = [
            AnyTokenFinder(),
            CharTokenFinder(),
        ]

        super().__init__(token_finders=token_finders)
