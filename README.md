<p>A simple library for intent classification and named-entity recognition using templates.</p>

```python
from coriander.matching import DefaultMatcher


DefaultMatcher().match(
    message="hello my name is Coriander",
    template="[hello|hi] my name is *",
)
# True

DefaultMatcher().match(
    message="hi my name is Millet",
    template="[hello|hi] my name is *",
)
# True

DefaultMatcher().match(
    message="hallo my name is Galangal",
    template="[hello|hi] my name is *",
)
# False
```
