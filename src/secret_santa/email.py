import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from secret_santa.draw import SecretSantaParticipant


class GmailServer:
    """A context manager for sending emails via Gmail."""

    def __init__(self, email: str, password: str):
        self.server = smtplib.SMTP_SSL("smtp.gmail.com")
        self.server.login(email, password)

    def __enter__(self):
        return self.server

    def __exit__(self, exc_type, exc_value, traceback):
        self.server.quit()

    def send_message(self, msg: MIMEMultipart):
        self.server.send_message(msg)


def email_participants(
    server: GmailServer,
    secret_santa_pairs: list[tuple[SecretSantaParticipant, SecretSantaParticipant]],
) -> None:
    """Send emails to the participants of the Secret Santa draw."""
    for giver, receiver in secret_santa_pairs:
        msg = MIMEMultipart()
        msg["To"] = receiver.email
        msg["Subject"] = "Secret Santa Draw"
        body = "Here are the results of the Secret Santa draw...\n\n"
        body += f"{giver.name} is buying a gift for {receiver.name}\n"
        body += "\n\nMerry Christmas!"
        body += "\n\nhttps://github.com/Ivanipani/secret-santa"
        msg.attach(MIMEText(body, "plain"))

        server.send_message(msg)
