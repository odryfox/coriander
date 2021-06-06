from typing import Iterable, List

from coriander.core import BaseToken, BaseTokenFinder, BaseTokenizer
from coriander.tokens import (
    AnyTokenFinder,
    CharTokenFinder,
    ChoiceTokenFinder,
    OptionalTokenFinder,
)


class Tokenizer(BaseTokenizer):
    def __init__(
        self,
        token_finders: Iterable[BaseTokenFinder],
    ) -> None:
        self.token_finders = token_finders

    def tokenize(self, template: str) -> List[BaseToken]:
        tokens = []

        while template:
            for token_finder in self.token_finders:
                find_result = token_finder.find_in_template(
                    template=template,
                    tokenizer=self,
                )
                if find_result:
                    tokens.append(find_result.token)
                    end = find_result.end
                    template = template[end:]
                    break

        return tokens


class DefaultTokenizer(Tokenizer):
    def __init__(self) -> None:
        token_finders = [
            AnyTokenFinder(),
            OptionalTokenFinder(),
            ChoiceTokenFinder(),
            CharTokenFinder(),
        ]

        super().__init__(token_finders=token_finders)
