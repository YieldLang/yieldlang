Development
===

## Clone

In order for `git` to create symbolic links correctly, on Windows you have to run as administrator (Linux users can ignore this):

```bash
git clone -c core.symlinks=true https://github.com/YieldLang/yieldlang.git
```

## Install

Install the package in editable mode with the development dependencies:

```bash
pip install -e ".[dev]"
```

## Make

```bash
make run-checks # Run all checks and tests
make build      # Build the package
make docs       # Build and watch the docs
```

## Release

Release the YieldLang package. Visit: [RELEASE_PROCESS.md](./RELEASE_PROCESS.md)

## Acknowledgements

- Python package template at [github.com/allenai/python-package-template](https://github.com/allenai/python-package-template)
