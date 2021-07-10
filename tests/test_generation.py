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


def test_generation_with_associate_name():
    tokenizer = DefaultTokenizer()
    generator = Generator(tokenizer=tokenizer)
    template = "*~name hello"

    message = generator.generate(template=template, context={"name": "coriander"})

    assert message == "coriander hello"


def test_generation_optional_with_associate_name_true():
    tokenizer = DefaultTokenizer()
    generator = Generator(tokenizer=tokenizer)
    template = "(coriander)~name hello"

    message = generator.generate(template=template, context={"name": True})

    assert message == "coriander hello"


def test_generation_optional_with_associate_name_false():
    tokenizer = DefaultTokenizer()
    generator = Generator(tokenizer=tokenizer)
    template = "(coriander)~name hello"

    message = generator.generate(template=template, context={"name": False})

    assert message == " hello"


def test_generation_choice_with_associate_name():
    tokenizer = DefaultTokenizer()
    generator = Generator(tokenizer=tokenizer)
    template = "[coriander|galangal]~name hello"

    message = generator.generate(template=template, context={"name": "galangal"})

    assert message == "galangal hello"


def test_default_generation():
    generator = DefaultGenerator()
    template = "he*o"

    message = generator.generate(template=template)

    assert message[0] == "h"
    assert message[1] == "e"
    assert message[-1] == "o"

    assert len(message) > 3
