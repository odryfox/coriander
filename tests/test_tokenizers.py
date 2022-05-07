from typing import Optional

from coriander.core import BaseTokenFinder, BaseTokenizer, FindTokenInTemplateResult
from coriander.tokenizers import DefaultTokenizer, Tokenizer
from coriander.tokens import (
    AnyToken,
    AnyTokenFinder,
    CharToken,
    CharTokenFinder,
    ChoiceTokenFinder,
)


class TestTokenizer:
    def test_tokenize(self):
        token_finders = [
            AnyTokenFinder(),
            CharTokenFinder(),
        ]
        tokenizer = Tokenizer(
            token_finders=token_finders,
        )

        actual_tokens = tokenizer.tokenize(template='* hello')

        expected_tokens = [
            AnyToken(),
            CharToken(char=' '),
            CharToken(char='h'),
            CharToken(char='e'),
            CharToken(char='l'),
            CharToken(char='l'),
            CharToken(char='o'),
        ]
        assert actual_tokens == expected_tokens

    def test_tokenize__associate_name(self):
        token_finders = [
            ChoiceTokenFinder(),
            CharTokenFinder(),
        ]
        tokenizer = Tokenizer(
            token_finders=token_finders,
        )

        tokens = tokenizer.tokenize(
            template='[Docker|Coriander]~name',
        )

        assert tokens
        assert tokens[0].associate_name == 'name'

    def test_tokenize__associate_name_with_underscore(self):
        token_finders = [
            ChoiceTokenFinder(),
            CharTokenFinder(),
        ]
        tokenizer = Tokenizer(
            token_finders=token_finders,
        )

        tokens = tokenizer.tokenize(
            template='[Docker|Coriander]~first_name',
        )

        assert tokens
        assert tokens[0].associate_name == 'first_name'

    def test_tokenize__associate_names(self):
        token_finders = [
            ChoiceTokenFinder(),
            CharTokenFinder(),
        ]
        tokenizer = Tokenizer(
            token_finders=token_finders,
        )

        tokens = tokenizer.tokenize(
            template='[Docker|Coriander]~name [12|21]~age',
        )

        assert tokens
        assert tokens[0].associate_name == 'name'
        assert tokens[1].associate_name is None  # space char
        assert tokens[2].associate_name == 'age'


class TestDefaultTokenizer:
    def test_tokenize(self):
        tokenizer = DefaultTokenizer()

        actual_tokens = tokenizer.tokenize(template='* hello')

        expected_tokens = [
            AnyToken(),
            CharToken(char=' '),
            CharToken(char='h'),
            CharToken(char='e'),
            CharToken(char='l'),
            CharToken(char='l'),
            CharToken(char='o'),
        ]
        assert actual_tokens == expected_tokens

    def test_tokenize__with_custom_token_finders(self):
        class AllTokenFinder(BaseTokenFinder):
            def find_in_template(
                self,
                template: str,
                tokenizer: 'BaseTokenizer',
            ) -> Optional[FindTokenInTemplateResult]:
                return FindTokenInTemplateResult(
                    end=len(template),
                    token=AnyToken(),
                )

        custom_token_finders = [AllTokenFinder()]
        tokenizer = DefaultTokenizer(custom_token_finders=custom_token_finders)

        actual_tokens = tokenizer.tokenize(template='hello')

        expected_tokens = [
            AnyToken(),
        ]
        assert actual_tokens == expected_tokens
