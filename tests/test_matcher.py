from unittest import mock

from coriander.matching import DefaultMatcher, Matcher
from coriander.tokenizers import DefaultTokenizer
from coriander.tokens import AnyToken, CharToken


class TestMatcher:
    def test_match_with_tokens(self):
        tokens = [
            CharToken(char="h"),
            CharToken(char="e"),
            AnyToken(),
            CharToken(char="o"),
        ]
        tokenizer = mock.Mock()
        matcher = Matcher(tokenizer=tokenizer)

        match_tokens_with_message_results = matcher.match_with_tokens(
            tokens=tokens,
            message="hello",
        )

        assert match_tokens_with_message_results[0].end == 5
        assert match_tokens_with_message_results[0].context == {}

    def test_match_with_tokens__incorrect(self):
        tokens = [
            CharToken(char="h"),
            CharToken(char="e"),
            AnyToken(),
            CharToken(char="a"),
        ]
        tokenizer = mock.Mock()
        matcher = Matcher(tokenizer=tokenizer)

        match_tokens_with_message_results = matcher.match_with_tokens(
            tokens=tokens,
            message="hello",
        )

        assert match_tokens_with_message_results == []

    def test_match_with_tokens__empty_message(self):
        tokens = [
            CharToken(char="h"),
            CharToken(char="e"),
            AnyToken(),
            CharToken(char="o"),
        ]
        tokenizer = mock.Mock()
        matcher = Matcher(tokenizer=tokenizer)

        match_tokens_with_message_results = matcher.match_with_tokens(
            tokens=tokens,
            message="",
        )

        assert match_tokens_with_message_results == []

    def test_match_with_tokens__empty_tokens_and_empty_message(self):
        tokens = []
        tokenizer = mock.Mock()
        matcher = Matcher(tokenizer=tokenizer)

        match_tokens_with_message_results = matcher.match_with_tokens(
            tokens=tokens,
            message="",
        )

        assert match_tokens_with_message_results[0].end == 0
        assert match_tokens_with_message_results[0].context == {}

    def test_match_with_tokens__empty_tokens_and_message(self):
        tokens = []
        tokenizer = mock.Mock()
        matcher = Matcher(tokenizer=tokenizer)

        match_tokens_with_message_results = matcher.match_with_tokens(
            tokens=tokens,
            message="hello",
        )

        assert match_tokens_with_message_results[0].end == 0
        assert match_tokens_with_message_results[0].context == {}

    def test_match_with_tokens__few_variants(self):
        tokens = [
            AnyToken(),
            CharToken(char="e"),
        ]
        tokenizer = mock.Mock()
        matcher = Matcher(tokenizer=tokenizer)

        match_tokens_with_message_results = matcher.match_with_tokens(
            tokens=tokens,
            message="hee",
        )

        assert match_tokens_with_message_results[0].end == 2
        assert match_tokens_with_message_results[0].context == {}
        assert match_tokens_with_message_results[1].end == 3
        assert match_tokens_with_message_results[1].context == {}

    def test_match_with_tokens__any_token(self):
        tokens = [
            AnyToken(),
        ]
        tokenizer = mock.Mock()
        matcher = Matcher(tokenizer=tokenizer)

        match_tokens_with_message_results = matcher.match_with_tokens(
            tokens=tokens,
            message="hee",
        )

        assert match_tokens_with_message_results[0].end == 1
        assert match_tokens_with_message_results[0].context == {}
        assert match_tokens_with_message_results[1].end == 2
        assert match_tokens_with_message_results[1].context == {}
        assert match_tokens_with_message_results[2].end == 3
        assert match_tokens_with_message_results[2].context == {}

    def test_match__associate_name(self):
        tokenizer = DefaultTokenizer()
        matcher = Matcher(tokenizer=tokenizer)

        result = matcher.match(
            message="hello",
            template="[hello|hi]~greeting",
        )

        assert result
        assert result.success
        assert result.context["greeting"] == "hello"

    def test_match__associate_name_second_variant(self):
        tokenizer = DefaultTokenizer()
        matcher = Matcher(tokenizer=tokenizer)

        result = matcher.match(
            message="hi",
            template="[hello|hi]~greeting",
        )

        assert result
        assert result.success
        assert result.context["greeting"] == "hi"

    def test_match__associate_name_nested(self):
        tokenizer = DefaultTokenizer()
        matcher = Matcher(tokenizer=tokenizer)

        result = matcher.match(
            message="millet",
            template="[[galangal|millet]~name|hi]~greeting",
        )

        assert result
        assert result.success
        assert result.context["greeting"] == "millet"
        assert result.context["name"] == "millet"

    def test_match__associate_name_nested_second(self):
        tokenizer = DefaultTokenizer()
        matcher = Matcher(tokenizer=tokenizer)

        result = matcher.match(
            message="hi",
            template="[[galangal|millet]~name|hi]~greeting",
        )

        assert result
        assert result.success
        assert result.context["greeting"] == "hi"
        assert "name" not in result.context

    def test_match__associate_name_few(self):
        tokenizer = DefaultTokenizer()
        matcher = Matcher(tokenizer=tokenizer)

        result = matcher.match(
            message="millet hello",
            template="[galangal|millet]~name [hello|hi]~greeting",
        )

        assert result
        assert result.success
        assert result.context["name"] == "millet"
        assert result.context["greeting"] == "hello"

    def test_match__associate_name_any(self):
        tokenizer = DefaultTokenizer()
        matcher = Matcher(tokenizer=tokenizer)

        result = matcher.match(
            message="millet hello",
            template="*~name hello",
        )

        assert result
        assert result.success
        assert result.context["name"] == "millet"

    def test_match__int_token_with_associate_name(self):
        tokenizer = DefaultTokenizer()
        matcher = Matcher(tokenizer=tokenizer)

        result = matcher.match(
            message="25 years old",
            template="INT~age years old",
        )

        assert result
        assert result.success
        assert result.context["age"] == 25


class TestDefaultMatcher:
    def test_match(self):
        matcher = DefaultMatcher()

        result = matcher.match(
            message="hello my name is Docker",
            template="[hello|hi] my name is *",
        )

        assert result
        assert result.success
        assert result.context == {}

    def test_match__incorrect(self):
        matcher = DefaultMatcher()

        result = matcher.match(
            message="hallo my name is Docker",
            template="[hello|hi] my name is *",
        )

        assert not result
        assert not result.success
        assert result.context == {}
