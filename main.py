#!/usr/bin/env python

"""
Use this Python module to generate a random draw for Secret Santa.

Example usage:
1. In this file, edit NAMES, NUM_GIFTS, and optionally EXCLUDE_GROUPS (or comment it out).


"""


import logging

from .derangements import Permutation, random_derangements



logger = logging.getLogger(__name__)



NAMES = ["Denis", "Marie-Laure", "Brice", "Benja", "Robin", "Julie", "Charlotte", "Seb"]
NUM_GIFTS = 2
EXCLUDE_GROUPS = [["Denis", "Marie-Laure"], ["Brice", "Benja"], ["Robin", "Julie"], ["Charlotte", "Seb"]]



class SecretSanta():
    def __init__(
            self, names: list[str], 
            num_gifts: int = 1, 
            exclude_groups: list[list[str]] | None = None
        ) -> None:
        self.num_people = len(names)
        self.names = names
        self.num_gifts = num_gifts
        self.exclude_groups = exclude_groups

        indices : dict[str, int] = dict()
        for (i, name) in enumerate(names):
            indices[name] = i
        self.indices = indices


    def draw(self):
        exclusions = self._get_exclusions()
        perms : list[Permutation] = random_derangements(n=self.num_people, d=self.num_gifts, exclusions=exclusions)
        secret_lists : dict[str, list[str]] = dict()
        for i, name in enumerate(self.names):
            secret_lists[name] = [self.names[perm(i)] for perm in perms]
        print(f"")
        self.secret_lists = secret_lists


    def _get_exclusions(self) -> list[list[int]] | None:
        if not self.exclude_groups:
            return None
        exclusions : list[list[int]] = [[]]*self.num_people
        for group in self.exclude_groups:
            group_indices = [self.indices[name] for name in group]
            for name in group:
                exclusions[self.indices[name]] = group_indices.copy()
        return exclusions.copy()
    



# def write_message(gifter, giftees, gift_labels=None):
#     res = f"Hello {gifter} !\n"
#     for i, giftee in enumerate(giftees):
#         if gift_labels is None:
#             res += f"\nCadeau {i+1} : {giftee}"
#         else:
#             res += f"\nCadeau {i+1} ({gift_labels[i]}): {giftee}"
#     return res

def main(names : list[str], num_gifts : int = 1):
    santa = SecretSanta(names=names, num_gifts=num_gifts)
    santa.draw()



if __name__ == '__main__':
    main(names=NAMES, num_gifts=NUM_GIFTS)
