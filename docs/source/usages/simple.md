Simple Usage
===

Import the `TextGenerator` class and define a generator. The `top` method always serves as the entry point for the generator. You can treat the generator as an iterator and use a `for` loop to iterate over the generated text. For example:

```py
from yieldlang import TextGenerator

class G(TextGenerator):
    def top(self):
        yield "Hello, World!"

for text in G():
    print(text)
```

Set another sampler for the generator (default is random sampling). For example, set the large language model sampler:

```py
sampler = MyLLMSampler()
print(list(G(sampler)))
```

Use combinators (e.g., `select`, `repeat`, `join`, etc.) to define grammar rules in the `TextGenerator`. For example, for JSON values:


```py
def value(self):
    yield select(
        self.object,
        self.array,
        self.string,
        self.number,
        self.boolean,
        self.null
    )
```

This is equivalent to the EBNF form:

```ebnf
value = object 
      | array
      | string
      | number
      | boolean
      | null
```

Generate a sequence easily. For example:

```py
def array(self):
    yield select(
        ('[', self.ws, ']'),
        ('[', self.elements, ']')
    )
```

You can get the string just generated and add branches, loops, and other control structures to the generation rules. For example:

```py
def diagram(self):
    match (yield self.diagram_type):
        case "flowchart":
            yield self.flowchart
        case "gannt":
            yield self.gannt
```

Use a loop statement in the generator. For example:

```py
def repeat4(self, s):
    l: list[str] = []
    for _ in range(4):
        l.append((yield s))
    self.do_my_own_thing(l)
```

Print the generated context tree (convertible to an abstract syntax tree):

```py
def print_context_tree():
    ctx = yield from G()
    print(ctx)
```