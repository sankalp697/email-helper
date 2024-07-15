import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
from email.parser import BytesParser

def send_email(sender_email, receiver_email, subject, message, smtp_server, smtp_port, username, password):
    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Add body to the email
    msg.attach(MIMEText(message, "plain"))

    # Create SMTP session
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
        print("Email sent successfully")

def read_unread_emails(username, password, imap_server, imap_port):
    # Connect to the IMAP server
    with imaplib.IMAP4_SSL(imap_server, imap_port) as server:
        # Login to the email account
        server.login(username, password)

        # Select the inbox folder
        server.select("INBOX")

        # Search for unread emails
        _, message_numbers = server.search(None, "UNSEEN")

        # Iterate over the message numbers
        for num in message_numbers[0].split():
            # Fetch the email data
            _, message_data = server.fetch(num, "(RFC822)")

            # Parse the email data
            email_message = BytesParser().parsebytes(message_data[0][1])

            # Print the email details
            print("From:", email_message["From"])
            print("Subject:", email_message["Subject"])
            print("Date:", email_message["Date"])
            print("")

        # Logout from the email account
        server.logout()

def get_unread_email_count(imap_server, imap_port, username, password):
    """
    Connects to the specified IMAP server and returns the count of unread emails.

    Parameters:
    imap_server (str): The IMAP server address.
    imap_port (int): The port number for the IMAP server.
    username (str): The username for the email account.
    password (str): The password for the email account.

    Returns:
    int: The count of unread emails.
    """
    try:
        with imaplib.IMAP4_SSL(imap_server, imap_port) as server:
            # Login to the email account
            server.login(username, password)

            # Select the inbox folder
            server.select("INBOX")

            # Search for unread emails
            _, message_numbers = server.search(None, "UNSEEN")

            # Count the unread emails
            unread_count = len(message_numbers[0].split())

            # Logout from the email account
            server.logout()

            return unread_count
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0

def test_imap_connection(imap_server, imap_port, username, password):
    """
    Tests the connection to the specified IMAP server with the provided credentials.

    Parameters:
    imap_server (str): The IMAP server address.
    imap_port (int): The port number for the IMAP server.
    username (str): The username for the email account.
    password (str): The password for the email account.

    Returns:
    bool: True if the connection is successful, False otherwise.
    """
    try:
        with imaplib.IMAP4_SSL(imap_server, imap_port) as server:
            # Attempt to login to the email account
            server.login(username, password)
            print("Connection successful.")
            return True
    except imaplib.IMAP4.error as e:
        print(f"IMAP4 error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return False
