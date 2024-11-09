#!/usr/bin/env python

"""
Use this Python module to generate a random draw for Secret Santa.

Usage
1. In this file, edit NAMES, EMAILS, NUM_GIFTS, and optionally EXCLUDE_GROUPS (or comment it out).
2. Run the script: from the parent folder, run:
```
python3 -m secret_santa.main [--send]
```

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
    """
    Class representing the Secret Santa bot.
    """
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

        self.secret_lists : dict[str, list[str]] = dict()


    def draw(self):
        """
        Draw the secret lists.
        """
        logger.info("Drawing odds...")
        exclusions = self._get_exclusions()
        perms : list[Permutation] = random_derangements(n=self.num_people, d=self.num_gifts, exclusions=exclusions)
        for i, name in enumerate(self.names):
            self.secret_lists[name] = [self.names[perm(i)] for perm in perms]


    def _get_exclusions(self) -> list[list[int]] | None:
        if not self.exclude_groups:
            return None
        exclusions : list[list[int]] = [[]]*self.num_people
        for group in self.exclude_groups:
            group_indices = [self.indices[name] for name in group]
            for name in group:
                exclusions[self.indices[name]] = group_indices.copy()
        return exclusions.copy()


    def stats(self, num_draws: int):
        """
        Compute statistics on the draws.
        """
        counters : dict[str, dict[str, list[int]]] = dict()
        for name in self.names:
            counters[name] = dict()
            for name2 in self.names:
                counters[name][name2] = [0] * self.num_gifts
        for _ in range(num_draws):
            self.draw()
            for name in self.names:
                for k in range(self.num_gifts):
                    counters[name][self.secret_lists[name][k]][k] += 1
        stats : dict[str, dict[str, list[float]]] = dict()
        for name in self.names:
            stats[name] = dict()
            for name2 in self.names:
                stats[name][name2] = [counters[name][name2][k]/num_draws for k in range(self.num_gifts)]
        pprint.pprint(stats)


    def send_emails(self, dry_run: bool = False) -> None:
        """
        Send the emails to the participants.
        """
        logger.info("Sending emails...")
        for name in self.names:
            subject = "Père Noël Secret 2024 ! 🎅🤫"
            message = self.create_message(name)
            if dry_run:
                logger.info(f"This is a dry run. Here is the email that would be sent to {name}:\n-----")
                print(f"{subject}")
                print("-----")
                print(f"{message}")
                print("-----\n")
            else:
                send_gmail(
                    subject = subject,
                    body = message,
                    recipients = [self.emails[name]],
                )

    def create_message(self, name: str) -> str:
        """
        Create the email message for a given name.
        """
        gifter = name
        giftees = self.secret_lists[gifter]

        res = f"Hohoho ! Salut {name} !\n\n"
        res += "Je suis le bot 🤖 du Père Noël, hohoho. Ceci est un message secret ! 🤫\n\n"
        res += "Voici le résultat du tirage au sort pour toi :\n\n"

        for i, giftee in enumerate(giftees):
            adjective = "(\"gros\") " if i == 0 else  "(\"petit\")"
            res += f"🎁 Cadeau {i+1} {adjective} : {giftee}\n"

        res += "\n\nJoyeux Noël ! Hohohohoho. 🎄🎄🎄"
        res += "\nPère Noël Secret 🎅"
        res += "\n\n\nPS: Ne réponds pas à ce message, car Brice le verrait !"
        return res



def main(
        names : list[str],
        emails: dict[str, str],
        num_gifts : int = 1,
        exclude_groups : list[list[str]] | None = None,
        send: bool = False,
    ) -> None:
    """
    Main function to run the Secret Santa bot.
    """
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

