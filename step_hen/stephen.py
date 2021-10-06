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
        self.__run()
        result = []
        for schutz_graph in self._orbit:
            result += schutz_graph.normal_forms()
        return result

    def schutzenberger_graphs(self) -> List[SchutzenbergerGraph]:
        self.__run()
        return self._orbit

    def equal_to(self, word1, word2) -> bool:
        return SchutzenbergerGraph(self._presn, word1).accepts(
            word2
        ) and SchutzenbergerGraph(self._presn, word2).accepts(word1)

    def __position(self, sg_index, node_index):
        result = 0
        for i in range(sg_index):
            result += self.schutzenberger_graphs()[i].number_of_nodes()
        return result + node_index

    def __inverse_position(self, index: int):  # -> Tuple[int, int]:
        sg_index = 0
        while index > self._orbit[sg_index].number_of_nodes():
            index -= self._orbit[sg_index].number_of_nodes()
            sg_index += 1
        return sg_index, index

    def __schutzenberger_graph(self, index: int) -> SchutzenbergerGraph:
        return self._orbit[self.__inverse_position(index)[0]]

    def left_cayley_graph(self) -> List[List[int]]:
        self.__run()
        result = [[None] * self._presn.number_of_generators()] * self.size()

        for i, sg in enumerate(self.schutzenberger_graphs()):
            index = __position(i, 0)
            for x in range(self._presn.number_of_generators()):
                sg_index = self._graph[i][x]
                result[index][x] = __position(sg_index,
                        self._orbit[sg_index].nodes.index(self._orbit[sg_index].path(
                    0, [x] + sg.rep
                ))

        for i, sg in enumerate(self.schutzenberger_graphs()):
            for j, node in enumerate(sg.nodes):
                k = __position(i, j)  # index of the element of the semigroup
                # corresponding to the jth node in the ith Schutzenberger graph
                for x in range(self._presn.number_of_generators()):
                    result[k][x] = __schutzenbergergraph(result[rep][x]).path(
                        sg.path_from_root_to(node)
                    )

    def normal_form(self, word: str) -> str:
        self.__run()
        for sg in self.schutzenberger_graphs():
            result = sg.normal_form(word)
            if result is not None:
                return result
        assert False
