<h1 align="center">
<img src="https://raw.githubusercontent.com/YieldLang/yieldlang/main/docs/source/_static/logo.min.svg#gh-dark-mode-only" alt="YieldLang LOGO" width="38.2%"/>

<img src="https://raw.githubusercontent.com/YieldLang/yieldlang/main/docs/source/_static/logo.min.svg#gh-light-mode-only" alt="YieldLang LOGO" width="38.2%"/>
</h1>

<p align="center">
  <a href="https://github.com/YieldLang/yieldlang/actions"><img alt="GitHub Actions Workflow Status" src="https://github.com/yieldlang/yieldlang/actions/workflows/main.yml/badge.svg"/></a>
  <a href="https://docs.yieldlang.com/"><img alt="Documentation" src="https://readthedocs.org/projects/yieldlang/badge/?version=latest"/></a>
  <a href="https://github.com/YieldLang/yieldlang/blob/main/LICENSE"><img alt="Apache License, Version 2.0" src="https://img.shields.io/badge/License-Apache_2.0-blue.svg"/></a>
  <a href="https://github.com/YieldLang/yieldlang/commits/main/"><img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/yieldlang/yieldlang"/></a>
  <a href="https://pypi.org/project/yieldlang/"><img alt="PyPI - Wheel" src="https://img.shields.io/pypi/wheel/yieldlang"/></a>
</p>

**English** | [简体中文](./README.zh-hans.md)

## [Read the docs](https://docs.yieldlang.com/)

YieldLang is a [meta-language](https://en.wikipedia.org/wiki/Metalanguage) for generating structured text (ST) that can provide corpora for large language models (LLMs) or guide LLMs to generate ST. Currently provided as a [Python package](https://pypi.org/project/yieldlang/).

- 🧠 Based on a coroutine generator and sampler architecture
- 🤖 Stream-sends characters and parses the context above into a syntax tree
- 🦾 Build formal grammars with classes, methods, and combinators

**Work in progress now.**

## Simple Usage

```bash
pip install yieldlang
```

Import the `TextGenerator` class and define a generator. The `top` method always serves as the entry point for the generator. You can treat the generator as an iterator and use a `for` loop to iterate over the generated text. For example:

```py
from yieldlang import TextGenerator

class G(TextGenerator):
    def top(self):
        yield "Hello, World!"

for text in G():
    print(text)
```

Set a sampler for the generator. For example, set random sampling:

```py
from yieldlang import RandomSampler

sampler = RandomSampler()
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
        case "sequence":
            yield self.sequence
```

Use a loop statement in the generator. For example:

```py
def repeat4(self, s):
    l = []
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

For more documentation, please visit [docs.yieldlang.com](https://docs.yieldlang.com/).

## Development

For more information, please refer to [CONTRIBUTING.md](./CONTRIBUTING.md).  

### Clone

In order for `git` to create symbolic links correctly, on Windows you have to run as administrator (Linux users can ignore this):

```bash
git clone -c core.symlinks=true https://github.com/YieldLang/yieldlang.git
```

### Install

Install the package in editable mode with the development dependencies:

```bash
pip install -e ".[dev]"
```

### Make

```bash
make run-checks # Run all checks and tests
make build      # Build the package
make docs       # Build and watch the docs
```

### Release

Release the YieldLang package. Visit: [RELEASE_PROCESS.md](./RELEASE_PROCESS.md)

## Publications

- [Guiding Large Language Models to Generate Computer-Parsable Content](https://arxiv.org/abs/2404.05499)  
  Author: [Jiaye Wang](https://orcid.org/0009-0007-5832-2474) Date: `2024-03-26 22:54:14`


## Acknowledgements

- Python package template at [github.com/allenai/python-package-template](https://github.com/allenai/python-package-template)