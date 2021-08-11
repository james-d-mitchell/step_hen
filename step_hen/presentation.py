# -*- coding: utf-8 -*-

# Copyright (c) 2021, J. D. Mitchell + Maria Tsalakou
#
# Distributed under the terms of the GPL license version 3.
#
# The full license is in the file LICENSE, distributed with this software.

"""
This module contains the classes :py:class:`MonoidPresentation` and
:py:class:`InverseMonoidPresentation` which can be used to define
presentations. These serve as part of the input to the main algorithms
implemented in this package in :py:class:`stephen.wordgraph.WordGraph`,
:py:class:`stephen.schutzenbergergraph.SchutzenbergerGraph`, and
:py:class:`stephen.Stephen`.
"""

import typing


class MonoidPresentation:
    """
    This class is used to define monoid presentations.  The alphabet is set
    using the method :py:meth:`set_alphabet`, and relations can be added using
    :py:meth:`add_relation`.
    """

    def __init__(self):
        """
        Constructs an empty presentation.
        """
        self.alphabet = ""
        self.relations = []

    def letter(self, string: str) -> int:
        """
        Converts a string of length 1 to its index in the alphabet of this.

        This is the inverse of :py:meth:`char`.
        """
        assert len(string) == 1
        if not string[0] in self.alphabet:
            raise ValueError(
                "letter %s does not belong to the alphabet %s"
                % (string, self.alphabet)
            )
        return self.alphabet.index(string)

    def char(self, index: int) -> str:
        """
        Converts a integer to the corresponding letter of the alphabet of this
        .
        This is the inverse of :py:meth:`letter`.
        """
        assert index < len(self.alphabet)
        return self.alphabet[index]

    def word(self, string: str) -> typing.List[int]:
        """
        Converts a string to the corresponding list of ints.
        """
        return [self.letter(x) for x in string]

    def string(self, word: typing.List[int]) -> str:
        """
        Converts a list of ints to the corresponding string.
        """
        return "".join(self.char(x) for x in word)

    def set_alphabet(self, alphabet: str) -> None:
        """
        Set the alphabet of the presentation.

        :param alphabet: the string containing the alphabet.
        :returns: ``None``.
        :raises ValueError:
          If the alphabet has already been set.
        :raises ValueError:
          If the parameter ``alphabet`` contains duplicate letters.
        :raises TypeError:
          If the alphabet is not a string.`
        """
        if not isinstance(alphabet, str):
            raise TypeError("the argument <alphabet> must be a string")
        if self.alphabet != "":
            raise ValueError("the alphabet cannot be set more than once")

        letters = dict()
        for letter in alphabet:
            if letter in letters:
                raise ValueError(
                    "the argument <alphabet> must be duplicate free"
                )
            letters[letter] = True
        self.alphabet = alphabet

    def add_relation(self, word1: str, word2: str) -> None:
        """
        Add a relation to the presentation.

        :param word1: the left hand side of the relation to add.
        :param word2: the right hand side of the relation to add.
        :returns: ``None``.
        :raises ValueError:
          If the alphabet has not been defined.
        :raises ValueError:
          If ``word1`` or ``word2`` contains a letter not in the alphabet.
        :raises TypeError:
          If ``word1`` or ``word2`` is not a string.
        """
        if self.alphabet == "":
            raise ValueError("no alphabet defined, use set_alphabet() first")

        if not isinstance(word1, str):
            raise TypeError("the argument <word1> must be a string")
        if not isinstance(word2, str):
            raise TypeError("the argument <word2> must be a string")

        word1 = [self.letter(x) for x in word1]
        word2 = [self.letter(x) for x in word2]
        self.relations.append((word1, word2))


class InverseMonoidPresentation(MonoidPresentation):
    """
    This class is used to define inverse monoid presentations.  The alphabet is
    set using the method :py:meth:`set_alphabet`, and relations can be added
    using :py:meth:`add_relation`.

    Letters in the alphabet must be lower case, and upper case letters are used
    for the inverse of a letter.
    """

    def __init__(self):
        MonoidPresentation.__init__(self)

    def inverse(self, letter: int) -> int:
        """
        Return the index representing the inverse of ``letter``.
        """
        half = len(self.alphabet) // 2
        return letter + half if letter < half else letter - half

    def set_alphabet(self, alphabet: str) -> None:
        """
        Set the alphabet of the presentation.

        :param alphabet: the string containing the alphabet.
        :returns: ``None``.
        :raises ValueError:
          If the alphabet has already been set.
        :raises ValueError:
          If the parameter ``alphabet`` contains duplicate letters.
        :raises ValueError:
          If the parameter ``alphabet`` contains upper case letters.
        :raises TypeError:
          If the alphabet is not a string.`
        """
        if not all(x.islower() for x in alphabet):
            raise ValueError("the letters in the alphabet must be lower case")
        MonoidPresentation.set_alphabet(self, alphabet)  # for the exceptions
        self.alphabet += alphabet.upper()
