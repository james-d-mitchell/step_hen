import unittest
from stephen import Stephen, InverseMonoidPresentation


class TestStephen(unittest.TestCase):
    def test_001(self):
        P = InverseMonoidPresentation()
        P.set_alphabet("x")
        P.add_relation("xx", "xxxx")

        S = Stephen(P)
        self.assertEqual(S.size(), 7)
        self.assertEqual(S.number_of_r_classes(), 4)

    def test_002(self):
        P = InverseMonoidPresentation()
        P.set_alphabet("xy")
        P.add_relation("xxx", "x")
        P.add_relation("yyyyy", "y")
        P.add_relation("xyxy", "xx")

        S = Stephen(P)
        self.assertEqual(S.size(), 13)
        self.assertEqual(S.number_of_r_classes(), 3)

    def test_003(self):
        P = InverseMonoidPresentation()
        P.set_alphabet("xy")
        P.add_relation("xxx", "x")
        P.add_relation("yyy", "y")
        P.add_relation("xyy", "yxx")

        S = Stephen(P)
        self.assertEqual(S.size(), 7)
        self.assertEqual(S.size(), 7)
        self.assertEqual(S.number_of_r_classes(), 4)

    def test_004(self):
        P = InverseMonoidPresentation()
        P.set_alphabet("xyz")
        P.add_relation("xxxxx", "x")
        P.add_relation("yyyyy", "y")
        P.add_relation("zzzzz", "z")
        P.add_relation("xyy", "yxx")
        P.add_relation("xzz", "zxx")
        P.add_relation("yzz", "zyy")

        S = Stephen(P)
        self.assertEqual(S.size(), 173)
        self.assertEqual(S.number_of_r_classes(), 8)

    def test_005(self):
        P = InverseMonoidPresentation()
        P.set_alphabet("xe")
        P.add_relation("xxxx", "x")
        P.add_relation("ee", "e")

        S = Stephen(P)
        self.assertEqual(S.number_of_r_classes(), 10)
        self.assertEqual(S.size(), 26)

    def test_006(self):
        P = InverseMonoidPresentation()
        P.set_alphabet("abc")

        P.add_relation("aaa", "")
        P.add_relation("bb", "")
        P.add_relation("Ab", "ba")
        P.add_relation("bA", "ab")
        P.add_relation("aba", "b")
        P.add_relation("bab", "A")
        P.add_relation("cb", "bc")
        P.add_relation("cc", "c")
        P.add_relation("bcA", "cab")
        P.add_relation("bcab", "cA")
        P.add_relation("Acac", "bcac")
        P.add_relation("abcac", "cac")
        P.add_relation("acAc", "cabc")
        P.add_relation("bacA", "Acab")
        P.add_relation("bacab", "AcA")
        P.add_relation("bacac", "acac")
        P.add_relation("cAca", "bcac")
        P.add_relation("cabca", "cac")
        P.add_relation("cacA", "cabc")
        P.add_relation("cacab", "caca")
        P.add_relation("Acabc", "cAc")
        P.add_relation("acacac", "cacac")
        P.add_relation("bcacac", "cacac")
        P.add_relation("cacaca", "cacac")

        S = Stephen(P)
        self.assertEqual(S.number_of_r_classes(), 8)
        self.assertEqual(S.size(), 34)
