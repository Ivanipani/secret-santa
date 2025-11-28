# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Secret Santa draw application that randomly assigns gift-giving pairs and emails all participants with their assignments. It's a simple Python CLI tool managed with Rye.

## Development Setup

This project uses Rye for dependency management:
- Install dependencies: `rye sync`
- The project uses Python 3.12+ (as specified in pyproject.toml)

## Running the Application

The application requires two environment variables for Gmail SMTP authentication:
- `EMAIL_ADDRESS`: The Gmail address to send emails from
- `EMAIL_PASSWORD`: A Gmail App Password (not regular password - see https://support.google.com/mail/answer/185833?hl=en)

Run the program:
```bash
EMAIL_ADDRESS=<email> EMAIL_PASSWORD=<password> python -m secret_santa participants.csv
```

Or with the installed script:
```bash
EMAIL_ADDRESS=<email> EMAIL_PASSWORD=<password> secret_santa participants.csv
```

Dry run (doesn't send emails, just logs the pairs):
```bash
EMAIL_ADDRESS=<email> EMAIL_PASSWORD=<password> python -m secret_santa participants.csv --dry-run
```

## Testing

Run all tests:
```bash
pytest
```

Run a specific test file:
```bash
pytest tests/unit/test_draw.py
```

Run a specific test function:
```bash
pytest tests/unit/test_draw.py::test_match_participants
```

The project includes pytest-repeat for running tests multiple times (useful for testing randomization logic).

## Code Architecture

### Core Components

1. **draw.py**: Contains the core Secret Santa matching logic
   - `SecretSantaParticipant`: Dataclass representing a participant (name + email)
   - `match_participants()`: Shuffles participants and creates a circular gift-giving chain (each person gives to the next, last person gives to first)
   - `read_participants_from_csv()`: Parses CSV file with format: `Name, email@example.com`

2. **email.py**: Handles email sending via Gmail SMTP
   - `GmailServer`: Context manager for SMTP connection
   - `email_participants()`: Sends personalized emails to each giver with their receiver's name
   - Email subject and body are currently hardcoded in Spanish for the Perdomo/Silva/Aponte family

3. **__main__.py**: Entry point with CLI argument parsing and orchestration
   - Sets up logging
   - Reads environment variables for email credentials
   - Coordinates reading CSV, matching participants, and sending emails
   - Supports `--dry-run` flag

### Participant CSV Format

The CSV file should contain one participant per line:
```
Name, email@example.com
Another Person, another@example.com
```

### Email Customization

The email subject and body are currently hardcoded in `email.py:32-36` for a specific family. When modifying for general use, these should be made configurable.

### Matching Algorithm

The matching algorithm in `match_participants()` creates a simple circular chain by:
1. Shuffling the participants list
2. Each participant at index `i` gives to participant at index `(i+1) % len(participants)`

This ensures everyone gives to exactly one person and receives from exactly one person, with no self-assignments.
