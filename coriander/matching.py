from typing import List, Optional

from coriander.core import (
    BaseMatcher,
    BaseToken,
    BaseTokenFinder,
    BaseTokenizer,
    MatchResult,
    MatchTokensWithMessageResult,
)
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
    ) -> MatchResult:
        tokens = self.tokenizer.tokenize(template=template)
        match_tokens_with_message_results = self.match_with_tokens(
            message=message,
            tokens=tokens,
        )

        for match_tokens_with_message_result in match_tokens_with_message_results:
            if match_tokens_with_message_result.end == len(message):
                return MatchResult(
                    success=True,
                    context=match_tokens_with_message_result.context,
                )

        return MatchResult(
            success=False,
            context={},
        )

    def match_with_tokens(
        self,
        message: str,
        tokens: List[BaseToken],
    ) -> List[MatchTokensWithMessageResult]:
        if not tokens:
            return [
                MatchTokensWithMessageResult(
                    end=0,
                    context={},
                )
            ]

        if not message:
            return []

        match_token_with_message_results = tokens[0].match_with_message(
            message=message,
            matcher=self,
        )

        result = set()

        for match_token_with_message_result in match_token_with_message_results:
            context = {}
            associate_name = tokens[0].associate_name
            if associate_name:
                context[associate_name] = match_token_with_message_result.value
                if match_token_with_message_result.context:
                    context = {**context, **match_token_with_message_result.context}

            other_match_tokens_with_message_results = self.match_with_tokens(
                message=message[match_token_with_message_result.end :],
                tokens=tokens[1:],
            )
            for other_result in other_match_tokens_with_message_results:
                context = {**context, **other_result.context}
                result.add(
                    MatchTokensWithMessageResult(
                        end=other_result.end + match_token_with_message_result.end,
                        context=context,
                    )
                )

        return list(sorted(result, key=lambda x: x.end))


class DefaultMatcher(Matcher):
    def __init__(
        self,
        custom_token_finders: Optional[List[BaseTokenFinder]] = None,
    ) -> None:
        tokenizer = DefaultTokenizer(custom_token_finders=custom_token_finders)
        super(DefaultMatcher, self).__init__(
            tokenizer=tokenizer,
        )
