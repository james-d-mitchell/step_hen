# -*- coding: utf-8 -*-

# Copyright (c) 2021, J. D. Mitchell + Maria Tsalakou
#
# Distributed under the terms of the GPL license version 3.
#
# The full license is in the file LICENSE, distributed with this software.

"""
This module contains the single class :py:class:`WordGraph` which
implements a version of Stephen's procedure which can be used to check whether
two words in the free monoid represent the same element of a finitely presented
monoid.
"""

from typing import Union, List, Tuple
from step_hen.presentation import MonoidPresentation


class WordGraph:
    """
    This class implements Stephen's procedure for (possibly) checking whether
    an arbitrary word in the free monoid represents the same element of a
    finitely presented monoid as a fixed word.

    The finite monoid presentation and fixed word are set at construction.

    """

    def __init__(self, presn: MonoidPresentation, rep: str):
        """
        Construct from a monoid presentation and a representative.

        :param presn: the monoid presentation.
        :param rep: the representative.
        """
        self.presn = presn
        self.nodes = [0]
        self.edges = [[None] * len(self.presn.alphabet)]
        self.kappa = []
        self.next_node = 1
        self.rep = [self.presn.letter(a) for a in rep]
        current_node = 0
        for letter in self.rep:
            current_node = self.target(current_node, letter)

    def number_of_nodes(self) -> int:
        """
        Returns the number of nodes in the graph.

        :parameters: ``None``
        :returns: An ``int``.
        """
        return len(self.nodes)

    def target(self, node: int, letter: int) -> int:
        """
        Returns the target node of the edge with source ``node`` and label
        ``letter``, if it exists, and adds a new node and edge if it does not.

        :param node: the source node.
        :param letter: the edge label.
        :returns: An ``int``.
        """
        if self.edges[node][letter] is None:
            self.nodes.append(self.next_node)
            self.edges[node][letter] = self.next_node
            self.edges.append([None] * len(self.presn.alphabet))
            self.next_node += 1
        return self.edges[node][letter]

    def last_node_on_path(
        self, root: int, word: Union[List[int], int]
    ) -> Tuple[int, int]:
        """
        Returns the last node on the path starting at ``root`` labelled by
        a prefix of ``word``.

        :param root: the root node.
        :param word: the word.
        :returns:
           A tuple consisting of the last node on the path and the
           corresponding index in ``word``.
        """
        assert isinstance(word, (list, int))
        word = [word] if not isinstance(word, list) else word
        for i, letter in enumerate(word):
            node = self.edges[root][letter]
            if node is None:
                return (root, i)
            root = node
        return (root, len(word))

    def path(self, node: int, word: List[int]) -> int:
        """
        Returns the target node on the path starting at ``root`` labelled by
        ``word`` if such a node exists and ``None`` otherwise.

        :param root: the root node.
        :param word: the word.
        :returns: An ``int``.
        """
        word = [word] if not isinstance(word, list) else word
        node, index = self.last_node_on_path(node, word)
        return node if index == len(word) else None

    def run(self) -> None:
        """
        Runs the algorithm.
        """
        while True:
            node, word1, word2 = next(
                (
                    (node, word1, word2)
                    for node in self.nodes
                    for word1, word2 in self.presn.relations
                    if self.path(node, word1) != self.path(node, word2)
                ),
                (None, None, None),
            )
            if node is None:
                break
            self.elementary_expansion(node, word1, word2)
            assert (
                self.path(node, word1) is not None
                and self.path(node, word2) is not None
            )
            while len(self.kappa) != 0:
                self.merge_nodes(*self.kappa.pop())

    def equal_to(self, word: str) -> bool:
        """
        Returns ``True`` if the argument is equal to the word used to construct
        this instance, and ``False`` if it does not.

        :param word: the word.
        :returns: a ``bool``.

        .. warning::
            The procedure implemented by method may never terminate. In
            particular, it terminates if and only if the subgraph of the right
            Cayley graph of the finitely presented monoid induced by those
            vertices reachable from empty word and from which the
            representative is reachable is finite.  Even if the induced
            subgraph is finite, there is no bound on the run time of this
            method.
        """
        self.run()
        return self.path(0, self.presn.word(word)) == self.path(0, self.rep)

    def elementary_expansion(
        self, node: int, word1: List[int], word2: List[int]
    ) -> None:
        """
        Perform an "elementary expansion" starting at ``node`` using the
        relation ``(word1, word2)``.
        """
        target1 = self.path(node, word1)
        if target1 is not None:
            node, i = self.last_node_on_path(node, word2)
            for letter in word2[i:]:
                node = self.target(node, letter)
            self.kappa.append((node, target1))
        else:
            self.elementary_expansion(  # pylint: disable=arguments-out-of-order
                node, word2, word1
            )

    def merge_nodes(self, node1: int, node2: int) -> None:
        """
        Merge the nodes ``node1`` and ``node2``.
        """
        if node1 == node2:
            return
        if node1 > node2:
            node1, node2 = node2, node1

        for letter in range(len(self.presn.alphabet)):
            if self.path(node2, letter) is not None:
                if self.path(node1, letter) is None:
                    self.edges[node1][letter] = self.path(node2, letter)
                else:
                    self.kappa.append(
                        (self.path(node1, letter), self.path(node2, letter))
                    )
        for node in self.nodes:
            for letter in range(len(self.presn.alphabet)):
                if self.path(node, letter) == node2:
                    self.edges[node][letter] = node1
        self.kappa = [
            [node1, l] if k == node2 else [k, l] for k, l in self.kappa
        ]
        self.kappa = [
            [k, node1] if l == node2 else [k, l] for k, l in self.kappa
        ]
        self.nodes.remove(node2)
