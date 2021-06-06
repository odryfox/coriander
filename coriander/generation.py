from typing import List

from coriander.core import BaseGenerator, BaseToken, BaseTokenizer
from coriander.tokenizers import DefaultTokenizer


class Generator(BaseGenerator):
    def __init__(self, tokenizer: BaseTokenizer) -> None:
        self.tokenizer = tokenizer

    def generate(
        self,
        template: str,
    ) -> str:
        tokens = self.tokenizer.tokenize(template=template)
        return self.generate_from_tokens(tokens=tokens)

    def generate_from_tokens(
        self,
        tokens: List["BaseToken"],
    ) -> str:
        message_parts = []

        for token in tokens:
            message_part = token.generate_message(generator=self)
            message_parts.append(message_part)

        return "".join(message_parts)


class DefaultGenerator(Generator):
    def __init__(self):
        tokenizer = DefaultTokenizer()
        super().__init__(tokenizer=tokenizer)
