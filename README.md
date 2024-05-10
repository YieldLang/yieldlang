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

## [Read the docs](https://docs.yieldlang.com/)

YieldLang is a [meta-language](https://en.wikipedia.org/wiki/Metalanguage) for generating structured text (ST) that can provide corpora for large language models (LLMs) or guide LLMs to generate ST. Currently provided as a Python package.

- Based on a coroutine generator and sampler architecture
- Stream-sends characters and parses the context above into a syntax tree
- Build formal grammars with classes, methods, and combinators

**Work in progress now.**

## Simple Usage

```bash
pip install yieldlang
```

Use combinators (e.g., `select`, `repeat`, `join`, etc.) to define grammar rules. For example, for JSON values:

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
value = object | array | string | number | boolean | null
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

```py
def repeat4(s):
    l = []
    for _ in range(4):
        l.append((yield s))
    return "".join(l)
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

Release the YieldLang package.

- Visit: [RELEASE_PROCESS.md](./RELEASE_PROCESS.md)

## Acknowledgements

- Python package template at [github.com/allenai/python-package-template](https://github.com/allenai/python-package-template)
