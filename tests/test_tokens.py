from coriander.tokenizers import DefaultTokenizer, Tokenizer
from coriander.tokens import AnyToken, AnyTokenFinder, CharToken, CharTokenFinder


def test_char_token():
    tokenizer = Tokenizer(token_finders=[])
    token_finder = CharTokenFinder()

    token_find_result = token_finder.find(
        raw_template="hello",
        tokenizer=tokenizer,
    )

    assert token_find_result
    assert token_find_result.token == CharToken(char="h")
    assert token_find_result.end == 1


def test_any_token():
    tokenizer = Tokenizer(token_finders=[])
    token_finder = AnyTokenFinder()

    token_find_result = token_finder.find(
        raw_template="* hello",
        tokenizer=tokenizer,
    )

    assert token_find_result
    assert token_find_result.token == AnyToken()
    assert token_find_result.end == 1


def test_not_any_token():
    tokenizer = Tokenizer(token_finders=[])
    token_finder = AnyTokenFinder()

    token_find_result = token_finder.find(
        raw_template="hello",
        tokenizer=tokenizer,
    )

    assert token_find_result is None


def test_tokenizer():
    token_finders = [
        AnyTokenFinder(),
        CharTokenFinder(),
    ]
    tokenizer = Tokenizer(token_finders=token_finders)

    actual_tokens = tokenizer.tokenize(raw_template="* hello")

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

    actual_tokens = tokenizer.tokenize(raw_template="* hello")

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
