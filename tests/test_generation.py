from coriander.generation import DefaultGenerator, Generator
from coriander.tokenizers import DefaultTokenizer


def test_generation():
    tokenizer = DefaultTokenizer()
    generator = Generator(tokenizer=tokenizer)
    template = "he*o"

    message = generator.generate(template=template)

    assert message[0] == "h"
    assert message[1] == "e"
    assert message[-1] == "o"

    assert len(message) > 3


def test_default_generation():
    generator = DefaultGenerator()
    template = "he*o"

    message = generator.generate(template=template)

    assert message[0] == "h"
    assert message[1] == "e"
    assert message[-1] == "o"

    assert len(message) > 3
