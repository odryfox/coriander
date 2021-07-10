<p>A simple library for intent classification and named-entity recognition using templates.</p>

```python
# matching
from coriander.matching import DefaultMatcher

DefaultMatcher().match(
    template="[hello|hi] my name is *",
    message="hello my name is Coriander",
).success
# True

DefaultMatcher().match(
    template="[hello|hi] my name is *",
    message="hi my name is Millet",
).success
# True

DefaultMatcher().match(
    template="[hello|hi] my name is *",
    message="hallo my name is Galangal",
).success
# False

DefaultMatcher().match(
    template="[hello|hi]~greeting my name is *~name",
    message="hello my name is Galangal",
).context
# {'greeting': 'hello', 'name': 'Galangal'}


# generation
from coriander.generation import DefaultGenerator

DefaultGenerator().generate(
    template="[hello|hi]~greeting my name is *~name",
    context={'greeting': 'hello', 'name': 'Galangal'},
)
# 'hello my name is Galangal'
```
