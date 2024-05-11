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

[English](./README.md) | **简体中文**

## [阅读官方文档](https://docs.yieldlang.com/)

YieldLang 是一个生成结构化文本 (ST) 的[元语言](https://en.wikipedia.org/wiki/Metalanguage)，它可以为大语言模型 (LLM) 提供语料或引导 LLM 生成 ST 。目前以 [Python 软件包](https://pypi.org/project/yieldlang/)的方式提供。

- 🧠 采用基于协程的生成器、采样器架构
- 🤖 流式发送字符的并解析上文为语法树
- 🦾 用类、方法、组合子来构建形式文法


**目前还处于早期开发当中。**

## 简单使用

```bash
pip install yieldlang
```

导入 `TextGenerator` 类并定义生成器。其中 `top` 总是作为生成器的入口。你可以将生成器当作迭代器，用 `for` 循环来遍历生成的文本。例如：

```py
from yieldlang import TextGenerator

class G(TextGenerator):
    def top(self):
        yield "Hello, World!"

for text in G():
    print(text)
```

为生成器设置另一个采样器（默认是随机采样）。例如设置大语言模型采样器：

```py
sampler = MyLLMSampler()
print(list(G(sampler)))
```

在 `TextGenerator` 中使用组合子（例如 `select`, `repeat`, `join` 等）来定义文法规则。以 JSON 值为例：

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

这等价于 EBNF 形式：

```ebnf
value = object 
      | array
      | string
      | number
      | boolean
      | null
```

轻松的产生一个序列。例如：

```py
def array(self):
    yield select(
        ('[', self.ws, ']'),
        ('[', self.elements, ']')
    )
```


你可以获取刚刚产生的字符串，并为生成规则添加分支、循环等控制结构。例如：

```py
def diagram(self):
    match (yield self.diagram_type):
        case "flowchart":
            yield self.flowchart
        case "gannt":
            yield self.gannt
```

在生成器中使用循环语句。例如：

```py
def repeat4(self, s):
    l = []
    for _ in range(4):
        l.append((yield s))
    self.do_my_own_thing(l)
```

打印生成的上下文树（可转化为抽象语法树）：

```py
def print_context_tree():
    ctx = yield from G()
    print(ctx)
```

更多信息，请参考文档：[docs.yieldlang.com](https://docs.yieldlang.com/)

## 开发本项目

更多信息请参考 [CONTRIBUTING.md](./CONTRIBUTING.md)。

### Clone

为了让 `git` 正确创建符号链接，Windows 用户需要以管理员身份运行（Linux 请用户忽略）：

```bash
git clone -c core.symlinks=true https://github.com/YieldLang/yieldlang.git
```

### Install
 
以可编辑模式安装软件包，并安装开发依赖：

```bash
pip install -e ".[dev]"
```

### Make

```bash
make run-checks # 运行所有检查和测试
make build      # 构建软件包
make docs       # 构建并查看文档
```

### Release

发布 YieldLang 软件包。请参考: [RELEASE_PROCESS.md](./RELEASE_PROCESS.md)

## Publications

- [引导大语言模型生成计算机可解析内容](https://arxiv.org/abs/2404.05499)  
  作者：[王家晔](https://orcid.org/0009-0007-5832-2474) 日期：`2024-03-26 22:54:14`


## Acknowledgements

- Python 软件包参考了模板：[github.com/allenai/python-package-template](https://github.com/allenai/python-package-template)