import random
import csv
from dataclasses import dataclass
import logging
import yaml

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


def validate_yaml_structure(data: dict) -> None:
    """Validate the structure of the YAML file.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If the YAML structure is invalid
    """
    if not data:
        raise ValueError("YAML file is empty")

    if not isinstance(data, dict):
        raise ValueError("YAML file must contain a dictionary at the top level")

    if "participants" not in data:
        raise ValueError("YAML file must contain a 'participants' key")

    participants = data["participants"]

    if not isinstance(participants, list):
        raise ValueError("'participants' must be a list")

    if len(participants) == 0:
        raise ValueError("'participants' list cannot be empty")

    for idx, participant in enumerate(participants):
        if not isinstance(participant, dict):
            raise ValueError(
                f"Participant at index {idx} must be a dictionary, got {type(participant).__name__}"
            )

        if "name" not in participant:
            raise ValueError(f"Participant at index {idx} is missing 'name' field")

        if "email" not in participant:
            raise ValueError(f"Participant at index {idx} is missing 'email' field")

        name = participant["name"]
        email = participant["email"]

        if not isinstance(name, str):
            raise ValueError(
                f"Participant at index {idx}: 'name' must be a string, got {type(name).__name__}"
            )

        if not isinstance(email, str):
            raise ValueError(
                f"Participant at index {idx}: 'email' must be a string, got {type(email).__name__}"
            )

        if not name.strip():
            raise ValueError(f"Participant at index {idx}: 'name' cannot be empty")

        if not email.strip():
            raise ValueError(f"Participant at index {idx}: 'email' cannot be empty")

        # Basic email validation
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError(
                f"Participant at index {idx}: '{email}' is not a valid email address"
            )


def read_participants_from_yaml(file_path: str) -> set[SecretSantaParticipant]:
    """Read the participants from a YAML file.

    Expected format:
    participants:
      - name: Alice
        email: alice@example.com
      - name: Bob
        email: bob@example.com

    Args:
        file_path: Path to the YAML file

    Returns:
        Set of SecretSantaParticipant objects

    Raises:
        ValueError: If the YAML structure is invalid
        FileNotFoundError: If the file doesn't exist
    """
    with open(file_path, mode="r") as yamlfile:
        data = yaml.safe_load(yamlfile)
        validate_yaml_structure(data)

        participants = set()
        for participant_data in data["participants"]:
            name = participant_data["name"].strip()
            email = participant_data["email"].strip()
            participants.add(SecretSantaParticipant(name=name, email=email))

    return participants
