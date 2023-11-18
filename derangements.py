#!/usr/bin/env python

"""
Module to manipulate Permutation objects. A Permutation represents the mathetical concept of
a permutation of a finite set. It is internally represented by a list of length n 
containing the integers 0, ..., n-1.

Recall that a derangement is a permutation without fixed points.
"""


import logging
import random



logger = logging.getLogger(__name__)



class Permutation:
    def __init__(
            self, 
            n: int, 
            v: list[int] | None = None,
            random_derangement: bool = False,
        ) -> None:
        assert(v is None or not random_derangement)

        self.n = n

        if v is not None:
            assert(len(v) == n)
            self.v = v.copy()
        else:
            if random_derangement:
                self.v = _get_random_derangement(n)
            else:
                self.v = list(range(n))


    def __call__(self, i: int) -> int:
        return self.v[i]


    def __mul__(self, other: 'Permutation') -> 'Permutation':
        """
        Returns the product of permutations result = self compose other
        """
        n = self.n
        assert(other.n == n)
        w : list[int] = [0] * n
        for i in range(n):
            w[i] = self.v[other.v[i]]
        return Permutation(n, w)
    

    def inverse(self) -> 'Permutation':
        n = self.n
        w : list[int] = [0] * n
        for i, x in enumerate(self.v):
            w[x] = i
        return Permutation(n=n, v=w)


    def is_derangement(self) -> bool:
        for (i, x) in enumerate(self.v):
            if x == i:
                return False
        return True


    def verifies_exclusions(self, exclusions: list[list[int]]) -> bool:
        assert(len(exclusions) == self.n)
        for (i, x) in enumerate(self.v):
            if x in exclusions[i]:
                return False
        return True


# https://stackoverflow.com/questions/25200220/generate-a-random-derangement-of-a-list
def _get_random_derangement(n: int) -> list[int]:
    """
    Returns an n-tuple representing a derangement of a set of n elements
    """

    logger.info("Initializing Permutation...")
    while True:
        v : list[int] = list(range(n))
        for j in range(n-1, -1, -1):
            p = random.randint(0, j)
            if v[p] == j:
                break
            else:
                v[j], v[p] = v[p], v[j]
        else:
            if v[0] != 0:
                return v



def random_derangements(n: int, d: int, exclusions: list[list[int]] | None = None ) -> list[Permutation]:
    """
    Generates a list of derangements s_1, ... s_d, so that for all i in range(n), 
    the values s_1[i], ..., s_d[i] are distinct.
    
    Optionally pass a list of exclusions: the resulting derangements must satisfy 
    s[i] not in exclusions[i].
    """
    res : list[Permutation] = []
    while (len(res) < d):
        success = False
        while not success:
            next = Permutation(n, random_derangement=True)
            if exclusions is not None and not next.verifies_exclusions(exclusions):
                success = False
                continue
            success = True
            for s in res:
                if not (next * s.inverse()).is_derangement():
                    success = False
                    break
        res.append(next) # type: ignore
    return res
