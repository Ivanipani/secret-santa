import random
import csv
from dataclasses import dataclass
import logging

LOGGER = logging.getLogger(__name__)


@dataclass
class SecretSantaParticipant:
    """A participant in the Secret Santa draw."""

    email: str
    name: str

    def __hash__(self) -> int:
        return hash(self.name + self.email)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SecretSantaParticipant):
            return self.email == other.email and self.name == other.name
        return False


def match_participants(
    participants: set[SecretSantaParticipant],
) -> list[tuple[[SecretSantaParticipant, SecretSantaParticipant]]]:
    """Match the participants of the Secret Santa draw."""
    output = []
    randomized_participants = list(participants)
    random.shuffle(randomized_participants)
    for giver_idx in range(len(randomized_participants)):
        receiver_idx = (giver_idx + 1) % len(randomized_participants)
        output.append(
            (
                randomized_participants[giver_idx],
                randomized_participants[receiver_idx],
            )
        )
    return output


def read_participants_from_csv(file_path: str) -> set[SecretSantaParticipant]:
    """Read the participants from a CSV file."""
    participants = set()
    with open(file_path, mode="r", newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row) != 2:
                continue  # Skip rows that don't have exactly two columns
            name, email = row
            participants.add(SecretSantaParticipant(name=name, email=email))
    return participants
