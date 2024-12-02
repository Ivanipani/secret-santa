import pytest
from secret_santa.draw import match_participants, SecretSantaParticipant


@pytest.mark.parametrize(
    "participants",
    [
        {
            SecretSantaParticipant(name="Alice", email="alice@example.com"),
            SecretSantaParticipant(name="Bob", email="bob@example.com"),
            SecretSantaParticipant(name="Charlie", email="charlie@example.com"),
            SecretSantaParticipant(name="David", email="david@example.com"),
            SecretSantaParticipant(name="Eve", email="eve@example.com"),
            SecretSantaParticipant(name="Frank", email="frank@example.com"),
            SecretSantaParticipant(name="Grace", email="grace@example.com"),
            SecretSantaParticipant(name="Hank", email="hank@example.com"),
        },
        {
            SecretSantaParticipant(name="Alice", email="alice@example.com"),
            SecretSantaParticipant(name="Bob", email="bob@example.com"),
            SecretSantaParticipant(name="Charlie", email="charlie@example.com"),
        },
    ],
)
def test_match_participants(participants):
    result = match_participants(participants)
    assert {giver for giver, _ in result} == participants
    assert {receiver for _, receiver in result} == participants
