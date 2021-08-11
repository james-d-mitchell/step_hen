#!/usr/bin/env python3


class Stephen1:
    """
    This class implements Stephen's procedure for (possibly) checking whether
    an arbitrary word in the free monoid represents the same element of a
    finitely presented monoid as a fixed word.

    The fixed word is set using the method `init`.

    The alphabet is set using the method `set_alphabet`, and relations can be
    added using `add_relation`.
    """

    # Directly from ToddCoxeter
    def __init__(self):
        self.A = ""
        self.R = []
        self.clear()

    def set_alphabet(self, A: str) -> None:
        self.A = A
        self.edges = [[None] * len(A)]

    def add_relation(self, u: str, v: str) -> None:
        u = [self.A.index(x) for x in u]
        v = [self.A.index(x) for x in v]
        self.R.append((u, v))

    def tc1(self, c: int, a: int) -> int:
        if self.edges[c][a] is None:
            self.nodes.append(self.next_node)
            self.edges[c][a] = self.next_node
            self.edges.append([None] * len(self.A))
            self.next_node += 1
        return self.edges[c][a]

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

    def tc3(self, i: int, j: int) -> bool:
        if i == j:
            return False
        if i > j:
            i, j = j, i

        for a in range(len(self.A)):
            if self.path(j, a) is not None:
                if self.path(i, a) is None:
                    self.edges[i][a] = self.path(j, a)
                else:
                    self.kappa.append((self.path(i, a), self.path(j, a)))
        for c in self.nodes:
            for a in range(len(self.A)):
                if self.path(c, a) == j:
                    self.edges[c][a] = i
        self.kappa = [[i, l] if k == j else [k, l] for k, l in self.kappa]
        self.kappa = [[k, i] if l == j else [k, l] for k, l in self.kappa]
        self.nodes.remove(j)
        return True

    # New for Stephen1

    def clear(self):
        self.nodes = [0]
        self.edges = [[None] * len(self.A)]
        self.kappa = []
        self.next_node = 1
        self.original_word = None

    def init(self, w: str) -> None:
        self.clear()
        self.original_word = [self.A.index(a) for a in w]
        current_node = 0
        for a in self.original_word:
            current_node = self.tc1(current_node, a)

    def elementary_expansion(self, n: int, u: list, v: list) -> None:
        uu = self.path(n, u)
        if uu is not None:
            n, i = self.last_node_on_path(n, v)
            for a in v[i:]:
                n = self.tc1(n, a)
            self.kappa.append((n, uu))
        else:
            self.elementary_expansion(n, v, u)

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

    def equal_to(self, w: str) -> bool:
        self.run()
        ww = [self.A.index(a) for a in w]
        return self.path(0, ww) == self.path(0, self.original_word)


S = Stephen1()
S.set_alphabet("a")
S.add_relation("aa", "a")
S.init("aaa")
assert S.equal_to("a")
assert S.equal_to("aa")
assert S.equal_to("aaa")
assert S.equal_to("aaaa")

S = Stephen1()
S.set_alphabet("ab")
S.add_relation("aaa", "a")
S.add_relation("bbb", "b")
S.add_relation("abab", "aa")
S.init("bbab")
assert S.equal_to("bbaaba")
assert not S.equal_to("")
assert not S.equal_to("aaaaaaaaaa")
assert not S.equal_to("bbb")
S.init("bba")
assert S.equal_to("bbabb")
assert S.equal_to("bba")
assert not S.equal_to("bbb")
assert not S.equal_to("a")
assert not S.equal_to("ab")
S.init("bbaab")
assert S.equal_to("bbaba")

S = Stephen1()
S.set_alphabet("abcdefg")
S.add_relation("aaaeaa", "abcd")
S.add_relation("ef", "dg")
S.init("aaaeaaaeaa")
assert S.equal_to("aaaeabcd")
S.init("abcef")
assert S.equal_to("aaaeaag")

S = Stephen1()
S.set_alphabet("abc")
S.add_relation("ab", "ba")
S.add_relation("ac", "cc")
S.add_relation("ac", "a")
S.add_relation("cc", "a")
S.add_relation("bc", "cc")
S.add_relation("bcc", "b")
S.add_relation("bc", "b")
S.add_relation("cc", "b")
S.add_relation("a", "b")
S.init("abcc")
assert S.equal_to("baac")

S = Stephen1()
S.set_alphabet("abcd")
S.add_relation("bb", "c")
S.add_relation("caca", "abab")
S.add_relation("bc", "d")
S.add_relation("cb", "d")
S.add_relation("aa", "d")
S.add_relation("ad", "a")
S.add_relation("da", "a")
S.add_relation("bd", "b")
S.add_relation("db", "b")
S.add_relation("cd", "c")
S.add_relation("dc", "c")
S.init("dabdaaadabab")
assert S.equal_to("abdadcaca")
