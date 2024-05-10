import json
import random

from yieldlang.combinators import optional, repeat, select
from yieldlang.generator import TextGenerator
from yieldlang.tree import minify_ctx_tree
from yieldlang.types import EmptyString


def accept(range: tuple[str, str], invalids: tuple[str, ...]):
    start, end = map(ord, range)
    invalid_codes = set(map(ord, invalids))

    while True:
        code = random.randint(start, end)
        if code not in invalid_codes:
            yield chr(code)
            break


# fmt: off
class JSONGenerator(TextGenerator):
    def top(self):
        yield self.json

    def json(self):
        yield self.element

    def object(self):
        yield select(
            ('{', self.ws, '}'),
            ('{', self.members, '}')
        )

    def members(self):
        yield select(
            (self.member),
            (self.member, ',', self.members),
        )

    def member(self):
        yield (self.ws, self.string, self.ws, ':', self.element)

    def array(self):
        yield select(
            ('[', self.ws, ']'),
            ('[', self.elements, ']')
        )

    def elements(self):
        yield select(
            (self.element),
            (self.element, ',',  self.elements)
        )

    def string(self):
        yield ('"', self.characters, '"')

    def characters(self):
        yield optional(self.character, self.characters)

    def character(self):
        yield select(
            accept(range=('\u0020', '\uffff'), invalids=('"', '\\')),
            ('\\', self.escape)
        )

    def escape(self):
        yield select(
            *'\\"/bfnrt',
            ('u', repeat(self.hex, 4))
        )

    def hex(self):
        yield select(
            self.digit,
            select(*'ABCDEF'),
            select(*'abcdef'),
        )

    def digit(self):
        yield select('0', self.onenine)

    def onenine(self):
        yield select(*'123456789')

    def number(self):
        yield (self.integer, self.fraction, self.exponent)

    def integer(self):
        yield select(
            (self.digit),
            (self.onenine, self.digits),
            ('-', self.digit),
            ('-', self.onenine, self.digits)
        )

    def digits(self):
        yield select(
            (self.digit),
            (self.digit, self.digits)
        )

    def fraction(self):
        yield optional('.', self.digits)

    def exponent(self):
        yield optional(select(
            ('E', self.sign, self.digits),
            ('e', self.sign, self.digits),
        ))

    def sign(self):
        yield optional(select('+', '-'))

    def boolean(self):
        yield select('true', 'false')

    def null(self):
        yield 'null'

    def value(self):
        yield select(
            self.object,
            self.array,
            self.string,
            self.number,
            self.boolean,
            self.null,
        )

    def element(self):
        yield (self.ws, self.value, self.ws)

    def ws(self):
        yield optional(select(
            ('\u0020', self.ws),
            ('\u000A', self.ws),
            ('\u000D', self.ws),
            ('\u0009', self.ws),
        ))
# fmt: on


def test_base_json():
    for _ in range(10):
        json_text = EmptyString.join(JSONGenerator())
        json_obj = json.loads(json_text)
        json_classes = (dict, list, str, int, float, bool, type(None))
        assert isinstance(json_obj, json_classes)

    def gg():
        ret = yield from JSONGenerator()
        dic = minify_ctx_tree(ret)
        txt = json.dumps(dic, indent=2)
        print(txt)

    list(gg())


if __name__ == "__main__":
    test_base_json()
