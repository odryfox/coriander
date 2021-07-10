from coriander.matching import DefaultMatcher, Matcher
from coriander.tokens import AnyToken, CharToken


def test_correct_message():
    tokens = [
        CharToken(char="h"),
        CharToken(char="e"),
        AnyToken(),
        CharToken(char="o"),
    ]
    match_tokens_with_message_results = Matcher(tokenizer=None).match_with_tokens(
        tokens=tokens,
        message="hello",
    )
    assert match_tokens_with_message_results[0].end == 5


def test_incorrect_message():
    tokens = [
        CharToken(char="h"),
        CharToken(char="e"),
        AnyToken(),
        CharToken(char="a"),
    ]
    match_tokens_with_message_results = Matcher(tokenizer=None).match_with_tokens(
        tokens=tokens,
        message="hello",
    )
    assert match_tokens_with_message_results == []


def test_tokens_and_empty_message():
    tokens = [
        CharToken(char="h"),
        CharToken(char="e"),
        AnyToken(),
        CharToken(char="o"),
    ]
    match_tokens_with_message_results = Matcher(tokenizer=None).match_with_tokens(
        tokens=tokens,
        message="",
    )
    assert match_tokens_with_message_results == []


def test_empty_tokens_and_empty_message():
    tokens = []
    match_tokens_with_message_results = Matcher(tokenizer=None).match_with_tokens(
        tokens=tokens,
        message="",
    )
    assert match_tokens_with_message_results[0].end == 0


def test_empty_tokens_and_message():
    tokens = []
    match_tokens_with_message_results = Matcher(tokenizer=None).match_with_tokens(
        tokens=tokens,
        message="hello",
    )
    assert match_tokens_with_message_results[0].end == 0


def test_any_variants():
    tokens = [
        AnyToken(),
        CharToken(char="e"),
    ]
    match_tokens_with_message_results = Matcher(tokenizer=None).match_with_tokens(
        tokens=tokens,
        message="hee",
    )
    assert match_tokens_with_message_results[0].end == 2
    assert match_tokens_with_message_results[1].end == 3


def test_any_token():
    tokens = [
        AnyToken(),
    ]
    match_tokens_with_message_results = Matcher(tokenizer=None).match_with_tokens(
        tokens=tokens,
        message="hee",
    )
    assert match_tokens_with_message_results[0].end == 1
    assert match_tokens_with_message_results[1].end == 2
    assert match_tokens_with_message_results[2].end == 3


def test_default_matcher_success():
    matcher = DefaultMatcher()

    result = matcher.match(
        message="hello my name is Docker",
        template="[hello|hi] my name is *",
    )

    assert result


def test_associate_name():
    matcher = DefaultMatcher()

    result = matcher.match(
        message="hello",
        template="[hello|hi]~greeting",
    )

    assert result
    assert result.context["greeting"] == "hello"


def test_associate_name_2():
    matcher = DefaultMatcher()

    result = matcher.match(
        message="hi",
        template="[hello|hi]~greeting",
    )

    assert result
    assert result.context["greeting"] == "hi"


def test_associate_name_nested():
    matcher = DefaultMatcher()

    result = matcher.match(
        message="millet",
        template="[[galangal|millet]~name|hi]~greeting",
    )

    assert result
    assert result.context["greeting"] == "millet"
    assert result.context["name"] == "millet"


def test_associate_name_nested_2():
    matcher = DefaultMatcher()

    result = matcher.match(
        message="hi",
        template="[[galangal|millet]~name|hi]~greeting",
    )

    assert result
    assert result.context["greeting"] == "hi"
    assert "name" not in result.context


def test_associate_name_few():
    matcher = DefaultMatcher()

    result = matcher.match(
        message="millet hello",
        template="[galangal|millet]~name [hello|hi]~greeting",
    )

    assert result
    assert result.context["name"] == "millet"
    assert result.context["greeting"] == "hello"


def test_associate_name_any():
    matcher = DefaultMatcher()

    result = matcher.match(
        message="millet hello",
        template="*~name hello",
    )

    assert result
    assert result.context["name"] == "millet"


def test_default_matcher_fail():
    matcher = DefaultMatcher()

    result = matcher.match(
        message="hallo my name is Docker",
        template="[hello|hi] my name is *",
    )

    assert not result
