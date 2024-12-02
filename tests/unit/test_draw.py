import pytest
from secret_santa.draw import match_participants, SecretSantaParticipant


def test_match_participants():
    participants = {
        SecretSantaParticipant(name="Alice", email="alice@example.com"),
        SecretSantaParticipant(name="Bob", email="bob@example.com"),
        SecretSantaParticipant(name="Charlie", email="charlie@example.com"),
        SecretSantaParticipant(name="David", email="david@example.com"),
        SecretSantaParticipant(name="Eve", email="eve@example.com"),
        SecretSantaParticipant(name="Frank", email="frank@example.com"),
        SecretSantaParticipant(name="Grace", email="grace@example.com"),
        SecretSantaParticipant(name="Hank", email="hank@example.com"),
    }
    result = match_participants(participants)
    assert {giver for giver, _ in result} == participants
    assert {receiver for _, receiver in result} == participants


def test_match_participants_raises_error_if_odd_number_of_participants():
    participants = {
        SecretSantaParticipant(name="Alice", email="alice@example.com"),
        SecretSantaParticipant(name="Bob", email="bob@example.com"),
        SecretSantaParticipant(name="Charlie", email="charlie@example.com"),
    }
    with pytest.raises(ValueError):
        match_participants(participants)
