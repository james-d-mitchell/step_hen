#!/usr/bin/env python3

from stephenfpinvmon import InverseMonoidPresentation, SchutzenbergerGraph


class Stephen:
    def __init__(self, presn: InverseMonoidPresentation):
        self.presn = presn
        self.orbit = [SchutzenbergerGraph(presn, "")]
        self.finished = False

    def run(self) -> None:
        if self.finished:
            return
        for sg1 in self.orbit:
            w = sg1.rep
            for x in range(2 * len(self.presn.A)):
                xw = [x] + w
                sg_xw = SchutzenbergerGraph(self.presn, P.string(xw))
                for sg2 in self.orbit:
                    if P.string(xw) in sg2 and P.string(sg2.rep) in sg_xw:
                        break
                else:
                    self.orbit.append(sg_xw)
        self.finished = True

    def size(self) -> int:
        self.run()
        result = 0
        for sg in self.orbit:
            result += sg.size()
        return result

    def number_of_r_classes(self) -> int:
        self.run()
        return len(self.orbit)


P = InverseMonoidPresentation()
P.set_alphabet("x")
P.add_relation("xx", "xxxx")

S = Stephen(P)
assert S.size() == 7
assert S.number_of_r_classes() == 4

P = InverseMonoidPresentation()
P.set_alphabet("xy")
P.add_relation("xxx", "x")
P.add_relation("yyyyy", "y")
P.add_relation("xyxy", "xx")

S = Stephen(P)
assert S.size() == 13
assert S.number_of_r_classes() == 3

P = InverseMonoidPresentation()
P.set_alphabet("xy")
P.add_relation("xxx", "x")
P.add_relation("yyy", "y")
P.add_relation("xyy", "yxx")

S = Stephen(P)
assert S.size() == 7
assert S.size() == 7
assert S.number_of_r_classes() == 4

P = InverseMonoidPresentation()
P.set_alphabet("xyz")
P.add_relation("xxxxx", "x")
P.add_relation("yyyyy", "y")
P.add_relation("zzzzz", "z")
P.add_relation("xyy", "yxx")
P.add_relation("xzz", "zxx")
P.add_relation("yzz", "zyy")

S = Stephen(P)
assert S.size() == 173
assert S.number_of_r_classes() == 8

P = InverseMonoidPresentation()
P.set_alphabet("xe")
P.add_relation("xxxx", "x")
P.add_relation("ee", "e")

S = Stephen(P)
assert S.number_of_r_classes() == 10
assert S.size() == 26

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
assert S.number_of_r_classes() == 8
assert S.size() == 34

print("SUCCESS!")
