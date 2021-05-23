from typing import List

from coriander.core import BaseToken, BaseTokensWithMessageMatcher


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
