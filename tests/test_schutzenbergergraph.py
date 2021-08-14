# -*- coding: utf-8 -*-

# Copyright (c) 2021, J. D. Mitchell + Maria Tsalakou
#
# Distributed under the terms of the GPL license version 3.
#
# The full license is in the file LICENSE, distributed with this software.

import unittest
from stephen import SchutzenbergerGraph, InverseMonoidPresentation


class TestSchutzenbergerGraph(unittest.TestCase):
    def test_001(self):
        P = InverseMonoidPresentation()
        P.set_alphabet("abc")

        S = SchutzenbergerGraph(P, "aBcAbC")
        self.assertFalse(S.accepts("BaAbaBcAbC"))
        self.assertTrue(S.accepts("aBcCbBcAbC"))

        S = SchutzenbergerGraph(P, "aBcCbBcAbC")
        self.assertTrue(S.accepts("aBcAbC"))

        S = SchutzenbergerGraph(P, "BaAbaBcAbC")
        self.assertTrue(S.accepts("aBcAbC"))

    def test_002(self):
        P = InverseMonoidPresentation()
        P.set_alphabet("abc")

        S = SchutzenbergerGraph(P, "aBbcaABAabCc")
        self.assertEqual(S.path(0, P.word("aBbcaABAabCc")), 3)

    def test_003(self):
        P = InverseMonoidPresentation()
        P.set_alphabet("xy")

        S = SchutzenbergerGraph(P, "xxxyyy")
        self.assertTrue(S.accepts("xxxyyyYYYXXXxxxyyy"))

        S = SchutzenbergerGraph(P, "xxxyyyYYYXXXxxxyyy")
        self.assertTrue(S.accepts("xxxyyy"))
        self.assertFalse(S.accepts("xxx"))

    def test_004(self):
        P = InverseMonoidPresentation()
        P.set_alphabet("xy")
        P.add_relation("xyXxyX", "xyX")

        S = SchutzenbergerGraph(P, "xyXyy")

        for i in range(10):
            self.assertTrue(S.accepts("x" + "y" * i + "Xyy"))
        self.assertFalse(S.accepts("xXyx"))
        self.assertFalse(S.accepts("xXxx"))
        self.assertFalse(S.accepts("xXxy"))
        self.assertFalse(S.accepts("xXxX"))
        self.assertFalse(S.accepts("xXyY"))

        self.assertEqual(S.path(0, P.word("xyXyy")), 5)
        self.assertEqual(S.path(0, P.word("xyXyy")), 5)

        self.assertEqual(S.nodes, [0, 1, 4, 5])
        self.assertEqual(
            S.edges,
            [
                [1, 4, None, None],
                [None, 1, 0, 1],
                [None, 1, 3, 1],
                [1, 4, None, None],
                [None, 5, None, 0],
                [None, None, None, 4],
                [None, None, 3, 2],
                [6, None, None, None],
            ],
        )

    def test_005(self):
        P = InverseMonoidPresentation()
        P.set_alphabet("xy")
        P.add_relation("xyXxyX", "xyX")
        P.add_relation("xyxy", "xy")

        S = SchutzenbergerGraph(P, "xyXyy")

        self.assertTrue(S.accepts("y"))
        self.assertTrue(S.accepts("xxxxxxxxxxxxx"))
        self.assertTrue(S.accepts("xyXxyxyxyxyxyXyy"))

        self.assertEqual(S.nodes, [0])
        self.assertEqual(S.edges[0], [0, 0, 0, 0])
        self.assertEqual(S.path(0, P.word("xyXyy")), 0)
