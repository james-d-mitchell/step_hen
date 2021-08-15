# -*- coding: utf-8 -*-

# Copyright (c) 2021, J. D. Mitchell + Maria Tsalakou
#
# Distributed under the terms of the GPL license version 3.
#
# The full license is in the file LICENSE, distributed with this software.

"""
This module contains the single class :py:class:`SchutzenbergerGraph` which
implements a version of Stephen's procedure which can be used to check whether
two words in the free monoid represent the same element of a finitely presented
inverse monoid.
"""

from step_hen.presentation import InverseMonoidPresentation
from step_hen.wordgraph import WordGraph


class SchutzenbergerGraph(WordGraph):
    """
    This class implements Stephen's procedure for (possibly) checking whether
    an arbitrary word in the free inverse monoid represents the same element of
    a finitely presented inverse monoid as a fixed word.

    Generators are represented by lower case letters and their inverses by
    upper case letters.

    The alphabet is set using the method :py:meth:`set_alphabet`, and relations can be
    added using :py:meth:`add_relation`.
    """

    def __init__(self, presn: InverseMonoidPresentation, rep: str):
        """
        Construct from a monoid presentation and a representative.

        :param presn: the inverse monoid presentation.
        :param rep: the representative.
        """
        WordGraph.__init__(self, presn, rep)

    def target(self, node: int, letter: int) -> int:
        result = WordGraph.target(self, node, letter)
        self.edges[self.next_node - 1][self.presn.inverse(letter)] = node
        return result

    def accepts(self, word: str) -> bool:
        r"""
        Returns ``True`` if ``word`` is accepted by the Schutzenberger graph.
        This means that the paths starting at the first node ``0`` labelled by
        the representative and ``word`` are both defined and end at the same
        node.

        Two words in the free monoid are equal, in the finitely presented
        inverse monoid used to construct the Schutzenberger graph, if and only
        if their respective ``SchutzenbergerGraph`` objects both accept the
        other word.

        :param word: the word.
        :returns: a ``bool``.

        .. warning::
            The procedure implemented by method may never terminate. In
            particular, it terminates if and only if the
            :math:`\mathscr{R}`-class of the representative defined at
            construction is finite.  Even if the :math:`\mathscr{R}`-class is
            finite, there is no bound on the run time of this method.
        """
        self.run()
        word = [self.presn.letter(x) for x in word]
        return self.path(0, word) == self.path(0, self.rep)

    def __contains__(self, word: str) -> bool:
        r"""
        Returns ``True`` if ``word`` labels a path in the Schutzenberger graph.

        Two words in the free monoid represent elements in the finitely
        presented inverse monoid, used to define this, are
        :math:`\mathscr{R}`-related if and only if either word labels a path in
        the Schutzenberger graph of the other.

        :param word: The word.
        :returns: A ``bool``.

        .. warning::
            The procedure implemented by method may never terminate. In
            particular, it terminates if and only if the
            :math:`\mathscr{R}`-class of the representative defined at
            construction is finite.  Even if the :math:`\mathscr{R}`-class is
            finite.
        """
        self.run()
        word = [self.presn.letter(letter) for letter in word]
        return self.path(0, word) is not None

    def equal_to(self, word: str) -> None:
        pass
