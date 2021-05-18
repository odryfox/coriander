from typing import List

from coriander.core import BaseMatcher, BaseToken


class Matcher(BaseMatcher):
    def match(
        self,
        message: str,
        tokens: List[BaseToken],
    ) -> bool:
        if not tokens:
            return not message

        if not message:
            return not tokens

        token = tokens[0]

        token_ending_variants = token.match(message)
        if not token_ending_variants:
            return False

        for token_ending_variant in token_ending_variants:
            result = self.match(
                message=message[token_ending_variant:],
                tokens=tokens[1:],
            )
            if result:
                return True

        return False
