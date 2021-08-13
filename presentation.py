"""
TODO
"""


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

    def word(self, w: str) -> list[int]:
        return [self.letter(x) for x in w]

    def string(self, w: list[int]) -> str:
        return "".join(self.char(x) for x in w)

    def inverse(self, x: int) -> int:
        if x < len(self.A):
            return x + len(self.A)
        else:
            return x - len(self.A)

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
