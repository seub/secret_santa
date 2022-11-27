#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random



names = ["Denis", "Marie-Laure", "Brice", "Benja", "Robin", "Charlotte", "Seb"]
nb_draws = 3


# https://stackoverflow.com/questions/25200220/generate-a-random-derangement-of-a-list
def random_derangement(n):
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

def write_message(gifter, giftees):
    res = f"Hello {gifter}!\n"
    for i, giftee in enumerate(giftees):
        res += f"\nTirage {i+1}: {giftee}"
    return res

def santa_claus(names, nb_draws):
    n = len(names)
    d = nb_draws
    prods = random_derangements(n, d)
    for i in range(n):
        gifter = names[i]
        giftees = [names[prods[k][i]] for k in range(d)]
        message = write_message(gifter, giftees)
        with open(f"{gifter}.txt", "w") as f:
            f.write(message)

def main():
    santa_claus(names, nb_draws)

if __name__ == '__main__':
    main()
