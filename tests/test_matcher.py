from coriander.matching import (
    DefaultMessageWithTemplateMatcher,
    TokensWithMessageMatcher,
)
from coriander.tokens import AnyToken, CharToken


def test_correct_message():
    tokens = [
        CharToken(char="h"),
        CharToken(char="e"),
        AnyToken(),
        CharToken(char="o"),
    ]
    tokens_ending_variants = TokensWithMessageMatcher().match_tokens_with_message(
        tokens=tokens,
        message="hello",
    )
    assert tokens_ending_variants == [5]


def test_incorrect_message():
    tokens = [
        CharToken(char="h"),
        CharToken(char="e"),
        AnyToken(),
        CharToken(char="a"),
    ]
    tokens_ending_variants = TokensWithMessageMatcher().match_tokens_with_message(
        tokens=tokens,
        message="hello",
    )
    assert tokens_ending_variants == []


def test_tokens_and_empty_message():
    tokens = [
        CharToken(char="h"),
        CharToken(char="e"),
        AnyToken(),
        CharToken(char="o"),
    ]
    tokens_ending_variants = TokensWithMessageMatcher().match_tokens_with_message(
        tokens=tokens,
        message="",
    )
    assert tokens_ending_variants == []


def test_empty_tokens_and_empty_message():
    tokens = []
    tokens_ending_variants = TokensWithMessageMatcher().match_tokens_with_message(
        tokens=tokens,
        message="",
    )
    assert tokens_ending_variants == [0]


def test_empty_tokens_and_message():
    tokens = []
    tokens_ending_variants = TokensWithMessageMatcher().match_tokens_with_message(
        tokens=tokens,
        message="hello",
    )
    assert tokens_ending_variants == [0]


def test_any_variants():
    tokens = [
        AnyToken(),
        CharToken(char="e"),
    ]
    tokens_ending_variants = TokensWithMessageMatcher().match_tokens_with_message(
        tokens=tokens,
        message="hee",
    )
    assert tokens_ending_variants == [2, 3]


def test_any_token():
    tokens = [
        AnyToken(),
    ]
    tokens_ending_variants = TokensWithMessageMatcher().match_tokens_with_message(
        tokens=tokens,
        message="hee",
    )
    assert tokens_ending_variants == [1, 2, 3]


def test_default_matcher_success():
    message_with_template_matcher = DefaultMessageWithTemplateMatcher()

    result = message_with_template_matcher.match_message_with_template(
        message="hello my name is Docker",
        template="[hello|hi] my name is *",
    )

    assert result


def test_default_matcher_fail():
    message_with_template_matcher = DefaultMessageWithTemplateMatcher()

    result = message_with_template_matcher.match_message_with_template(
        message="hallo my name is Docker",
        template="[hello|hi] my name is *",
    )

    assert not result
