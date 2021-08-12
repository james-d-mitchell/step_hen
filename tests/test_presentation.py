import unittest
from presentation import InverseMonoidPresentation


class TestInverseMonoidPresentation(unittest.TestCase):
    def test_001(self):
        P = InverseMonoidPresentation()
        P.set_alphabet("abc")

        assert P.word("abcAbC") == [0, 1, 2, 3, 1, 5]
        assert P.string([0, 1, 2, 3, 1, 5]) == "abcAbC"
