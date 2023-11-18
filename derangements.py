#!/usr/bin/env python

from typing import 
import random
import sqlalchemy


# https://stackoverflow.com/questions/25200220/generate-a-random-derangement-of-a-list
def random_derangement(n: int) -> tuple[int]:
    """
    Returns an n-tuple representing a derangement of a set of n elements
    """
    while True:
        v = [i for i in range(n)]
        for j in range(n - 1, -1, -1):
            p = random.randint(0, j)
            if v[p] == j:
                break
            else:
                v[j], v[p] = v[p], v[j]
        else:
            if v[0] != 0:
                return tuple(v)


def test

def is_derangement(s):
    for (i, x) in enumerate(s):
        if x == i:
            return False
    return True

def permutation_prod(u, v):
    """Returns the product of permutations w = u compose v"""
    n = len(u)
    w = [0] * n
    for i in range(n):
        w[i] = u[v[i]]
    return tuple(w)

def permutation_inverse(v):
    """Returns the inverse w=v^{-1} of a permutations v"""
    n = len(v)
    w = [0] * n
    for i, x in enumerate(v):
        w[x] = i
    return tuple(w)

def random_derangements(n, d):
    """Generates a list of derangements s_1, ... s_d, so that for any i != j, the product s_j * s_i^{-1}
    is still a derangement."""
    res = []
    while (len(res) < d):
        success = False
        while not success:
            next = random_derangement(n)
            success = True
            for s in res:
                if not is_derangement(permutation_prod(next, permutation_inverse(s))):
                    success = False
                    break
        res.append(next)
    return res

def write_message(gifter, giftees, gift_labels=None):
    res = f"Hello {gifter} !\n"
    for i, giftee in enumerate(giftees):
        if gift_labels is None:
            res += f"\nCadeau {i+1} : {giftee}"
        else:
            res += f"\nCadeau {i+1} ({gift_labels[i]}): {giftee}"
    return res

def santa_claus(names, nb_draws, gift_labels=None):
    n = len(names)
    d = nb_draws
    prods = random_derangements(n, d)
    for i in range(n):
        gifter = names[i]
        giftees = [names[prods[k][i]] for k in range(d)]
        message = write_message(gifter, giftees, gift_labels)
        with open(f"{gifter}.txt", "w") as f:
            f.write(message)

def main():
    santa_claus(names, nb_draws)

if __name__ == '__main__':
    main()
