<p>A simple library for intent classification and named-entity recognition using templates.</p>

```python
from coriander.matching import DefaultMessageWithTemplateMatcher


DefaultMessageWithTemplateMatcher().match_message_with_template(
    message="hello my name is Coriander",
    template="[hello|hi] my name is *",
)
# True

DefaultMessageWithTemplateMatcher().match_message_with_template(
    message="hi my name is Coriander",
    template="[hello|hi] my name is *",
)
# True

DefaultMessageWithTemplateMatcher().match_message_with_template(
    message="hallo my name is Coriander",
    template="[hello|hi] my name is *",
)
# False
```
