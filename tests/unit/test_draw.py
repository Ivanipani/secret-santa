import pytest
import tempfile
import os

from secret_santa.draw import (
    SecretSantaParticipant,
    match_participants,
    read_participants_from_yaml,
    validate_yaml_structure,
)


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


def test_read_participants_from_yaml():
    """Test that YAML parser correctly reads participants."""
    yaml_content = """participants:
  - name: Alice
    email: alice@example.com
  - name: Bob
    email: bob@example.com
  - name: Charlie
    email: charlie@example.com
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(yaml_content)
        temp_file_path = f.name

    try:
        participants = read_participants_from_yaml(temp_file_path)

        expected_participants = {
            SecretSantaParticipant(name="Alice", email="alice@example.com"),
            SecretSantaParticipant(name="Bob", email="bob@example.com"),
            SecretSantaParticipant(name="Charlie", email="charlie@example.com"),
        }

        assert participants == expected_participants
        assert len(participants) == 3
    finally:
        os.unlink(temp_file_path)


@pytest.mark.parametrize(
    "yaml_data,expected_error_match",
    [
        # Empty file
        (None, "YAML file is empty"),
        # Top level not a dictionary
        (
            ["list", "of", "items"],
            "YAML file must contain a dictionary at the top level",
        ),
        # Missing 'participants' key
        ({"other_key": "value"}, "YAML file must contain a 'participants' key"),
        # 'participants' not a list
        ({"participants": "not a list"}, "'participants' must be a list"),
        # Empty participants list
        ({"participants": []}, "'participants' list cannot be empty"),
        # Participant not a dictionary
        (
            {"participants": ["not a dict"]},
            "Participant at index 0 must be a dictionary, got str",
        ),
        # Missing 'name' field
        (
            {"participants": [{"email": "test@example.com"}]},
            "Participant at index 0 is missing 'name' field",
        ),
        # Missing 'email' field
        (
            {"participants": [{"name": "Alice"}]},
            "Participant at index 0 is missing 'email' field",
        ),
        # 'name' not a string
        (
            {"participants": [{"name": 123, "email": "test@example.com"}]},
            "Participant at index 0: 'name' must be a string, got int",
        ),
        # 'email' not a string
        (
            {"participants": [{"name": "Alice", "email": 123}]},
            "Participant at index 0: 'email' must be a string, got int",
        ),
        # Empty 'name'
        (
            {"participants": [{"name": "  ", "email": "test@example.com"}]},
            "Participant at index 0: 'name' cannot be empty",
        ),
        # Empty 'email'
        (
            {"participants": [{"name": "Alice", "email": "  "}]},
            "Participant at index 0: 'email' cannot be empty",
        ),
        # Invalid email - no @ symbol
        (
            {"participants": [{"name": "Alice", "email": "notanemail"}]},
            "Participant at index 0: 'notanemail' is not a valid email address",
        ),
        # Invalid email - no dot after @
        (
            {"participants": [{"name": "Alice", "email": "test@example"}]},
            "Participant at index 0: 'test@example' is not a valid email address",
        ),
    ],
)
def test_validate_yaml_structure_invalid_cases(yaml_data, expected_error_match):
    """Test validation with all invalid YAML cases."""
    with pytest.raises(ValueError, match=expected_error_match):
        validate_yaml_structure(yaml_data)
