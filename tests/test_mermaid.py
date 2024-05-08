from yieldlang.combinators import join, repeat, select
from yieldlang.generator import TextGenerator
from yieldlang.types import EmptyString


def test_base_flowchart():
    class G(TextGenerator):
        def top(self):
            yield self.mermaid

        def mermaid(self):
            match (yield self.graph_name):
                case "flowchart":
                    yield self.flowchart

        def graph_name(self):
            yield select("flowchart")

        def flowchart(self):
            yield (" ", self.flowchart_dir, "\n")
            yield join("\n", self.flowchart_rules(), depth=2)

        def flowchart_dir(self):
            yield select("TD", "LR")

        def flowchart_rules(self):
            single_line = (" " * 4, self.flowchart_rule)
            yield repeat(single_line, 50)

        def flowchart_rule(self):
            yield self.node
            yield " --> "
            yield self.node

        def node(self):
            yield select(*range(1, 50))

    print(EmptyString.join(G()))


if __name__ == "__main__":
    test_base_flowchart()
