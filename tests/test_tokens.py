from coriander.tokenizers import DefaultTokenizer, TemplateTokenizer
from coriander.tokens import (
    AnyToken,
    AnyTokenInTemplateFinder,
    CharToken,
    CharTokenInTemplateFinder,
)


def test_char_token():
    template_tokenizer = TemplateTokenizer(token_in_template_finders=[])
    token_in_template_finder = CharTokenInTemplateFinder()

    find_token_in_template_result = token_in_template_finder.find_token_in_template(
        template="hello",
        template_tokenizer=template_tokenizer,
    )

    assert find_token_in_template_result
    assert find_token_in_template_result.token == CharToken(char="h")
    assert find_token_in_template_result.end == 1


def test_any_token():
    template_tokenizer = TemplateTokenizer(token_in_template_finders=[])
    token_in_template_finder = AnyTokenInTemplateFinder()

    find_token_in_template_result = token_in_template_finder.find_token_in_template(
        template="* hello",
        template_tokenizer=template_tokenizer,
    )

    assert find_token_in_template_result
    assert find_token_in_template_result.token == AnyToken()
    assert find_token_in_template_result.end == 1


def test_not_any_token():
    template_tokenizer = TemplateTokenizer(token_in_template_finders=[])
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
