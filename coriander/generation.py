from typing import List, Optional

from coriander.core import BaseGenerator, BaseToken, BaseTokenFinder, BaseTokenizer
from coriander.tokenizers import DefaultTokenizer


class Generator(BaseGenerator):
    def __init__(self, tokenizer: BaseTokenizer) -> None:
        self.tokenizer = tokenizer

    def generate(
        self,
        template: str,
        context: Optional[dict] = None,
    ) -> str:
        context = context or {}
        tokens = self.tokenizer.tokenize(template=template)
        return self.generate_from_tokens(tokens=tokens, context=context)

    def generate_from_tokens(
        self,
        tokens: List['BaseToken'],
        context: dict,
    ) -> str:
        message_parts = []

        for token in tokens:
            if token.associate_name in context:
                value = context[token.associate_name]
            else:
                value = None
            message_part = token.generate_message(
                generator=self,
                value=value,
                context=context,
            )
            message_parts.append(message_part)

        return ''.join(message_parts)


class DefaultGenerator(Generator):
    def __init__(
        self,
        custom_token_finders: Optional[List[BaseTokenFinder]] = None,
    ):
        tokenizer = DefaultTokenizer(custom_token_finders=custom_token_finders)
        super().__init__(tokenizer=tokenizer)
