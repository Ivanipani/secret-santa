import random
import csv
from dataclasses import dataclass
import logging

LOGGER = logging.getLogger(__name__)


@dataclass
class SecretSantaParticipant:
    email: str
    name: str

    def __hash__(self) -> int:
        return hash(self.name) + hash(self.email)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SecretSantaParticipant):
            return self.email == other.email and self.name == other.name
        return False


def match_participants(
    participants: set[SecretSantaParticipant],
) -> list[tuple[[SecretSantaParticipant, SecretSantaParticipant]]]:
    def _match_participants(p: set[SecretSantaParticipant]):
        if len(p) % 2 != 0:
            raise ValueError("Number of participants must be even")

        output = []
        need_gifts = p.copy()

        for giver in p:
            receiver = random.choice(tuple(need_gifts.difference({giver})))
            need_gifts.remove(receiver)
            output.append((giver, receiver))

        return output

    # can't be wrong 99 times in a row!
    for _ in range(100):
        try:
            return _match_participants(participants)
        except IndexError:
            continue
    raise ValueError("Failed to match participants after 100 attempts")


def read_participants_from_csv(file_path: str) -> set[SecretSantaParticipant]:
    participants = set()
    with open(file_path, mode="r", newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row) != 2:
                continue  # Skip rows that don't have exactly two columns
            name, email = row
            participants.add(SecretSantaParticipant(name=name, email=email))
    return participants
