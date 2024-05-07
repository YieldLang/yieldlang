<h1 align="center">
<img src="https://raw.githubusercontent.com/YieldLang/yieldlang/main/docs/source/_static/logo.min.svg#gh-dark-mode-only" alt="YieldLang LOGO" width="38.2%"/>

<img src="https://raw.githubusercontent.com/YieldLang/yieldlang/main/docs/source/_static/logo.min.svg#gh-light-mode-only" alt="YieldLang LOGO" width="38.2%"/>
</h1>

<p align="center">
  <a href="https://github.com/YieldLang/yieldlang/actions"><img alt="GitHub Actions Workflow Status" src="https://github.com/yieldlang/yieldlang/actions/workflows/main.yml/badge.svg"/></a>
  <a href="https://docs.yieldlang.com/"><img alt="Documentation" src="https://readthedocs.org/projects/yieldlang/badge/?version=latest"/></a>
  <a href="https://github.com/YieldLang/yieldlang/blob/main/LICENSE"><img alt="GPL-3.0 License" src="https://img.shields.io/badge/license-GPLv3.0-brightgreen"/></a>
  <a href="https://github.com/YieldLang/yieldlang/commits/main/"><img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/yieldlang/yieldlang"/></a>
  <a href="https://pypi.org/project/yieldlang/"><img alt="PyPI - Wheel" src="https://img.shields.io/pypi/wheel/yieldlang"/></a>
</p>

## [Read the docs](https://docs.yieldlang.com/)

YieldLang is a meta-language for LLMs to generate structured information.

**Work in progress now.**

## Usage

```bash
pip install yieldlang
```

## Develop

### Clone

In order for `git` to create symbolic links correctly, on Windows you have to run as administrator:

```bash
git clone -c core.symlinks=true https://github.com/YieldLang/yieldlang.git
```

### Make

```bash
make run-checks
make build
make docs
```

### Release

- Visit: [RELEASE_PROCESS.md](./RELEASE_PROCESS.md)

## Acknowledgements

- Based on template: [github.com/allenai/python-package-template](https://github.com/allenai/python-package-template)