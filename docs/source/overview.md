Overview
========

YieldLang is a [meta-language](https://en.wikipedia.org/wiki/Metalanguage) for LLMs to process (produce and parse) structured info.

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
        self.null,
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

```{toctree}
RELEASE_PROCESS
```


## Acknowledgements

- Python package template at [github.com/allenai/python-package-template](https://github.com/allenai/python-package-template)
