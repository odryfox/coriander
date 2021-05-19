from coriander.generation import (
    DefaultMessageFromTemplateGenerator,
    MessageFromTemplateGenerator,
)
from coriander.tokenizers import DefaultTokenizer


def test_generation():
    template_tokenizer = DefaultTokenizer()
    generator = MessageFromTemplateGenerator(template_tokenizer=template_tokenizer)
    template = "he*o"

    message = generator.generate_message_from_template(template=template)

    assert message[0] == "h"
    assert message[1] == "e"
    assert message[-1] == "o"

    assert len(message) > 3


def test_default_generation():
    generator = DefaultMessageFromTemplateGenerator()
    template = "he*o"

    message = generator.generate_message_from_template(template=template)

    assert message[0] == "h"
    assert message[1] == "e"
    assert message[-1] == "o"

    assert len(message) > 3
