from unittest import mock

from coriander.generation import DefaultGenerator
from coriander.matching import Matcher
from coriander.tokenizers import DefaultTokenizer
from coriander.tokens import (
    AnyToken,
    AnyTokenFinder,
    CharToken,
    CharTokenFinder,
    ChoiceToken,
    ChoiceTokenFinder,
    IntToken,
    IntTokenFinder,
    OptionalToken,
    OptionalTokenFinder,
)


class TestAnyToken:
    def test_repr(self):
        token = AnyToken()

        assert repr(token) == 'AnyToken()'

    def test_match_with_message(self):
        token = AnyToken()

        match_token_with_message_results = token.match_with_message(
            message='hello',
            matcher=Matcher(tokenizer=DefaultTokenizer()),
        )

        assert match_token_with_message_results[0].end == 1
        assert match_token_with_message_results[1].end == 2
        assert match_token_with_message_results[2].end == 3
        assert match_token_with_message_results[3].end == 4
        assert match_token_with_message_results[4].end == 5

    def test_generate_message(self):
        token = AnyToken()

        message = token.generate_message(
            generator=DefaultGenerator(),
            value=None,
            context={},
        )

        assert message


class TestAnyTokenFinder:
    def test_find_in_template(self):
        tokenizer = DefaultTokenizer()
        token_in_template_finder = AnyTokenFinder()

        find_token_in_template_result = token_in_template_finder.find_in_template(
            template='* hello',
            tokenizer=tokenizer,
        )

        assert find_token_in_template_result
        assert find_token_in_template_result.token == AnyToken()
        assert find_token_in_template_result.end == 1

    def test_find_in_template__without_token(self):
        tokenizer = DefaultTokenizer()
        token_in_template_finder = AnyTokenFinder()

        find_token_in_template_result = token_in_template_finder.find_in_template(
            template='hello',
            tokenizer=tokenizer,
        )

        assert find_token_in_template_result is None


class TestCharToken:
    def test_repr(self):
        token = CharToken(char='a')

        assert repr(token) == 'CharToken(char=\'a\')'

    def test_match_with_message(self):
        token = CharToken(char='h')

        match_token_with_message_results = token.match_with_message(
            message='hello',
            matcher=Matcher(tokenizer=DefaultTokenizer()),
        )

        assert match_token_with_message_results[0].end == 1

    def test_match_with_message__incorrect(self):
        token = CharToken(char='a')

        match_token_with_message_results = token.match_with_message(
            message='hello',
            matcher=Matcher(tokenizer=DefaultTokenizer()),
        )

        assert match_token_with_message_results == []

    def test_generate_message(self):
        token = CharToken(char='h')

        message = token.generate_message(
            generator=DefaultGenerator(),
            value=None,
            context={},
        )

        assert message == 'h'


class TestCharTokenFinder:
    def test_find_in_template(self):
        tokenizer = DefaultTokenizer()
        token_in_template_finder = CharTokenFinder()

        find_token_in_template_result = token_in_template_finder.find_in_template(
            template='hello',
            tokenizer=tokenizer,
        )

        assert find_token_in_template_result
        assert find_token_in_template_result.token == CharToken(char='h')
        assert find_token_in_template_result.end == 1


class TestOptionalToken:
    def test_repr(self):
        token = OptionalToken(tokens=[AnyToken(), CharToken(char='a')])

        assert repr(token) == 'OptionalToken(tokens=[AnyToken(), CharToken(char=\'a\')])'

    def test_match_with_message(self):
        token = OptionalToken(tokens=[CharToken(char='h')])

        match_token_with_message_results = token.match_with_message(
            message='hello',
            matcher=Matcher(tokenizer=DefaultTokenizer()),
        )

        assert match_token_with_message_results[0].end == 0
        assert match_token_with_message_results[1].end == 1

    @mock.patch('random.choice')
    def test_generate_message__random_true(self, choice_mock):
        choice_mock.return_value = True
        token = OptionalToken(tokens=[CharToken('h')])

        message = token.generate_message(
            generator=DefaultGenerator(),
            value=None,
            context={},
        )

        assert message == 'h'
        choice_mock.assert_called_once_with([True, False])

    @mock.patch('random.choice')
    def test_generate_message__random_false(self, choice_mock):
        choice_mock.return_value = False
        token = OptionalToken(tokens=[CharToken('h')])

        message = token.generate_message(
            generator=DefaultGenerator(),
            value=None,
            context={},
        )

        assert message == ''
        choice_mock.assert_called_once_with([True, False])

    @mock.patch('random.choice')
    def test_generate_message__value_true(self, choice_mock):
        token = OptionalToken(tokens=[CharToken('h')])

        message = token.generate_message(
            generator=DefaultGenerator(),
            value=True,
            context={},
        )

        assert message == 'h'
        choice_mock.assert_not_called()

    @mock.patch('random.choice')
    def test_generate_message__value_false(self, choice_mock):
        token = OptionalToken(tokens=[CharToken('h')])

        message = token.generate_message(
            generator=DefaultGenerator(),
            value=False,
            context={},
        )

        assert message == ''
        choice_mock.assert_not_called()


class TestOptionalTokenFinder:
    def test_find_in_template(self):
        tokenizer = DefaultTokenizer()
        token_in_template_finder = OptionalTokenFinder()

        find_token_in_template_result = token_in_template_finder.find_in_template(
            template='(hello)',
            tokenizer=tokenizer,
        )

        expected_token = OptionalToken(
            tokens=[
                CharToken(char='h'),
                CharToken(char='e'),
                CharToken(char='l'),
                CharToken(char='l'),
                CharToken(char='o'),
            ],
        )

        assert find_token_in_template_result
        assert find_token_in_template_result.token == expected_token
        assert find_token_in_template_result.end == 7

    def test_find_in_template__without_token(self):
        tokenizer = DefaultTokenizer()
        token_in_template_finder = OptionalTokenFinder()

        find_token_in_template_result = token_in_template_finder.find_in_template(
            template='hello',
            tokenizer=tokenizer,
        )

        assert not find_token_in_template_result

    def test_find_in_template__nested_tokens(self):
        tokenizer = DefaultTokenizer()
        token_in_template_finder = OptionalTokenFinder()

        find_token_in_template_result = token_in_template_finder.find_in_template(
            template='((h)ello)',
            tokenizer=tokenizer,
        )

        expected_token = OptionalToken(
            tokens=[
                OptionalToken(tokens=[CharToken(char='h')]),
                CharToken(char='e'),
                CharToken(char='l'),
                CharToken(char='l'),
                CharToken(char='o'),
            ],
        )

        assert find_token_in_template_result
        assert find_token_in_template_result.token == expected_token
        assert find_token_in_template_result.end == 9

    def test_find_in_template__without_finish_char(self):
        tokenizer = DefaultTokenizer()
        token_in_template_finder = OptionalTokenFinder()

        find_token_in_template_result = token_in_template_finder.find_in_template(
            template='((h)ello',
            tokenizer=tokenizer,
        )

        assert not find_token_in_template_result


class TestChoiceToken:
    def test_repr(self):
        token = ChoiceToken(
            choices=[
                [AnyToken(), CharToken(char='a')],
                [CharToken(char='b')],
            ]
        )

        assert (
            repr(token) == 'ChoiceToken(choices=[[AnyToken(), CharToken(char=\'a\')], '
            '[CharToken(char=\'b\')]])'
        )

    def test_match_with_message(self):
        token = ChoiceToken(
            choices=[
                [
                    CharToken(char='h'),
                    CharToken(char='e'),
                    CharToken(char='l'),
                    CharToken(char='l'),
                    CharToken(char='o'),
                ],
                [
                    CharToken(char='h'),
                    CharToken(char='i'),
                ],
            ]
        )

        match_token_with_message_results = token.match_with_message(
            message='hello',
            matcher=Matcher(tokenizer=DefaultTokenizer()),
        )

        assert match_token_with_message_results[0].end == 5

    def test_match_with_message__second_choice(self):
        token = ChoiceToken(
            choices=[
                [
                    CharToken(char='h'),
                    CharToken(char='e'),
                    CharToken(char='l'),
                    CharToken(char='l'),
                    CharToken(char='o'),
                ],
                [
                    CharToken(char='h'),
                    CharToken(char='i'),
                ],
            ]
        )

        match_token_with_message_results = token.match_with_message(
            message='hillo',
            matcher=Matcher(tokenizer=DefaultTokenizer()),
        )

        assert match_token_with_message_results[0].end == 2

    def test_match_with_message__incorrect(self):
        token = ChoiceToken(
            choices=[
                [
                    CharToken(char='h'),
                    CharToken(char='e'),
                    CharToken(char='l'),
                    CharToken(char='l'),
                    CharToken(char='o'),
                ],
                [
                    CharToken(char='h'),
                    CharToken(char='i'),
                ],
            ]
        )

        token_ending_variants = token.match_with_message(
            message='eee',
            matcher=Matcher(tokenizer=DefaultTokenizer()),
        )

        assert token_ending_variants == []

    @mock.patch('random.choice')
    def test_generate_message(self, choice_mock):
        choices = [
            [
                CharToken(char='h'),
                CharToken(char='e'),
                CharToken(char='l'),
                CharToken(char='l'),
                CharToken(char='o'),
            ],
            [
                CharToken(char='h'),
                CharToken(char='i'),
            ],
        ]
        choice_mock.return_value = choices[1]
        token = ChoiceToken(choices=choices)

        message = token.generate_message(
            generator=DefaultGenerator(),
            value=None,
            context={},
        )

        assert message == 'hi'
        choice_mock.assert_called_once_with(choices)

    def test_generate_message__empty_choices(self):
        choices = []
        token = ChoiceToken(choices=choices)

        message = token.generate_message(
            generator=DefaultGenerator(),
            value=None,
            context={},
        )

        assert message == ''


class TestChoiceTokenFinder:
    def test_find_in_template(self):
        tokenizer = DefaultTokenizer()
        token_in_template_finder = ChoiceTokenFinder()

        find_token_in_template_result = token_in_template_finder.find_in_template(
            template='[hello|hi]',
            tokenizer=tokenizer,
        )

        expected_token = ChoiceToken(
            choices=[
                [
                    CharToken(char='h'),
                    CharToken(char='e'),
                    CharToken(char='l'),
                    CharToken(char='l'),
                    CharToken(char='o'),
                ],
                [
                    CharToken(char='h'),
                    CharToken(char='i'),
                ],
            ]
        )

        assert find_token_in_template_result.token == expected_token
        assert find_token_in_template_result.end == 10

    def test_find_in_template__nested_tokens(self):
        tokenizer = DefaultTokenizer()
        token_in_template_finder = ChoiceTokenFinder()

        find_token_in_template_result = token_in_template_finder.find_in_template(
            template='[h[e|a]llo|hi]',
            tokenizer=tokenizer,
        )

        expected_token = ChoiceToken(
            choices=[
                [
                    CharToken(char='h'),
                    ChoiceToken(choices=[[CharToken(char='e')], [CharToken(char='a')]]),
                    CharToken(char='l'),
                    CharToken(char='l'),
                    CharToken(char='o'),
                ],
                [
                    CharToken(char='h'),
                    CharToken(char='i'),
                ],
            ]
        )

        assert find_token_in_template_result.token == expected_token
        assert find_token_in_template_result.end == 14

    def test_find_in_template__without_start_char(self):
        tokenizer = DefaultTokenizer()
        token_in_template_finder = ChoiceTokenFinder()

        find_token_in_template_result = token_in_template_finder.find_in_template(
            template='hello|hi]',
            tokenizer=tokenizer,
        )

        assert not find_token_in_template_result

    def test_find_in_template__without_finish_char(self):
        tokenizer = DefaultTokenizer()
        token_in_template_finder = ChoiceTokenFinder()

        find_token_in_template_result = token_in_template_finder.find_in_template(
            template='[hello|hi',
            tokenizer=tokenizer,
        )

        assert not find_token_in_template_result


class TestIntToken:
    def test_repr(self):
        token = IntToken()

        assert repr(token) == 'IntToken()'

    def test_match_with_message(self):
        token = IntToken()

        match_token_with_message_results = token.match_with_message(
            message='123ae',
            matcher=Matcher(tokenizer=DefaultTokenizer()),
        )

        assert match_token_with_message_results[0].end == 3
        assert match_token_with_message_results[0].value == 123
        assert match_token_with_message_results[0].context == {}

    def test_match_with_message__without_number(self):
        token = IntToken()

        match_token_with_message_results = token.match_with_message(
            message='ae',
            matcher=Matcher(tokenizer=DefaultTokenizer()),
        )

        assert not match_token_with_message_results

    def test_generate_message(self):
        token = IntToken()

        message = token.generate_message(
            generator=DefaultGenerator(),
            value=123,
            context={},
        )

        assert message == '123'

    @mock.patch('random.randint')
    def test_generate_message__without_value(self, randint_mock):
        randint_mock.return_value = 123
        token = IntToken()

        message = token.generate_message(
            generator=DefaultGenerator(),
            value=None,
            context={},
        )

        assert message == '123'
        randint_mock.assert_called_once_with(0, 100)


class TestIntTokenFinder:
    def test_find_in_template(self):
        tokenizer = DefaultTokenizer()
        token_in_template_finder = IntTokenFinder()

        find_token_in_template_result = token_in_template_finder.find_in_template(
            template='INT abc',
            tokenizer=tokenizer,
        )

        assert find_token_in_template_result
        assert find_token_in_template_result.token == IntToken()
        assert find_token_in_template_result.end == 3

    def test_find_in_template__without_token(self):
        tokenizer = DefaultTokenizer()
        token_in_template_finder = IntTokenFinder()

        find_token_in_template_result = token_in_template_finder.find_in_template(
            template='abc INT abc',
            tokenizer=tokenizer,
        )

        assert not find_token_in_template_result
