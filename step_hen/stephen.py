# -*- coding: utf-8 -*-

# Copyright (c) 2021, J. D. Mitchell + Maria Tsalakou
#
# Distributed under the terms of the GPL license version 3.
#
# The full license is in the file LICENSE, distributed with this software.

r"""
This module contains the single class :py:class:`Stephen` which implements a
version of Stephen's procedure for computing the size and number of
:math:`\mathscr{R}`-classes of a finitely presented inverse monoid.
"""

from typing import List

from step_hen.schutzenbergergraph import (
    InverseMonoidPresentation,
    SchutzenbergerGraph,
)

from libsemigroups_pybind11 import ActionDigraph, follow_path


def make_ActionDigraph(adj):
    D = ActionDigraph(len(adj), len(adj[0]))
    for i, x in enumerate(adj):
        for j, y in enumerate(x):
            D.add_edge(i, y, j)
    return D


def check_normal_forms(D):
    nf = [
        next(D.pstislo_iterator(0, n, 0, 100000))
        for n in range(D.number_of_nodes())
    ]
    max_len = max([len(x) for x in nf])
    minimal_words = {}
    for w in D.pislo_iterator(0, 0, max_len + 1):
        node = follow_path(D, 0, w)
        if not node in minimal_words:
            minimal_words[node] = w
        else:
            u = minimal_words[node]
            if len(w) < len(u) or (len(w) == len(u) and w < u):
                return w, node, u


class Stephen:
    """
    The class encodes a rudimentary version of Stephen's procedure as described
    in :cite:`Cutting2001aa`
    """

    def __init__(self, presn: InverseMonoidPresentation) -> None:
        """
        Construct a new :py:class:`Stephen` from an inverse monoid presentation.

        :param presn: the inverse monoid presentation
        :type presn: InverseMonoidPresentation

        :returns: ``None``

        Example
        -------
        .. code-block:: python

            P = InverseMonoidPresentation()
            P.set_alphabet("xy")
            P.add_relation("xxx", "x")
            P.add_relation("yyyyy", "y")
            P.add_relation("xyxy", "xx")

            S = Stephen(P)
        """
        self._presn = presn
        self._orbit = [SchutzenbergerGraph(presn, "")]
        self._finished = False
        self._graph = []
        # self._graph[i][j] will contain the position of the SchutzenbergerGraph
        # in self._orbit containing the rep of self._orbit[i] left multiplied by
        # letter[j]

    def __run(self) -> None:
        if self._finished:
            return
        for i, sg1 in enumerate(self._orbit):
            word = sg1.rep
            self._graph.append([-1] * len(self._presn.alphabet))
            for letter in range(len(self._presn.alphabet)):
                rep = [letter] + word
                rep = rep + self._presn.inverse(rep)
                sg_xw = SchutzenbergerGraph(
                    self._presn, self._presn.string(rep)
                )
                for k, sg2 in enumerate(self._orbit):
                    if (
                        self._presn.string(rep) in sg2
                        and self._presn.string(sg2.rep) in sg_xw
                    ):
                        self._graph[i][letter] = k
                        break
                else:
                    self._graph[i][letter] = len(self._orbit)
                    self._orbit.append(sg_xw)
        self._finished = True

    def size(self) -> int:
        """
        Returns the size of the inverse monoid defined by the presentation used
        to define an instance of this type.

        :parameters: ``None``
        :returns: An ``int``.

        .. warning::
            The procedure implemented by method may never terminate. In
            particular, it terminates if and only if the inverse monoid defined
            by the inverse monoid presentation used to construct the class is
            finite. Even if the monoid defined by the presentation is finite,
            there is no bound on the run time of this method.

        Example
        -------
        .. code-block:: python

            P = InverseMonoidPresentation()
            P.set_alphabet("xy")
            P.add_relation("xxx", "x")
            P.add_relation("yyyyy", "y")
            P.add_relation("xyxy", "xx")

            S = Stephen(P)
            S.size()  # returns 13
        """
        self.__run()
        result = 0
        for schutz_graph in self._orbit:
            result += schutz_graph.number_of_nodes()
        return result

    def number_of_r_classes(self) -> int:
        r"""
        Returns the number of :math:`\mathscr{R}`-classes of the inverse monoid
        defined by the presentation used to define an instance of this type.

        :parameters: ``None``
        :returns: An ``int``.

        .. warning::
            The procedure implemented by method may never terminate. In
            particular, it terminates if and only if the inverse monoid defined
            by the inverse monoid presentation used to construct the class is
            finite. Even if the monoid defined by the presentation is finite,
            there is no bound on the run time of this method.

        Example
        -------
        .. code-block:: python

            P = InverseMonoidPresentation()
            P.set_alphabet("xy")
            P.add_relation("xxx", "x")
            P.add_relation("yyyyy", "y")
            P.add_relation("xyxy", "xx")

            S = Stephen(P)
            S.number_of_r_classes()  # returns 3
        """
        self.__run()
        return len(self._orbit)

    def normal_forms(self) -> List[str]:
        D = self.right_cayley_graph()
        return [
            self._presn.string(next(D.pstislo_iterator(0, n, 0, 100000)))
            for n in range(D.number_of_nodes())
        ]

    def normal_forms_by_r_class(self) -> List[List[str]]:
        # FIXME this is fragile
        nf = self.normal_forms()
        offset = 0
        result = []
        for sg in self.schutzenberger_graphs():
            result.append(nf[offset : offset + sg.number_of_nodes()])
            result[-1].sort(key=lambda s: (len(s), s))
            offset += sg.number_of_nodes()
        return result

    def schutzenberger_graphs(self) -> List[SchutzenbergerGraph]:
        self.__run()
        return self._orbit

    def schutzenberger_graph(self, word):
        # TODO improve just follow the path in the _graph
        self.__run()
        for sg in self.schutzenberger_graphs():
            if word in sg:
                return sg

    def equal_to(self, word1, word2) -> bool:
        return SchutzenbergerGraph(self._presn, word1).accepts(
            word2
        ) and SchutzenbergerGraph(self._presn, word2).accepts(word1)

    def _position(self, sg_index, node_index):
        assert node_index < self._orbit[sg_index].number_of_nodes()
        result = 0
        for i in range(sg_index):
            result += self.schutzenberger_graphs()[i].number_of_nodes()
        return result + node_index

    def left_cayley_graph(self) -> ActionDigraph:
        self.__run()
        m = len(self._presn.alphabet)
        result = [[None] * m for _ in range(self.size())]

        for i, sg in enumerate(self.schutzenberger_graphs()):
            for j, node in enumerate(sg.nodes):
                k = self._position(i, j)
                for x in range(m):
                    # xs_k = x product the element of the semigroup
                    # corresponding to the j-th node of the i-th Schutzenberger
                    # graph
                    l = self._graph[i][
                        x
                    ]  # index of the Schutzenberger graph containing xs_k
                    sg_l = self._orbit[l]
                    u = sg_l.path(
                        0, [x] + sg.rep
                    )  # node in the sg_l corresponding to x sg.rep
                    assert sg.path(0, list(sg.path_from_root_to(node))) == node
                    v = list(sg.path_from_root_to(node))
                    result[k][x] = self._position(
                        l, sg_l.nodes.index(sg_l.path(u, v))
                    )
        return make_ActionDigraph(result)

    def right_cayley_graph(self) -> ActionDigraph:
        left = self.left_cayley_graph()
        m = len(self._presn.alphabet)
        result = [[None] * m for _ in range(self.size())]
        for i in range(self.size()):
            w = next(left.pstislo_iterator(0, i, 0, 100000))[::-1]
            for x in range(m):
                u = w + [x]
                result[i][x] = follow_path(left, 0, list(reversed(u)))
        return make_ActionDigraph(result)

    def number_of_d_classes(self) -> int:
        m = len(self._presn.alphabet)
        union = ActionDigraph(self.left_cayley_graph())
        union.add_to_out_degree(m)
        right = self.right_cayley_graph()
        for v in range(right.number_of_nodes()):
            for x in range(m):
                union.add_edge(v, right.neighbor(v, x), x + m)
        return union.number_of_scc()

    def normal_form(self, word: str) -> str:
        D = self.right_cayley_graph()
        n = follow_path(D, 0, self._presn.word(word))
        return self._presn.string(next(D.pstislo_iterator(0, n, 0, 100000)))
