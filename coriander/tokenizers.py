import string
from typing import Iterable, List

from coriander.core import BaseToken, BaseTokenFinder, BaseTokenizer
from coriander.tokens import (
    AnyTokenFinder,
    CharTokenFinder,
    ChoiceTokenFinder,
    IntTokenFinder,
    OptionalTokenFinder,
)


class Tokenizer(BaseTokenizer):
    ASSOCIATE_NAME_CHAR = "~"
    ASSOCIATE_NAME_ALPHABET = set(string.ascii_letters) | {"_"}

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
                    token = find_result.token
                    end = find_result.end
                    template = template[end:]

                    if (
                        len(template) > 1
                        and template[0] == self.ASSOCIATE_NAME_CHAR
                        and template[1] in self.ASSOCIATE_NAME_ALPHABET
                    ):
                        for i in range(1, len(template)):
                            if template[i] not in self.ASSOCIATE_NAME_ALPHABET:
                                associate_name = template[1:i]
                                token.associate_name = associate_name
                                template = template[i:]
                                break
                        else:
                            associate_name = template[1:]
                            token.associate_name = associate_name
                            template = ""

                    tokens.append(token)
                    break

        return tokens


class DefaultTokenizer(Tokenizer):
    def __init__(self) -> None:
        token_finders = [
            AnyTokenFinder(),
            OptionalTokenFinder(),
            ChoiceTokenFinder(),
            IntTokenFinder(),
            CharTokenFinder(),
        ]

        super().__init__(token_finders=token_finders)
