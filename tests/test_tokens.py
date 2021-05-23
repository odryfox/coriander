from unittest import mock

from coriander.matching import TokensWithMessageMatcher
from coriander.tokenizers import DefaultTokenizer, TemplateTokenizer
from coriander.tokens import (
    AnyToken,
    AnyTokenInTemplateFinder,
    CharToken,
    CharTokenInTemplateFinder,
    OptionalToken,
    OptionalTokenInTemplateFinder,
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


def test_char_token():
    template_tokenizer = DefaultTokenizer()
    token_in_template_finder = CharTokenInTemplateFinder()

    find_token_in_template_result = token_in_template_finder.find_token_in_template(
        template="hello",
        template_tokenizer=template_tokenizer,
    )

    assert find_token_in_template_result
    assert find_token_in_template_result.token == CharToken(char="h")
    assert find_token_in_template_result.end == 1


def test_any_token():
    template_tokenizer = DefaultTokenizer()
    token_in_template_finder = AnyTokenInTemplateFinder()

    find_token_in_template_result = token_in_template_finder.find_token_in_template(
        template="* hello",
        template_tokenizer=template_tokenizer,
    )

    assert find_token_in_template_result
    assert find_token_in_template_result.token == AnyToken()
    assert find_token_in_template_result.end == 1


def test_optional_token():
    template_tokenizer = DefaultTokenizer()
    token_in_template_finder = OptionalTokenInTemplateFinder()

    find_token_in_template_result = token_in_template_finder.find_token_in_template(
        template="(hello)",
        template_tokenizer=template_tokenizer,
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
    template_tokenizer = DefaultTokenizer()
    token_in_template_finder = OptionalTokenInTemplateFinder()

    find_token_in_template_result = token_in_template_finder.find_token_in_template(
        template="hello",
        template_tokenizer=template_tokenizer,
    )

    assert not find_token_in_template_result


def test_optional_token_nested():
    template_tokenizer = DefaultTokenizer()
    token_in_template_finder = OptionalTokenInTemplateFinder()

    find_token_in_template_result = token_in_template_finder.find_token_in_template(
        template="((h)ello)",
        template_tokenizer=template_tokenizer,
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
    template_tokenizer = DefaultTokenizer()
    token_in_template_finder = OptionalTokenInTemplateFinder()

    find_token_in_template_result = token_in_template_finder.find_token_in_template(
        template="((h)ello",
        template_tokenizer=template_tokenizer,
    )

    assert not find_token_in_template_result


def test_not_any_token():
    template_tokenizer = DefaultTokenizer()
    token_in_template_finder = AnyTokenInTemplateFinder()

    find_token_in_template_result = token_in_template_finder.find_token_in_template(
        template="hello",
        template_tokenizer=template_tokenizer,
    )

    assert find_token_in_template_result is None


def test_tokenizer():
    token_in_template_finders = [
        AnyTokenInTemplateFinder(),
        CharTokenInTemplateFinder(),
    ]
    template_tokenizer = TemplateTokenizer(
        token_in_template_finders=token_in_template_finders,
    )

    actual_tokens = template_tokenizer.template_tokenize(template="* hello")

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
    template_tokenizer = DefaultTokenizer()

    actual_tokens = template_tokenizer.template_tokenize(template="* hello")

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
    message = AnyToken().generate_message()
    assert message


def test_generate_char_token():
    message = CharToken(char="h").generate_message()
    assert message == "h"


@mock.patch("random.choice")
def test_generate_optional_token_true(choice_mock):
    choice_mock.return_value = True

    message = OptionalToken(tokens=[CharToken("h")]).generate_message()

    assert message == "h"
    choice_mock.assert_called_once_with([True, False])


@mock.patch("random.choice")
def test_generate_optional_token_false(choice_mock):
    choice_mock.return_value = False

    message = OptionalToken(tokens=[CharToken("h")]).generate_message()

    assert message == ""
    choice_mock.assert_called_once_with([True, False])


def test_any_token_match_with_message():
    token = AnyToken()

    token_ending_variants = token.match_with_message(
        message="hello",
        tokens_with_message_matcher=TokensWithMessageMatcher(),
    )

    assert token_ending_variants == [1, 2, 3, 4, 5]


def test_char_token_match_with_message():
    token = CharToken(char="h")

    token_ending_variants = token.match_with_message(
        message="hello",
        tokens_with_message_matcher=TokensWithMessageMatcher(),
    )

    assert token_ending_variants == [1]


def test_char_token_match_with_message_incorrect():
    token = CharToken(char="a")

    token_ending_variants = token.match_with_message(
        message="hello",
        tokens_with_message_matcher=TokensWithMessageMatcher(),
    )

    assert token_ending_variants == []


def test_optional_token_match_with_message():
    token = OptionalToken(tokens=[CharToken(char="h")])

    token_ending_variants = token.match_with_message(
        message="hello",
        tokens_with_message_matcher=TokensWithMessageMatcher(),
    )

    assert token_ending_variants == [0, 1]
