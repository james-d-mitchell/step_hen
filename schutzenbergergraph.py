#!/usr/bin/env python3

from presentation import InverseMonoidPresentation
from wordgraph import WordGraph


class SchutzenbergerGraph(WordGraph):
    """
    This class implements Stephen's procedure for (possibly) checking whether
    an arbitrary word in the free inverse monoid represents the same element of
    a finitely presented inverse monoid as a fixed word.

    Generators are represented by lower case letters and their inverses by
    upper case letters.

    The fixed word is set using the method `init`.

    The alphabet is set using the method `set_alphabet`, and relations can be
    added using `add_relation`.
    """

    def __init__(self, presn: InverseMonoidPresentation, rep: str):
        WordGraph.__init__(self, presn, rep)

    def target(self, c: int, a: int) -> int:
        result = WordGraph.target(self, c, a)
        self.edges[self.next_node - 1][self.presn.inverse(a)] = c
        return result

    def accepts(self, w: str) -> bool:
        self.run()
        w = [self.presn.letter(x) for x in w]
        return self.path(0, w) == self.path(0, self.rep)

    def __contains__(self, w: str) -> bool:
        self.run()
        w = [self.presn.letter(x) for x in w]
        return self.path(0, w) is not None

    def equal_to(self) -> None:
        pass


# Test case 1
P = InverseMonoidPresentation()
P.set_alphabet("abc")

S = SchutzenbergerGraph(P, "aBcAbC")
assert not S.accepts("BaAbaBcAbC")
assert S.accepts("aBcCbBcAbC")

S = SchutzenbergerGraph(P, "aBcCbBcAbC")
assert S.accepts("aBcAbC")

S = SchutzenbergerGraph(P, "BaAbaBcAbC")
assert S.accepts("aBcAbC")

# Test case 2
P = InverseMonoidPresentation()
P.set_alphabet("abc")

S = SchutzenbergerGraph(P, "aBbcaABAabCc")
assert S.path(0, P.word("aBbcaABAabCc")) == 3

# # Test case 3
P = InverseMonoidPresentation()
P.set_alphabet("xy")

S = SchutzenbergerGraph(P, "xxxyyy")
assert S.accepts("xxxyyyYYYXXXxxxyyy")

S = SchutzenbergerGraph(P, "xxxyyyYYYXXXxxxyyy")
assert S.accepts("xxxyyy")
assert not S.accepts("xxx")

# Test case 4
P = InverseMonoidPresentation()
P.set_alphabet("xy")
P.add_relation("xyXxyX", "xyX")

S = SchutzenbergerGraph(P, "xyXyy")

for i in range(10):
    assert S.accepts("x" + "y" * i + "Xyy")
assert not S.accepts("xXyx")
assert not S.accepts("xXxx")
assert not S.accepts("xXxy")
assert not S.accepts("xXxX")
assert not S.accepts("xXyY")

assert S.path(0, P.word("xyXyy")) == 5
assert S.path(0, P.word("xyXyy")) == 5

assert S.nodes == [0, 1, 4, 5]
assert S.edges == [
    [1, 4, None, None],
    [None, 1, 0, 1],
    [None, 1, 3, 1],
    [1, 4, None, None],
    [None, 5, None, 0],
    [None, None, None, 4],
    [None, None, 3, 2],
    [6, None, None, None],
]

# # Test case 5
P = InverseMonoidPresentation()
P.set_alphabet("xy")
P.add_relation("xyXxyX", "xyX")
P.add_relation("xyxy", "xy")

S = SchutzenbergerGraph(P, "xyXyy")

assert S.accepts("y")
assert S.accepts("xxxxxxxxxxxxx")
assert S.accepts("xyXxyxyxyxyxyXyy")

assert S.nodes == [0]
assert S.edges[0] == [0, 0, 0, 0]
assert S.path(0, P.word("xyXyy")) == 0

print("SUCCESS!")
