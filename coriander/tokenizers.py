from typing import Iterable, List

from coriander.core import BaseTemplateTokenizer, BaseToken, BaseTokenInTemplateFinder
from coriander.tokens import AnyTokenInTemplateFinder, CharTokenInTemplateFinder


class TemplateTokenizer(BaseTemplateTokenizer):
    def __init__(
        self,
        token_in_template_finders: Iterable[BaseTokenInTemplateFinder],
    ) -> None:
        self.token_in_template_finders = token_in_template_finders

    def template_tokenize(self, template: str) -> List[BaseToken]:
        tokens = []

        while template:
            for token_in_template_finder in self.token_in_template_finders:
                find_result = token_in_template_finder.find_token_in_template(
                    template=template,
                    template_tokenizer=self,
                )
                if find_result:
                    tokens.append(find_result.token)
                    end = find_result.end
                    template = template[end:]

        return tokens


class DefaultTokenizer(TemplateTokenizer):
    def __init__(self) -> None:
        token_in_template_finders = [
            AnyTokenInTemplateFinder(),
            CharTokenInTemplateFinder(),
        ]

        super().__init__(token_in_template_finders=token_in_template_finders)
