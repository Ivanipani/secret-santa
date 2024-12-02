import argparse
import logging
import logging.config
import os
import sys

from secret_santa.draw import match_participants, read_participants_from_csv
from secret_santa.email import email_participants, GmailServer

LOGGER = logging.getLogger(__name__)


def setup_logging(log_level=logging.DEBUG):
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "detailed",
                "stream": "ext://sys.stdout",
            },
        },
        "": {
            "level": log_level,
            "handlers": ["console"],
        },
    }
    logging.config.dictConfig(LOGGING_CONFIG)


def parse_args():
    parser = argparse.ArgumentParser(description="Run the Secret Santa program")
    parser.add_argument(
        "participants_file", help="Path to the CSV file containing participants"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run the program without sending emails",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # gmail app password: https://support.google.com/mail/answer/185833?hl=en
    try:
        email = os.environ["EMAIL_ADDRESS"]
        password = os.environ["EMAIL_PASSWORD"]
    except KeyError:
        raise ValueError("EMAIL_ADDRESS and EMAIL_PASSWORD must be set")

    participants = read_participants_from_csv(args.participants_file)
    secret_santa_pairs = match_participants(participants)
    if args.dry_run:
        LOGGER.info("Dry run enabled, not sending emails")
        LOGGER.info("Secret santa pairs: %s", secret_santa_pairs)
        return

    with GmailServer(email, password) as server:
        email_participants(server, secret_santa_pairs)


if __name__ == "__main__":
    setup_logging(logging.INFO)
    try:
        main()
    except Exception:
        LOGGER.exception("An unexpected error occurred")
        sys.exit(1)
