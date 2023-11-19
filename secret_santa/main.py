#!/usr/bin/env python

"""
Use this Python module to generate a random draw for Secret Santa.

Example usage:
1. In this file, edit NAMES, NUM_GIFTS, and optionally EXCLUDE_GROUPS (or comment it out).


"""


import logging
import pprint

from .derangements import Permutation, random_derangements
from .mail import send_gmail


logger = logging.getLogger(__name__)



NAMES = ["Nono", "Marie-Laure", "Brice", "Benja", "Robin", "Julie", "Charlotte", "Seb"]
EMAILS = {
    "Nono": "briceloustau@gmail.com",
    "Marie-Laure": "briceloustau@gmail.com",
    "Brice": "briceloustau@gmail.com",
    "Benja": "briceloustau@gmail.com",
    "Robin": "briceloustau@gmail.com",
    "Julie": "briceloustau@gmail.com",
    "Charlotte": "briceloustau@gmail.com",
    "Seb": "briceloustau@gmail.com",
}
NUM_GIFTS = 2
EXCLUDE_GROUPS = [["Nono", "Marie-Laure"], ["Brice", "Benja"], ["Robin", "Julie"], ["Charlotte", "Seb"]]



class SecretSanta():
    def __init__(
            self, 
            names: list[str],
            emails: dict[str, str],
            num_gifts: int = 1, 
            exclude_groups: list[list[str]] | None = None
        ) -> None:
        self.num_people = len(names)
        self.names = names
        self.emails = emails
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
        # print(f"{secret_lists = }")
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
    

    def stats(self, N: int):        
        counters : dict[str, dict[str, list[int]]] = dict()
        for name in self.names:
            counters[name] = dict()
            for name2 in self.names:
                counters[name][name2] = [0] * self.num_gifts
        for _ in range(N):
            self.draw()
            for name in self.names:
                for k in range(self.num_gifts):
                    counters[name][self.secret_lists[name][k]][k] += 1
        stats : dict[str, dict[str, list[float]]] = dict()
        for name in self.names:
            stats[name] = dict()
            for name2 in self.names:
                stats[name][name2] = [counters[name][name2][k]/N for k in range(self.num_gifts)]
        pprint.pprint(stats)

    def send_emails(self) -> None:
        for name in self.names:
            send_gmail(
                subject = f"Secret Santa 2023! 🎅🤫",
                body= self.create_message(name),
                recipients = [self.emails[name]],
            )

    def create_message(self, name: str) -> str:
        gifter = name
        giftees = self.secret_lists[gifter]

        res = f"\n\n\nHohoho! Salut {name} !\n\n"
        res += f"Découvre dans ce message secret qui tu vas devoir gâter pour Noël !\n\n"

        for i, giftee in enumerate(giftees):
            res += f"🎁 Cadeau {i+1} : {giftee}\n"

        res += "\n\nJoyeux Noël! Hohoho! 🎄🎄🎄\n\nSecret Santa 🎅🤫"

        print(res)
        return res



def main(
        names : list[str], 
        emails: dict[str, str], 
        num_gifts : int = 1,
        exclude_groups : list[list[str]] | None = None
    ) -> None:
    santa = SecretSanta(names=names, emails=emails, num_gifts=num_gifts, exclude_groups=exclude_groups)
    santa.draw()
    santa.send_emails()



if __name__ == '__main__':
    main(
        names = NAMES, 
        emails = EMAILS,
        num_gifts = NUM_GIFTS, 
        exclude_groups = EXCLUDE_GROUPS
    )
