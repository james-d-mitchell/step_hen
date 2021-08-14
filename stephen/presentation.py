# -*- coding: utf-8 -*-

# Copyright (c) 2021, J. D. Mitchell + Maria Tsalakou
#
# Distributed under the terms of the GPL license version 3.
#
# The full license is in the file LICENSE, distributed with this software.

"""
TODO
"""

import typing


class MonoidPresentation:
    def __init__(self):
        self.A = ""
        self.R = []

    def letter(self, x: str) -> int:
        assert len(x) == 1
        assert x[0] in self.A
        return self.A.index(x)

    def char(self, x: int) -> str:
        assert x < len(self.A)
        return self.A[x]

    def word(self, w: str) -> typing.List[int]:
        return [self.letter(x) for x in w]

    def string(self, w: typing.List[int]) -> str:
        return "".join(self.char(x) for x in w)

    def set_alphabet(self, A: str) -> None:
        self.A = A

    def add_relation(self, u: str, v: str) -> None:
        u = [self.letter(x) for x in u]
        v = [self.letter(x) for x in v]
        self.R.append((u, v))


class InverseMonoidPresentation(MonoidPresentation):
    def __init__(self):
        MonoidPresentation.__init__(self)

    def inverse(self, x: int) -> int:
        n = len(self.A) // 2
        return x + n if x < n else x - n

    def set_alphabet(self, A: str) -> None:
        assert all(x.islower() for x in A)
        self.A = A + A.upper()
