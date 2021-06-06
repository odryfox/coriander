from typing import List

from coriander.core import BaseMatcher, BaseToken, BaseTokenizer
from coriander.tokenizers import DefaultTokenizer


class Matcher(BaseMatcher):
    def __init__(
        self,
        tokenizer: BaseTokenizer,
    ) -> None:
        self.tokenizer = tokenizer

    def match(
        self,
        message: str,
        template: str,
    ) -> bool:
        tokens = self.tokenizer.tokenize(template=template)
        tokens_ending_variants = self.match_with_tokens(
            message=message,
            tokens=tokens,
        )

        try:
            tokens_ending_variants.index(len(message))
            return True
        except ValueError:
            return False

    def match_with_tokens(
        self,
        message: str,
        tokens: List[BaseToken],
    ) -> List[int]:
        if not tokens:
            return [0]

        if not message:
            return []

        current_token_ending_variants = tokens[0].match_with_message(
            message=message,
            matcher=self,
        )

        token_ending_variants_set = set()

        for current_token_ending_variant in current_token_ending_variants:
            other_tokens_ending_variants = self.match_with_tokens(
                message=message[current_token_ending_variant:],
                tokens=tokens[1:],
            )
            for other_tokens_ending_variant in other_tokens_ending_variants:
                token_ending_variants_set.add(
                    other_tokens_ending_variant + current_token_ending_variant
                )

        return list(sorted(token_ending_variants_set))


class DefaultMatcher(Matcher):
    def __init__(self) -> None:
        tokenizer = DefaultTokenizer()
        super(DefaultMatcher, self).__init__(
            tokenizer=tokenizer,
        )
