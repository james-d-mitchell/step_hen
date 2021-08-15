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

from stephen.presentation import MonoidPresentation, InverseMonoidPresentation
from stephen.wordgraph import WordGraph
from stephen.schutzenbergergraph import SchutzenbergerGraph
from stephen.stephen import Stephen
