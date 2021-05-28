from typing import List

from coriander.core import (
    BaseMessageWithTemplateMatcher,
    BaseTemplateTokenizer,
    BaseToken,
    BaseTokensWithMessageMatcher,
)
from coriander.tokenizers import DefaultTokenizer


class TokensWithMessageMatcher(BaseTokensWithMessageMatcher):
    def match_tokens_with_message(
        self,
        tokens: List[BaseToken],
        message: str,
    ) -> List[int]:
        if not tokens:
            return [0]

        if not message:
            return []

        current_token_ending_variants = tokens[0].match_with_message(
            message=message,
            tokens_with_message_matcher=self,
        )

        token_ending_variants_set = set()

        for current_token_ending_variant in current_token_ending_variants:
            other_tokens_ending_variants = self.match_tokens_with_message(
                tokens=tokens[1:],
                message=message[current_token_ending_variant:],
            )
            for other_tokens_ending_variant in other_tokens_ending_variants:
                token_ending_variants_set.add(
                    other_tokens_ending_variant + current_token_ending_variant
                )

        return list(sorted(token_ending_variants_set))


class MessageWithTemplateMatcher(BaseMessageWithTemplateMatcher):
    def __init__(
        self,
        template_tokenizer: BaseTemplateTokenizer,
    ) -> None:
        self.template_tokenizer = template_tokenizer

    def match_message_with_template(
        self,
        message: str,
        template: str,
    ) -> bool:
        tokens_with_message_matcher = TokensWithMessageMatcher()

        tokens = self.template_tokenizer.template_tokenize(template=template)
        tokens_ending_variants = tokens_with_message_matcher.match_tokens_with_message(
            tokens=tokens,
            message=message,
        )

        try:
            tokens_ending_variants.index(len(message))
            return True
        except ValueError:
            return False


class DefaultMessageWithTemplateMatcher(MessageWithTemplateMatcher):
    def __init__(self) -> None:
        template_tokenizer = DefaultTokenizer()
        super(DefaultMessageWithTemplateMatcher, self).__init__(
            template_tokenizer=template_tokenizer,
        )
