#!/usr/bin/env python3


class Stephen1:
    # Directly from ToddCoxeter
    def __init__(self):
        self.A = ""
        self.R = []
        self.nodes = [0]
        self.edges = None
        self.kappa = []
        self.next_node = 1
        self.original_word = None

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
        for a in w:
            c = self.edges[c][a]
            if c is None:
                return None
        return c

    def tc3(self, i: int, j: int) -> bool:
        """Returns True if i and j are not equal and False if they are equal."""
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
    def set_linear_graph(self, w: str) -> None:
        self.original_word = [self.A.index(a) for a in w]
        current_node = 0
        for a in self.original_word:
            current_node = self.tc1(current_node, a)

    def elementary_expansion(self, n: int, u: list, v: list) -> None:
        # TODO check that n is a node
        uu = self.path(n, u)
        vv = self.path(n, v)
        if uu is not None:
            if vv is not None:
                if uu != vv:
                    self.kappa.append((uu, vv))
            else:
                i = 0
                for a in v:
                    m = self.edges[n][a]
                    if m is None:
                        break
                    n = m
                    i += 1
                for a in v[i:]:
                    n = self.tc1(n, a)
                self.kappa.append((n, uu))
        elif vv is not None:
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
        ww = [self.A.index(a) for a in w]
        return self.path(0, ww) == self.path(0, self.original_word)


S = Stephen1()
S.set_alphabet("a")
S.add_relation("aa", "a")
S.set_linear_graph("aaa")
S.run()
assert S.equal_to("a")
assert S.equal_to("aa")
assert S.equal_to("aaa")
assert S.equal_to("aaaa")

S = Stephen1()
S.set_alphabet("ab")
S.add_relation("aaa", "a")
S.add_relation("bbb", "b")
S.add_relation("abab", "aa")
S.set_linear_graph("bbab")
S.run()
assert S.equal_to("bbaaba")
S.set_linear_graph("bba")
S.run()
assert S.equal_to("bbabb")
S.set_linear_graph("bbaab")
S.run()
assert S.equal_to("bbaba")

S = Stephen1()
S.set_alphabet("abcdefg")
S.add_relation("aaaeaa", "abcd")
S.add_relation("ef", "dg")
S.set_linear_graph("aaaeaaaeaa")
S.run()
assert S.equal_to("aaaeabcd")
S.set_linear_graph("abcef")
S.run()
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
S.set_linear_graph("abcc")
S.run()
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
S.set_linear_graph("dabdaaadabab")
S.run()
S.equal_to("abdadcaca")
