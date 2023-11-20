#!/usr/bin/env python

"""
Use this Python module to generate a random draw for Secret Santa.

Usage
1. In this file, edit NAMES, EMAILS, NUM_GIFTS, and optionally EXCLUDE_GROUPS (or comment it out).
2. Run the script: from the parent folder, execute `python3 -m main [--send]`.

If you do not use the `--send` flag, it will be a dry run and no emails will be sent.
"""


import argparse
import logging
import pprint

from .derangements import Permutation, random_derangements
from .mail import send_gmail



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


NAMES = ["Nono", "Marie-Laure", "Brice", "Benja", "Robin", "Julie", "Charlotte", "Seb"]
EMAILS = {
    "Nono": "loustau.denis@gmail.com",
    "Marie-Laure": "marielaure.loustau@gmail.com",
    "Brice": "brice.loustau@gmail.com",
    "Benja": "bdv2113@gmail.com",
    "Robin": "robin.loustau@gmail.com",
    "Julie": "priault.julie@gmail.com",
    "Charlotte": "charlotte.loustau@gmail.com",
    "Seb": "sebastien.arches@gmail.com",
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
        logger.info("Drawing odds...")
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


    def send_emails(self, dry_run: bool = False) -> None:
        logger.info("Sending emails...")
        for name in self.names:
            subject = f"Père Noël Secret 2023 ! 🎅🤫"
            message = self.create_message(name)
            if dry_run:
                logger.info(f"This is a dry run. Here is the email that would be sent to {name}:\n-----")
                print(f"{subject}")
                print(f"-----")
                print(f"{message}")
                print(f"-----\n")
            else:
                send_gmail(
                    subject = subject,
                    body = message,
                    recipients = [self.emails[name]],
                )

    def create_message(self, name: str) -> str:
        gifter = name
        giftees = self.secret_lists[gifter]

        res = f"Hohoho! Salut {name} !\n\n"
        res += f"Je suis le Père Noël Secret programmé par Brice et je viens de faire le tirage au sort.\n\n"
        res += f"Découvre qui tu vas devoir gâter pour Noël !\n\n"

        for i, giftee in enumerate(giftees):
            res += f"🎁 Cadeau {i+1} : {giftee}\n"

        res += "\n\nJoyeux Noël ! Hohoho! 🎄🎄🎄"
        # res += "\n\nPS: Ne réponds pas à ce message, car Brice ne l'a pas vu !" 
        return res



def main(
        names : list[str], 
        emails: dict[str, str], 
        num_gifts : int = 1,
        exclude_groups : list[list[str]] | None = None,
        send: bool = False,
    ) -> None:
    logger.info("Starting Secret Santa...")
    santa = SecretSanta(names=names, emails=emails, num_gifts=num_gifts, exclude_groups=exclude_groups)
    santa.draw()
    santa.send_emails(dry_run=not send)
    logger.info("Done!")




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--send", action="store_true")
    args = parser.parse_args()

    main(
        names = NAMES, 
        emails = EMAILS,
        num_gifts = NUM_GIFTS, 
        exclude_groups = EXCLUDE_GROUPS,
        send = args.send,
    )
