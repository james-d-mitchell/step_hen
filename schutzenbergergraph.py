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
