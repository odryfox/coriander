from typing import Optional

from coriander.core import BaseTokenFinder, BaseTokenizer, FindTokenInTemplateResult
from coriander.generation import DefaultGenerator, Generator
from coriander.tokenizers import DefaultTokenizer
from coriander.tokens import AnyToken


class TestGenerator:
    def test_generate(self):
        tokenizer = DefaultTokenizer()
        generator = Generator(tokenizer=tokenizer)
        template = "he*o"

        message = generator.generate(template=template)

        assert message[0] == "h"
        assert message[1] == "e"
        assert message[-1] == "o"

        assert len(message) > 3

    def test_generate__associate_name(self):
        tokenizer = DefaultTokenizer()
        generator = Generator(tokenizer=tokenizer)
        template = "*~name hello"

        message = generator.generate(template=template, context={"name": "coriander"})

        assert message == "coriander hello"

    def test_generate__optional_with_associate_name_true(self):
        tokenizer = DefaultTokenizer()
        generator = Generator(tokenizer=tokenizer)
        template = "(coriander)~name hello"

        message = generator.generate(template=template, context={"name": True})

        assert message == "coriander hello"

    def test_generate__optional_with_associate_name_false(self):
        tokenizer = DefaultTokenizer()
        generator = Generator(tokenizer=tokenizer)
        template = "(coriander)~name hello"

        message = generator.generate(template=template, context={"name": False})

        assert message == " hello"

    def test_generate__choice_with_associate_name_false(self):
        tokenizer = DefaultTokenizer()
        generator = Generator(tokenizer=tokenizer)
        template = "[coriander|galangal]~name hello"

        message = generator.generate(template=template, context={"name": "galangal"})

        assert message == "galangal hello"

    def test_generate__int_token_with_associate_name(self):
        tokenizer = DefaultTokenizer()
        generator = Generator(tokenizer=tokenizer)
        template = "INT~age years old"

        message = generator.generate(template=template, context={"age": 25})

        assert message == "25 years old"


class TestDefaultGenerator:
    def test_generate(self):
        generator = DefaultGenerator()
        template = "he*o"

        message = generator.generate(template=template)

        assert message[0] == "h"
        assert message[1] == "e"
        assert message[-1] == "o"

        assert len(message) > 3

    def test_generate__with_custom_token_finders(self):
        class AllTokenFinder(BaseTokenFinder):
            def find_in_template(
                self,
                template: str,
                tokenizer: "BaseTokenizer",
            ) -> Optional[FindTokenInTemplateResult]:
                return FindTokenInTemplateResult(
                    end=len(template),
                    token=AnyToken(),
                )

        custom_token_finders = [AllTokenFinder()]

        generator = DefaultGenerator(custom_token_finders=custom_token_finders)
        template = "he*o"

        message = generator.generate(template=template)

        assert message[0] != "h"
        assert message[1] != "e"
        assert message[-1] != "o"

        assert len(message) > 3
