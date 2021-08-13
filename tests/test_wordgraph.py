import unittest
from wordgraph import WordGraph, MonoidPresentation


class TestWordGraph(unittest.TestCase):
    def test_001(self):
        P = MonoidPresentation()
        P.set_alphabet("a")
        P.add_relation("aa", "a")

        S = WordGraph(P, "aa")
        self.assertTrue(S.equal_to("a"))
        self.assertTrue(S.equal_to("aa"))
        self.assertTrue(S.equal_to("aaa"))
        self.assertTrue(S.equal_to("aaaa"))

    def test_002(self):
        P = MonoidPresentation()
        P.set_alphabet("ab")
        P.add_relation("aaa", "a")
        P.add_relation("bbb", "b")
        P.add_relation("abab", "aa")

        S = WordGraph(P, "bbab")
        self.assertTrue(S.equal_to("bbaaba"))
        self.assertFalse(S.equal_to(""))
        self.assertFalse(S.equal_to("aaaaaaaaaa"))
        self.assertFalse(S.equal_to("bbb"))

        S = WordGraph(P, "bba")
        self.assertTrue(S.equal_to("bbabb"))
        self.assertTrue(S.equal_to("bba"))
        self.assertFalse(S.equal_to("bbb"))
        self.assertFalse(S.equal_to("a"))
        self.assertFalse(S.equal_to("ab"))

        S = WordGraph(P, "bbaab")
        self.assertTrue(S.equal_to("bbaba"))

    def test_003(self):
        P = MonoidPresentation()
        P.set_alphabet("abcdefg")
        P.add_relation("aaaeaa", "abcd")
        P.add_relation("ef", "dg")

        S = WordGraph(P, "aaaeaaaeaa")
        self.assertTrue(S.equal_to("aaaeabcd"))

        S = WordGraph(P, "abcef")
        self.assertTrue(S.equal_to("aaaeaag"))

    def test_004(self):
        P = MonoidPresentation()
        P.set_alphabet("abc")
        P.add_relation("ab", "ba")
        P.add_relation("ac", "cc")
        P.add_relation("ac", "a")
        P.add_relation("cc", "a")
        P.add_relation("bc", "cc")
        P.add_relation("bcc", "b")
        P.add_relation("bc", "b")
        P.add_relation("cc", "b")
        P.add_relation("a", "b")

        S = WordGraph(P, "abcc")
        self.assertTrue(S.equal_to("baac"))

    def test_005(self):
        P = MonoidPresentation()
        P.set_alphabet("abcd")
        P.add_relation("bb", "c")
        P.add_relation("caca", "abab")
        P.add_relation("bc", "d")
        P.add_relation("cb", "d")
        P.add_relation("aa", "d")
        P.add_relation("ad", "a")
        P.add_relation("da", "a")
        P.add_relation("bd", "b")
        P.add_relation("db", "b")
        P.add_relation("cd", "c")
        P.add_relation("dc", "c")

        S = WordGraph(P, "dabdaaadabab")
        self.assertTrue(S.equal_to("abdadcaca"))
