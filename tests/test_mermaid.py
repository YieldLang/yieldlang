from yieldlang.combinators import join, repeat, select
from yieldlang.generator import TextGenerator
from yieldlang.types import EmptyString


def test_base_flowchart():
    class G(TextGenerator):
        def top(self):
            self.nodes: set[str] = set()
            yield self.mermaid

        def mermaid(self):
            match (yield self.graph_name):
                case "flowchart":
                    yield self.flowchart

        def graph_name(self):
            yield select("flowchart")

        def flowchart(self):
            yield (" ", self.flowchart_dir, "\n")
            yield join("\n", self.flowchart_rules, depth=3)

        def flowchart_dir(self):
            yield select("TD", "LR")

        def flowchart_rules(self):
            single_line = (" " * 4, self.flowchart_rule)
            yield repeat(single_line, 30)

        def flowchart_rule(self):
            node1 = yield self.node
            yield " --> "
            node2 = yield self.node

            self.nodes |= set((node1, node2))

        def node(self):
            yield select(*range(1, 15), *self.nodes)

    mermaid_code = EmptyString.join(G())
    print(mermaid_code)


if __name__ == "__main__":
    test_base_flowchart()
