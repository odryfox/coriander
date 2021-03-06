from unittest import mock

from coriander.generation import DefaultGenerator
from coriander.matching import Matcher
from coriander.tokenizers import DefaultTokenizer, Tokenizer
from coriander.tokens import (
    AnyToken,
    AnyTokenFinder,
    CharToken,
    CharTokenFinder,
    ChoiceToken,
    ChoiceTokenFinder,
    OptionalToken,
    OptionalTokenFinder,
)


def test_any_token_repr():
    token = AnyToken()

    assert repr(token) == "AnyToken()"


def test_char_token_repr():
    token = CharToken(char="a")

    assert repr(token) == "CharToken(char='a')"


def test_optional_token_repr():
    token = OptionalToken(tokens=[AnyToken(), CharToken(char="a")])

    assert repr(token) == "OptionalToken(tokens=[AnyToken(), CharToken(char='a')])"


def test_choice_token_repr():
    token = ChoiceToken(
        choices=[
            [AnyToken(), CharToken(char="a")],
            [CharToken(char="b")],
        ]
    )

    assert (
        repr(token) == "ChoiceToken(choices=[[AnyToken(), CharToken(char='a')], "
        "[CharToken(char='b')]])"
    )


def test_char_token():
    tokenizer = DefaultTokenizer()
    token_in_template_finder = CharTokenFinder()

    find_token_in_template_result = token_in_template_finder.find_in_template(
        template="hello",
        tokenizer=tokenizer,
    )

    assert find_token_in_template_result
    assert find_token_in_template_result.token == CharToken(char="h")
    assert find_token_in_template_result.end == 1


def test_any_token():
    tokenizer = DefaultTokenizer()
    token_in_template_finder = AnyTokenFinder()

    find_token_in_template_result = token_in_template_finder.find_in_template(
        template="* hello",
        tokenizer=tokenizer,
    )

    assert find_token_in_template_result
    assert find_token_in_template_result.token == AnyToken()
    assert find_token_in_template_result.end == 1


def test_optional_token():
    tokenizer = DefaultTokenizer()
    token_in_template_finder = OptionalTokenFinder()

    find_token_in_template_result = token_in_template_finder.find_in_template(
        template="(hello)",
        tokenizer=tokenizer,
    )

    expected_token = OptionalToken(
        tokens=[
            CharToken(char="h"),
            CharToken(char="e"),
            CharToken(char="l"),
            CharToken(char="l"),
            CharToken(char="o"),
        ],
    )

    assert find_token_in_template_result
    assert find_token_in_template_result.token == expected_token
    assert find_token_in_template_result.end == 7


def test_optional_token_none():
    tokenizer = DefaultTokenizer()
    token_in_template_finder = OptionalTokenFinder()

    find_token_in_template_result = token_in_template_finder.find_in_template(
        template="hello",
        tokenizer=tokenizer,
    )

    assert not find_token_in_template_result


def test_optional_token_nested():
    tokenizer = DefaultTokenizer()
    token_in_template_finder = OptionalTokenFinder()

    find_token_in_template_result = token_in_template_finder.find_in_template(
        template="((h)ello)",
        tokenizer=tokenizer,
    )

    expected_token = OptionalToken(
        tokens=[
            OptionalToken(tokens=[CharToken(char="h")]),
            CharToken(char="e"),
            CharToken(char="l"),
            CharToken(char="l"),
            CharToken(char="o"),
        ],
    )

    assert find_token_in_template_result
    assert find_token_in_template_result.token == expected_token
    assert find_token_in_template_result.end == 9


def test_optional_token_without_finish_char():
    tokenizer = DefaultTokenizer()
    token_in_template_finder = OptionalTokenFinder()

    find_token_in_template_result = token_in_template_finder.find_in_template(
        template="((h)ello",
        tokenizer=tokenizer,
    )

    assert not find_token_in_template_result


def test_not_any_token():
    tokenizer = DefaultTokenizer()
    token_in_template_finder = AnyTokenFinder()

    find_token_in_template_result = token_in_template_finder.find_in_template(
        template="hello",
        tokenizer=tokenizer,
    )

    assert find_token_in_template_result is None


def test_tokenizer():
    token_finders = [
        AnyTokenFinder(),
        CharTokenFinder(),
    ]
    tokenizer = Tokenizer(
        token_finders=token_finders,
    )

    actual_tokens = tokenizer.tokenize(template="* hello")

    expected_tokens = [
        AnyToken(),
        CharToken(char=" "),
        CharToken(char="h"),
        CharToken(char="e"),
        CharToken(char="l"),
        CharToken(char="l"),
        CharToken(char="o"),
    ]
    assert actual_tokens == expected_tokens


def test_default_tokenizer():
    tokenizer = DefaultTokenizer()

    actual_tokens = tokenizer.tokenize(template="* hello")

    expected_tokens = [
        AnyToken(),
        CharToken(char=" "),
        CharToken(char="h"),
        CharToken(char="e"),
        CharToken(char="l"),
        CharToken(char="l"),
        CharToken(char="o"),
    ]
    assert actual_tokens == expected_tokens


def test_generate_any_token():
    message = AnyToken().generate_message(
        generator=DefaultGenerator(),
        value=None,
        context={},
    )
    assert message


def test_generate_char_token():
    message = CharToken(char="h").generate_message(
        generator=DefaultGenerator(),
        value=None,
        context={},
    )
    assert message == "h"


@mock.patch("random.choice")
def test_generate_optional_token_true(choice_mock):
    choice_mock.return_value = True

    message = OptionalToken(tokens=[CharToken("h")]).generate_message(
        generator=DefaultGenerator(),
        value=None,
        context={},
    )

    assert message == "h"
    choice_mock.assert_called_once_with([True, False])


@mock.patch("random.choice")
def test_generate_optional_token_false(choice_mock):
    choice_mock.return_value = False

    message = OptionalToken(tokens=[CharToken("h")]).generate_message(
        generator=DefaultGenerator(),
        value=None,
        context={},
    )

    assert message == ""
    choice_mock.assert_called_once_with([True, False])


def test_any_token_match_with_message():
    token = AnyToken()

    match_token_with_message_results = token.match_with_message(
        message="hello",
        matcher=Matcher(tokenizer=DefaultTokenizer()),
    )

    assert match_token_with_message_results[0].end == 1
    assert match_token_with_message_results[1].end == 2
    assert match_token_with_message_results[2].end == 3
    assert match_token_with_message_results[3].end == 4
    assert match_token_with_message_results[4].end == 5


def test_char_token_match_with_message():
    token = CharToken(char="h")

    match_token_with_message_results = token.match_with_message(
        message="hello",
        matcher=Matcher(tokenizer=DefaultTokenizer()),
    )

    assert match_token_with_message_results[0].end == 1


def test_char_token_match_with_message_incorrect():
    token = CharToken(char="a")

    match_token_with_message_results = token.match_with_message(
        message="hello",
        matcher=Matcher(tokenizer=DefaultTokenizer()),
    )

    assert match_token_with_message_results == []


def test_optional_token_match_with_message():
    token = OptionalToken(tokens=[CharToken(char="h")])

    match_token_with_message_results = token.match_with_message(
        message="hello",
        matcher=Matcher(tokenizer=DefaultTokenizer()),
    )

    assert match_token_with_message_results[0].end == 0
    assert match_token_with_message_results[1].end == 1


def test_choice_token_find():
    tokenizer = DefaultTokenizer()
    token_in_template_finder = ChoiceTokenFinder()

    find_token_in_template_result = token_in_template_finder.find_in_template(
        template="[hello|hi]",
        tokenizer=tokenizer,
    )

    expected_token = ChoiceToken(
        choices=[
            [
                CharToken(char="h"),
                CharToken(char="e"),
                CharToken(char="l"),
                CharToken(char="l"),
                CharToken(char="o"),
            ],
            [
                CharToken(char="h"),
                CharToken(char="i"),
            ],
        ]
    )

    assert find_token_in_template_result.token == expected_token
    assert find_token_in_template_result.end == 10


def test_choice_token_match():
    token = ChoiceToken(
        choices=[
            [
                CharToken(char="h"),
                CharToken(char="e"),
                CharToken(char="l"),
                CharToken(char="l"),
                CharToken(char="o"),
            ],
            [
                CharToken(char="h"),
                CharToken(char="i"),
            ],
        ]
    )

    match_token_with_message_results = token.match_with_message(
        message="hello",
        matcher=Matcher(tokenizer=DefaultTokenizer()),
    )

    assert match_token_with_message_results[0].end == 5


def test_choice_token_match_short():
    token = ChoiceToken(
        choices=[
            [
                CharToken(char="h"),
                CharToken(char="e"),
                CharToken(char="l"),
                CharToken(char="l"),
                CharToken(char="o"),
            ],
            [
                CharToken(char="h"),
                CharToken(char="i"),
            ],
        ]
    )

    match_token_with_message_results = token.match_with_message(
        message="hillo",
        matcher=Matcher(tokenizer=DefaultTokenizer()),
    )

    assert match_token_with_message_results[0].end == 2


def test_choice_token_match_none():
    token = ChoiceToken(
        choices=[
            [
                CharToken(char="h"),
                CharToken(char="e"),
                CharToken(char="l"),
                CharToken(char="l"),
                CharToken(char="o"),
            ],
            [
                CharToken(char="h"),
                CharToken(char="i"),
            ],
        ]
    )

    token_ending_variants = token.match_with_message(
        message="eee",
        matcher=Matcher(tokenizer=DefaultTokenizer()),
    )

    assert token_ending_variants == []


@mock.patch("random.choice")
def test_choice_token_generation(choice_mock):
    choices = [
        [
            CharToken(char="h"),
            CharToken(char="e"),
            CharToken(char="l"),
            CharToken(char="l"),
            CharToken(char="o"),
        ],
        [
            CharToken(char="h"),
            CharToken(char="i"),
        ],
    ]
    choice_mock.return_value = choices[1]

    message = ChoiceToken(choices=choices).generate_message(
        generator=DefaultGenerator(),
        value=None,
        context={},
    )

    assert message == "hi"
    choice_mock.assert_called_once_with(choices)


def test_choice_token_generation_empty():
    choices = []

    message = ChoiceToken(choices=choices).generate_message(
        generator=DefaultGenerator(),
        value=None,
        context={},
    )

    assert message == ""


def test_choice_token_find_without_start_symbol():
    tokenizer = DefaultTokenizer()
    token_in_template_finder = ChoiceTokenFinder()

    find_token_in_template_result = token_in_template_finder.find_in_template(
        template="hello|hi]",
        tokenizer=tokenizer,
    )

    assert not find_token_in_template_result


def test_choice_token_find_nested():
    tokenizer = DefaultTokenizer()
    token_in_template_finder = ChoiceTokenFinder()

    find_token_in_template_result = token_in_template_finder.find_in_template(
        template="[h[e|a]llo|hi]",
        tokenizer=tokenizer,
    )

    expected_token = ChoiceToken(
        choices=[
            [
                CharToken(char="h"),
                ChoiceToken(choices=[[CharToken(char="e")], [CharToken(char="a")]]),
                CharToken(char="l"),
                CharToken(char="l"),
                CharToken(char="o"),
            ],
            [
                CharToken(char="h"),
                CharToken(char="i"),
            ],
        ]
    )

    assert find_token_in_template_result.token == expected_token
    assert find_token_in_template_result.end == 14


def test_choice_token_find_without_finish():
    tokenizer = DefaultTokenizer()
    token_in_template_finder = ChoiceTokenFinder()

    find_token_in_template_result = token_in_template_finder.find_in_template(
        template="[hello|hi",
        tokenizer=tokenizer,
    )

    assert not find_token_in_template_result


def test_tokenize_with_associate_name():
    tokenizer = DefaultTokenizer()

    tokens = tokenizer.tokenize(
        template="[Docker|Coriander]~name",
    )

    assert tokens
    assert tokens[0].associate_name == "name"


def test_tokenize_with_associate_name_with_underscore():
    tokenizer = DefaultTokenizer()

    tokens = tokenizer.tokenize(
        template="[Docker|Coriander]~first_name",
    )

    assert tokens
    assert tokens[0].associate_name == "first_name"


def test_tokenize_with_associate_names():
    tokenizer = DefaultTokenizer()

    tokens = tokenizer.tokenize(
        template="[Docker|Coriander]~name [12|21]~age",
    )

    assert tokens
    assert tokens[0].associate_name == "name"
    assert tokens[1].associate_name is None  # space char
    assert tokens[2].associate_name == "age"
