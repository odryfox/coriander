import random
import string
from typing import Any, List, Optional

from coriander.core import (
    BaseTemplateTokenizer,
    BaseToken,
    BaseTokenInTemplateFinder,
    BaseTokensWithMessageMatcher,
    FindTokenInTemplateResult,
)


class AnyToken(BaseToken):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__)

    def match_with_message(
        self,
        message: str,
        tokens_with_message_matcher: BaseTokensWithMessageMatcher,
    ) -> List[int]:
        return list(range(1, len(message) + 1))

    def generate_message(
        self,
    ) -> str:
        n = random.randint(1, 10)
        alphabet = string.ascii_uppercase + string.digits
        return "".join(random.choice(alphabet) for _ in range(n))


class AnyTokenInTemplateFinder(BaseTokenInTemplateFinder):
    def find_token_in_template(
        self,
        template: str,
        template_tokenizer: BaseTemplateTokenizer,
    ) -> Optional[FindTokenInTemplateResult]:
        if template[0] == "*":
            token = AnyToken()
            return FindTokenInTemplateResult(token=token, end=1)
        return None


class CharToken(BaseToken):
    def __init__(self, char: str) -> None:
        self.char = char

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(char={repr(self.char)})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and other.char == self.char

    def match_with_message(
        self,
        message: str,
        tokens_with_message_matcher: BaseTokensWithMessageMatcher,
    ) -> List[int]:
        if message[0] == self.char:
            return [1]
        return []

    def generate_message(
        self,
    ) -> str:
        return self.char


class CharTokenInTemplateFinder(BaseTokenInTemplateFinder):
    def find_token_in_template(
        self,
        template: str,
        template_tokenizer: BaseTemplateTokenizer,
    ) -> Optional[FindTokenInTemplateResult]:
        token = CharToken(char=template[0])
        return FindTokenInTemplateResult(token=token, end=1)


class OptionalToken(BaseToken):
    def __init__(self, tokens: List[BaseToken]) -> None:
        self.tokens = tokens

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tokens={repr(self.tokens)})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and other.tokens == self.tokens

    def match_with_message(
        self,
        message: str,
        tokens_with_message_matcher: BaseTokensWithMessageMatcher,
    ) -> List[int]:
        tokens_ending_variants = tokens_with_message_matcher.match_tokens_with_message(
            message=message,
            tokens=self.tokens,
        )
        return [0] + tokens_ending_variants

    def generate_message(self) -> str:
        parts = []

        if random.choice([True, False]):
            parts = [token.generate_message() for token in self.tokens]

        return "".join(parts)


class OptionalTokenInTemplateFinder(BaseTokenInTemplateFinder):

    CHAR_START = "("
    CHAR_FINISH = ")"

    def find_token_in_template(
        self,
        template: str,
        template_tokenizer: BaseTemplateTokenizer,
    ) -> Optional[FindTokenInTemplateResult]:

        if template[0] != self.CHAR_START:
            return None

        depth = 1

        for char_idx, char in enumerate(template[1:], start=1):
            if char == self.CHAR_FINISH:
                depth -= 1
                if depth == 0:
                    template_part = template[1:char_idx]
                    tokens = template_tokenizer.template_tokenize(template_part)
                    return FindTokenInTemplateResult(
                        token=OptionalToken(tokens=tokens),
                        end=char_idx + 1,
                    )
            if char == self.CHAR_START:
                depth += 1

        return None


class ChoiceToken(BaseToken):
    def __init__(self, choices: List[List[BaseToken]]):
        self.choices = choices

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(choices={repr(self.choices)})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and other.choices == self.choices

    def match_with_message(
        self,
        message: str,
        tokens_with_message_matcher: BaseTokensWithMessageMatcher,
    ) -> List[int]:

        matcher = tokens_with_message_matcher
        variants = set()

        for choice in self.choices:
            tokens_ending_variants = matcher.match_tokens_with_message(
                message=message,
                tokens=choice,
            )
            variants.update(tokens_ending_variants)

        return sorted(list(variants))

    def generate_message(self) -> str:
        if not self.choices:
            return ""

        choice = random.choice(self.choices)
        parts = [token.generate_message() for token in choice]
        return "".join(parts)


class ChoiceTokenInTemplateFinder(BaseTokenInTemplateFinder):

    CHAR_START = "["
    CHAR_FINISH = "]"
    CHAR_SEPARATOR = "|"

    def find_token_in_template(
        self,
        template: str,
        template_tokenizer: BaseTemplateTokenizer,
    ) -> Optional[FindTokenInTemplateResult]:

        if template[0] != self.CHAR_START:
            return None

        depth = 1
        last_pos = 1
        template_parts = []

        for char_idx, char in enumerate(template[1:], start=1):
            if char == self.CHAR_SEPARATOR:
                if depth == 1:
                    template_parts.append(template[last_pos:char_idx])
                    last_pos = char_idx + 1

            if char == self.CHAR_FINISH:
                depth -= 1
                if depth == 0:
                    template_parts.append(template[last_pos:char_idx])
                    choices = [
                        template_tokenizer.template_tokenize(template_part)
                        for template_part in template_parts
                    ]
                    return FindTokenInTemplateResult(
                        token=ChoiceToken(choices=choices),
                        end=char_idx + 1,
                    )
            if char == self.CHAR_START:
                depth += 1

        return None
