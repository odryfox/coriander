from coriander.matching import MessageWithTokensMatcher
from coriander.tokens import AnyToken, CharToken


def test_correct_message():
    tokens = [
        CharToken(char="h"),
        CharToken(char="e"),
        AnyToken(),
        CharToken(char="o"),
    ]
    match_result = MessageWithTokensMatcher().match_message_with_tokens(
        message="hello",
        tokens=tokens,
    )
    assert match_result


def test_incorrect_message():
    tokens = [
        CharToken(char="h"),
        CharToken(char="e"),
        AnyToken(),
        CharToken(char="a"),
    ]
    match_result = MessageWithTokensMatcher().match_message_with_tokens(
        message="hello",
        tokens=tokens,
    )
    assert not match_result


def test_empty_message_and_non_empty_tokens():
    tokens = [
        CharToken(char="h"),
        CharToken(char="e"),
        AnyToken(),
        CharToken(char="o"),
    ]
    match_result = MessageWithTokensMatcher().match_message_with_tokens(
        message="",
        tokens=tokens,
    )
    assert not match_result


def test_empty_message_and_empty_tokens():
    tokens = []
    match_result = MessageWithTokensMatcher().match_message_with_tokens(
        message="",
        tokens=tokens,
    )
    assert match_result


def test_message_and_tokens():
    tokens = []
    match_result = MessageWithTokensMatcher().match_message_with_tokens(
        message="hello",
        tokens=tokens,
    )
    assert not match_result
