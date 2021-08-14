# -*- coding: utf-8 -*-

# Copyright (c) 2021, J. D. Mitchell + Maria Tsalakou
#
# Distributed under the terms of the GPL license version 3.
#
# The full license is in the file LICENSE, distributed with this software.

"""
This module contains the single class :py:class:`WordGraph` which
implements a version of Stephen's procedure which can be used to check whether
two words in the free monoid represent the same element of a finitely presented monoid.
"""

from typing import Union, List
from stephen.presentation import MonoidPresentation


class WordGraph:
    """
    This class implements Stephen's procedure for (possibly) checking whether
    an arbitrary word in the free monoid represents the same element of a
    finitely presented monoid as a fixed word.

    The finite monoid presentation and fixed word are set at construction.

    The alphabet is set using the method `set_alphabet`, and relations can be
    added using `add_relation`.
    """

    def __init__(self, presn: MonoidPresentation, rep: str):
        self.presn = presn
        self.nodes = [0]
        self.edges = [[None] * len(self.presn.A)]
        self.kappa = []
        self.next_node = 1
        self.rep = [self.presn.letter(a) for a in rep]
        current_node = 0
        for a in self.rep:
            current_node = self.target(current_node, a)

    def number_of_nodes(self) -> int:
        return len(self.nodes)

    def target(self, c: int, a: int) -> int:
        if self.edges[c][a] is None:
            self.nodes.append(self.next_node)
            self.edges[c][a] = self.next_node
            self.edges.append([None] * len(self.presn.A))
            self.next_node += 1
        return self.edges[c][a]

    def last_node_on_path(self, root: int, word: Union[List[int], int]) -> int:
        assert isinstance(word, list) or isinstance(word, int)
        word = [word] if not isinstance(word, list) else word
        for i in range(len(word)):
            node = self.edges[root][word[i]]
            if node is None:
                return (root, i)
            root = node
        return (root, len(word))

    def path(self, c: int, w: List[int]) -> int:
        w = [w] if not isinstance(w, list) else w
        n, i = self.last_node_on_path(c, w)
        return n if i == len(w) else None

    def merge_nodes(self, node1: int, node2: int) -> None:
        if node1 == node2:
            return
        if node1 > node2:
            node1, node2 = node2, node1

        for a in range(len(self.presn.A)):
            if self.path(node2, a) is not None:
                if self.path(node1, a) is None:
                    self.edges[node1][a] = self.path(node2, a)
                else:
                    self.kappa.append(
                        (self.path(node1, a), self.path(node2, a))
                    )
        for c in self.nodes:
            for a in range(len(self.presn.A)):
                if self.path(c, a) == node2:
                    self.edges[c][a] = node1
        self.kappa = [
            [node1, l] if k == node2 else [k, l] for k, l in self.kappa
        ]
        self.kappa = [
            [k, node1] if l == node2 else [k, l] for k, l in self.kappa
        ]
        self.nodes.remove(node2)

    def elementary_expansion(self, n: int, u: List[int], v: List[int]) -> None:
        uu = self.path(n, u)
        if uu is not None:
            n, i = self.last_node_on_path(n, v)
            for a in v[i:]:
                n = self.target(n, a)
            self.kappa.append((n, uu))
        else:
            self.elementary_expansion(n, v, u)

    def run(self) -> None:
        while True:
            n, u, v = next(
                (
                    (n, u, v)
                    for n in self.nodes
                    for u, v in self.presn.R
                    if self.path(n, u) != self.path(n, v)
                ),
                (None, None, None),
            )
            if n is None:
                break
            self.elementary_expansion(n, u, v)
            assert self.path(n, u) is not None and self.path(n, v) is not None
            while len(self.kappa) != 0:
                self.merge_nodes(*self.kappa.pop())

    def equal_to(self, w: str) -> bool:
        self.run()
        return self.path(0, self.presn.word(w)) == self.path(0, self.rep)
