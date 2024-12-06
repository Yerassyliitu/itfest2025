from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from settings.mail_config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_PORT, MAIL_SERVER


class EmailUtils:
    """
    Utility class for sending email messages.
    """

    @classmethod
    def send_code_to_email(cls, send_to: str, random_password: str) -> bool:
        """
        Sends an email with a random password to the specified recipient.

        :param send_to: Recipient's email address.
        :param random_password: Password to include in the email.
        :return: True if the email was sent successfully, False otherwise.
        """
        try:
            text = f"{random_password}"
            msg = MIMEText(text, "html")
            msg["Subject"] = "Ваш пароль"
            msg["From"] = f"BED <{MAIL_USERNAME}>"
            msg["To"] = send_to

            # Connect to the email server
            server = SMTP_SSL(MAIL_SERVER, MAIL_PORT)
            server.login(MAIL_USERNAME, MAIL_PASSWORD)

            # Send the email
            server.send_message(msg)
            server.quit()
            return True

        except Exception as e:
            print(f"Error sending email: {e}")
            raise e
