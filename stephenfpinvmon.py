#!/usr/bin/env python3


class Stephen2:
    """
    This class implements Stephen's procedure for (possibly) checking whether
    an arbitrary word in the free monoid represents the same element of
    a finitely presented inverse monoid as a fixed word.

    Generators are represented by lower case letters and their inverses by
    upper case letters.

    The fixed word is set using the method `init`.

    The alphabet is set using the method `set_alphabet`, and relations can be
    added using `add_relation`.
    """

    # From Stephen1
    def __init__(self):
        self.A = ""
        self.R = []
        self.clear()

    def add_relation(self, u: str, v: str) -> None:
        assert all(x in self.A for x in u.lower())
        assert all(x in self.A for x in v.lower())
        u = [self.letter(x) for x in u]
        v = [self.letter(x) for x in v]
        self.R.append((u, v))

    def tc3(self, i: int, j: int) -> bool:
        if i == j:
            return False
        if i > j:
            i, j = j, i

        for a in range(len(self.edges[0])):
            if self.path(j, a) is not None:
                if self.path(i, a) is None:
                    self.edges[i][a] = self.path(j, a)
                else:
                    self.kappa.append((self.path(i, a), self.path(j, a)))
        for c in self.nodes:
            for a in range(len(self.edges[0])):
                if self.path(c, a) == j:
                    self.edges[c][a] = i
        self.kappa = [[i, l] if k == j else [k, l] for k, l in self.kappa]
        self.kappa = [[k, i] if l == j else [k, l] for k, l in self.kappa]
        self.nodes.remove(j)
        return True

    def path(self, c: int, w: list) -> int:
        w = [w] if not isinstance(w, list) else w
        n, i = self.last_node_on_path(c, w)
        return n if i == len(w) else None

    def last_node_on_path(self, c: int, w) -> int:
        assert isinstance(w, list) or isinstance(w, int)
        w = [w] if not isinstance(w, list) else w
        for i in range(len(w)):
            d = self.edges[c][w[i]]
            if d is None:
                return (c, i)
            c = d
        return (c, len(w))

    def init(self, w: str) -> None:
        self.clear()
        self.original_word = [self.letter(a) for a in w]
        current_node = 0
        for a in self.original_word:
            current_node = self.tc1(current_node, a)

    # From Stephen1 almost
    def clear(self):
        self.nodes = [0]
        self.edges = [[None] * 2 * len(self.A)]
        self.kappa = []
        self.next_node = 1
        self.original_word = None

    def set_alphabet(self, A: str) -> None:
        assert all(x.islower() for x in A)
        self.A = A
        self.edges = [[None] * 2 * len(A)]

    def elementary_expansion(self, n: int, u: list, v: list) -> None:
        uu = self.path(n, u)
        if uu is not None:
            n, i = self.last_node_on_path(n, v)
            for a in v[i:]:
                n = self.tc1(n, a)
            self.kappa.append((n, uu))
        else:
            self.elementary_expansion(n, v, u)

    # New for Stephen2
    def letter(self, x: str) -> int:
        result = self.A.index(x.lower())
        if not x.islower():
            result += len(self.A)
        return result

    def inverse(self, x: int) -> int:
        if x < len(self.A):
            return x + len(self.A)
        else:
            return x - len(self.A)

    def tc1(self, c: int, a: int) -> int:
        if self.edges[c][a] is None:
            self.nodes.append(self.next_node)
            self.edges[c][a] = self.next_node
            self.edges.append([None] * 2 * len(self.A))
            self.edges[self.next_node][self.inverse(a)] = c
            self.next_node += 1
        return self.edges[c][a]

    def run(self) -> None:
        while True:
            n, u, v = next(
                (
                    (n, u, v)
                    for n in self.nodes
                    for u, v in self.R
                    if self.path(n, u) != self.path(n, v)
                ),
                (None, None, None),
            )
            if n is None:
                break
            self.elementary_expansion(n, u, v)
            assert self.path(n, u) is not None and self.path(n, v) is not None
            while len(self.kappa) != 0:
                self.tc3(*self.kappa.pop())

    def accepts(self, w: str) -> bool:
        self.run()
        w = [self.letter(x) for x in w]
        return self.path(0, w) == self.path(0, self.original_word)


# Test case 1
S = Stephen2()
S.set_alphabet("abc")
S.init("aBcAbC")
assert not S.accepts("BaAbaBcAbC")
assert S.accepts("aBcCbBcAbC")
S.init("aBcCbBcAbC")
assert S.accepts("aBcAbC")
S.init("BaAbaBcAbC")
assert S.accepts("aBcAbC")

# Test case 2
S = Stephen2()
S.set_alphabet("abc")
S.init("aBbcaABAabCc")
assert S.path(0, [S.letter(x) for x in "aBbcaABAabCc"]) == 3

# Test case 3
S = Stephen2()
S.set_alphabet("xy")
S.init("xxxyyy")
assert S.accepts("xxxyyyYYYXXXxxxyyy")
S.init("xxxyyyYYYXXXxxxyyy")
assert S.accepts("xxxyyy")
assert not S.accepts("xxx")

# Test case 4
S = Stephen2()
S.set_alphabet("xy")
S.add_relation("xyXxyX", "xyX")
S.init("xyXyy")

for i in range(10):
    assert S.accepts("x" + "y" * i + "Xyy")
assert not S.accepts("xXyx")
assert not S.accepts("xXxx")
assert not S.accepts("xXxy")
assert not S.accepts("xXxX")
assert not S.accepts("xXyY")

assert S.path(0, [S.letter(x) for x in "xyXyy"]) == 5
assert S.path(0, [S.letter(x) for x in "xyXyy"]) == 5

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

# Test case 5
S = Stephen2()
S.set_alphabet("xy")
S.add_relation("xyXxyX", "xyX")
S.add_relation("xyxy", "xy")
S.init("xyXyy")

assert S.accepts("y")
assert S.accepts("xxxxxxxxxxxxx")
assert S.accepts("xyXxyxyxyxyxyXyy")

assert S.nodes == [0]
assert S.edges[0] == [0, 0, 0, 0]
assert S.path(0, [S.letter(x) for x in "xyXyy"]) == 0
