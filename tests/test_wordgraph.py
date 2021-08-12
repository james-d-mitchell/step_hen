import unittest
from wordgraph import WordGraph, MonoidPresentation


class TestWordGraph(unittest.TestCase):
    def test_1(self):
        P = MonoidPresentation()
        P.set_alphabet("a")
        P.add_relation("aa", "a")

        S = WordGraph(P, "aa")
        self.assertTrue(S.equal_to("a"))
        self.assertTrue(S.equal_to("aa"))
        self.assertTrue(S.equal_to("aaa"))
        self.assertTrue(S.equal_to("aaaa"))

    def test_2(self):
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

    def test_3(self):
        P = MonoidPresentation()
        P.set_alphabet("abcdefg")
        P.add_relation("aaaeaa", "abcd")
        P.add_relation("ef", "dg")

        S = WordGraph(P, "aaaeaaaeaa")
        self.assertTrue(S.equal_to("aaaeabcd"))

        S = WordGraph(P, "abcef")
        self.assertTrue(S.equal_to("aaaeaag"))


#
# S = WordGraph()
# S.set_alphabet("abc")
# S.add_relation("ab", "ba")
# S.add_relation("ac", "cc")
# S.add_relation("ac", "a")
# S.add_relation("cc", "a")
# S.add_relation("bc", "cc")
# S.add_relation("bcc", "b")
# S.add_relation("bc", "b")
# S.add_relation("cc", "b")
# S.add_relation("a", "b")
# S.init("abcc")
# assert S.equal_to("baac")
#
# S = WordGraph()
# S.set_alphabet("abcd")
# S.add_relation("bb", "c")
# S.add_relation("caca", "abab")
# S.add_relation("bc", "d")
# S.add_relation("cb", "d")
# S.add_relation("aa", "d")
# S.add_relation("ad", "a")
# S.add_relation("da", "a")
# S.add_relation("bd", "b")
# S.add_relation("db", "b")
# S.add_relation("cd", "c")
# S.add_relation("dc", "c")
# S.init("dabdaaadabab")
# assert S.equal_to("abdadcaca")
#         S = FpSemigroup()
#         S.set_alphabet("abcde")
#         S.set_identity("e")
#         S.add_rule("cacac", "aacaa")
#         S.add_rule("acaca", "ccacc")
#         S.add_rule("ada", "bbcbb")
#         S.add_rule("bcb", "aadaa")
#         S.add_rule("aaaa", "e")
#         S.add_rule("ab", "e")
#         S.add_rule("ba", "e")
#         S.add_rule("cd", "e")
#         S.add_rule("dc", "e")
#         S.run()
#
#         self.assertEqual(S.nr_rules(), 18)
#         # self.assertEqual()
#         self.assertTrue(
#             S.equal_to(
#                 "abbbbbbbbbbbadddddddddddddddacccccccccccc",
#                 "aaccccccccccccccccccccccccccc",
#             )
#         )
#
#         self.assertFalse(
#             S.equal_to("abbbbbbbbbbbadddddddddddddddacccccccccccc", "a")
#         )
