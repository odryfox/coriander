import random
import string
from typing import Any, List, Optional

from coriander.core import (
    BaseGenerator,
    BaseMatcher,
    BaseToken,
    BaseTokenFinder,
    BaseTokenizer,
    FindTokenInTemplateResult,
    MatchTokenWithMessageResult,
)


class AnyToken(BaseToken):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__)

    def match_with_message(
        self,
        message: str,
        matcher: BaseMatcher,
    ) -> List[MatchTokenWithMessageResult]:
        result = []
        for end in range(1, len(message) + 1):
            result.append(
                MatchTokenWithMessageResult(
                    value=message[:end],
                    end=end,
                    context={},
                )
            )
        return result

    def generate_message(
        self,
        generator: BaseGenerator,
        value: Any,
        context: dict,
    ) -> str:
        if value:
            return value

        n = random.randint(1, 10)
        alphabet = string.ascii_uppercase + string.digits
        return "".join(random.choice(alphabet) for _ in range(n))


class AnyTokenFinder(BaseTokenFinder):
    @classmethod
    def find_in_template(
        cls,
        template: str,
        tokenizer: BaseTokenizer,
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
        matcher: BaseMatcher,
    ) -> List[MatchTokenWithMessageResult]:
        if message[0] == self.char:
            return [MatchTokenWithMessageResult(value=message[0], end=1)]
        return []

    def generate_message(
        self,
        generator: BaseGenerator,
        value: Any,
        context: dict,
    ) -> str:
        return self.char


class CharTokenFinder(BaseTokenFinder):
    @classmethod
    def find_in_template(
        cls,
        template: str,
        tokenizer: BaseTokenizer,
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
        matcher: BaseMatcher,
    ) -> List[MatchTokenWithMessageResult]:
        match_tokens_with_message_results = matcher.match_with_tokens(
            message=message,
            tokens=self.tokens,
        )
        return [MatchTokenWithMessageResult(end=0)] + [
            MatchTokenWithMessageResult(
                end=r.end,
                context=r.context,
            )
            for r in match_tokens_with_message_results
        ]

    def generate_message(
        self,
        generator: BaseGenerator,
        value: Any,
        context: dict,
    ) -> str:
        message = ""

        if value is not None:
            if value:
                message = generator.generate_from_tokens(
                    tokens=self.tokens,
                    context=context,
                )
        else:
            if random.choice([True, False]):
                message = generator.generate_from_tokens(
                    tokens=self.tokens,
                    context=context,
                )

        return message


class OptionalTokenFinder(BaseTokenFinder):
    CHAR_START = "("
    CHAR_FINISH = ")"

    @classmethod
    def find_in_template(
        cls,
        template: str,
        tokenizer: BaseTokenizer,
    ) -> Optional[FindTokenInTemplateResult]:

        if template[0] != cls.CHAR_START:
            return None

        depth = 1

        for char_idx, char in enumerate(template[1:], start=1):
            if char == cls.CHAR_FINISH:
                depth -= 1
                if depth == 0:
                    template_part = template[1:char_idx]
                    tokens = tokenizer.tokenize(template_part)
                    return FindTokenInTemplateResult(
                        token=OptionalToken(tokens=tokens),
                        end=char_idx + 1,
                    )
            if char == cls.CHAR_START:
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
        matcher: BaseMatcher,
    ) -> List[MatchTokenWithMessageResult]:

        variants = {}

        for index, choice in enumerate(self.choices):
            match_tokens_with_message_results = matcher.match_with_tokens(
                message=message,
                tokens=choice,
            )
            variants[index] = match_tokens_with_message_results

        return [
            MatchTokenWithMessageResult(
                end=match_tokens_with_message_result.end,
                value=message[: match_tokens_with_message_result.end],
                context=match_tokens_with_message_result.context,
            )
            for key, match_tokens_with_message_results in variants.items()
            for match_tokens_with_message_result in match_tokens_with_message_results
        ]

    def generate_message(
        self,
        generator: BaseGenerator,
        value: Any,
        context: dict,
    ) -> str:
        if value:
            return value

        if not self.choices:
            return ""

        choice = random.choice(self.choices)
        message = generator.generate_from_tokens(tokens=choice, context=context)
        return message


class ChoiceTokenFinder(BaseTokenFinder):
    CHAR_START = "["
    CHAR_FINISH = "]"
    CHAR_SEPARATOR = "|"

    @classmethod
    def find_in_template(
        cls,
        template: str,
        tokenizer: BaseTokenizer,
    ) -> Optional[FindTokenInTemplateResult]:

        if template[0] != cls.CHAR_START:
            return None

        depth = 1
        last_pos = 1
        template_parts = []

        for char_idx, char in enumerate(template[1:], start=1):
            if char == cls.CHAR_SEPARATOR:
                if depth == 1:
                    template_parts.append(template[last_pos:char_idx])
                    last_pos = char_idx + 1

            if char == cls.CHAR_FINISH:
                depth -= 1
                if depth == 0:
                    template_parts.append(template[last_pos:char_idx])
                    choices = [
                        tokenizer.tokenize(template_part)
                        for template_part in template_parts
                    ]
                    return FindTokenInTemplateResult(
                        token=ChoiceToken(choices=choices),
                        end=char_idx + 1,
                    )
            if char == cls.CHAR_START:
                depth += 1

        return None


class IntToken(BaseToken):
    ALPHABET = set(map(str, range(10)))

    def __repr__(self) -> str:
        return "IntToken()"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__)

    def match_with_message(
        self,
        message: str,
        matcher: "BaseMatcher",
    ) -> List[MatchTokenWithMessageResult]:
        number_chars = []
        for c in message:
            if c in self.ALPHABET:
                number_chars.append(c)
            else:
                break

        if not number_chars:
            return []

        number = "".join(number_chars)
        return [
            MatchTokenWithMessageResult(
                end=len(number),
                value=int(number),
                context={},
            ),
        ]

    def generate_message(
        self,
        generator: "BaseGenerator",
        value: Any,
        context: dict,
    ) -> str:
        if value is not None:
            return str(value)
        return str(random.randint(0, 100))


class IntTokenFinder(BaseTokenFinder):
    def find_in_template(
        self, template: str, tokenizer: "BaseTokenizer"
    ) -> Optional[FindTokenInTemplateResult]:
        if template.startswith("INT"):
            return FindTokenInTemplateResult(
                token=IntToken(),
                end=3,
            )
        return None
