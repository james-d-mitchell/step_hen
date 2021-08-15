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

from step_hen.presentation import MonoidPresentation, InverseMonoidPresentation
from step_hen.wordgraph import WordGraph
from step_hen.schutzenbergergraph import SchutzenbergerGraph
from step_hen.stephen import Stephen
