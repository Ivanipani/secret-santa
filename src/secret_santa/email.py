import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from secret_santa.draw import SecretSantaParticipant


def email_participants(
    server: smtplib.SMTP,
    from_email: str,
    secret_santa_pairs: list[tuple[SecretSantaParticipant, SecretSantaParticipant]],
) -> None:
    for giver, receiver in secret_santa_pairs:
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = receiver.email
        msg["Subject"] = "Secret Santa Draw"
        body = "Here are the results of the Secret Santa draw...\n\n"
        body += f"{giver.name} is buying a gift for {receiver.name}\n"
        body += "\n\nMerry Christmas!"
        body += "\n\nhttps://github.com/Ivanipani/secret-santa"
        msg.attach(MIMEText(body, "plain"))

        server.send_message(msg)
