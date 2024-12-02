import argparse
import logging
import logging.config
import os
import smtplib
import sys

from secret_santa.draw import match_participants, read_participants_from_csv
from secret_santa.email import email_participants

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
    if args.dry_run:
        print("here")
        LOGGER.info("Dry run enabled, not sending emails")
        LOGGER.info(participants)
        return

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Secure the connection
        server.login(email, password)
        secret_santa_pairs = match_participants(participants)
        email_participants(server, email, secret_santa_pairs)


if __name__ == "__main__":
    # Call this function at the start of your script to configure logging
    # setup_logging(logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logging.debug("Logging is configured and working.")  # Test log message
    # print("Logging is configured and working.")  # Test log message
    try:
        main()
    except Exception as e:
        LOGGER.error(f"Error: {e}")
        sys.exit(1)
