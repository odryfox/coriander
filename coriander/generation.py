from coriander.core import BaseMessageFromTemplateGenerator, BaseTemplateTokenizer
from coriander.tokenizers import DefaultTokenizer


class MessageFromTemplateGenerator(BaseMessageFromTemplateGenerator):
    def __init__(self, template_tokenizer: BaseTemplateTokenizer) -> None:
        self.template_tokenizer = template_tokenizer

    def generate_message_from_template(
        self,
        template: str,
    ) -> str:
        tokens = self.template_tokenizer.template_tokenize(template=template)

        message_parts = []

        for token in tokens:
            message_part = token.generate_message()
            message_parts.append(message_part)

        return "".join(message_parts)


class DefaultMessageFromTemplateGenerator(MessageFromTemplateGenerator):
    def __init__(self):
        template_tokenizer = DefaultTokenizer()
        super().__init__(template_tokenizer=template_tokenizer)
