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
