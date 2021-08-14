# -*- coding: utf-8 -*-

# Copyright (c) 2021, J. D. Mitchell + Maria Tsalakou
#
# Distributed under the terms of the GPL license version 3.
#
# The full license is in the file LICENSE, distributed with this software.

import unittest
from stephen import InverseMonoidPresentation


class TestInverseMonoidPresentation(unittest.TestCase):
    def test_001(self):
        P = InverseMonoidPresentation()
        P.set_alphabet("abc")

        self.assertEqual(P.word("abcAbC"), [0, 1, 2, 3, 1, 5])
        self.assertEqual(P.string([0, 1, 2, 3, 1, 5]), "abcAbC")
        self.assertEqual(P.inverse(0), 3)
        self.assertEqual(P.inverse(3), 0)
