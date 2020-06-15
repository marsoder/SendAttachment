import argparse
import smtplib
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.encoders import encode_base64
from email.mime.text import MIMEText


# some of the resources I used 
# https://docs.python.org/2/howto/argparse.html
# https://nitratine.net/blog/post/how-to-send-an-email-with-python/
# https://docs.python.org/2/library/email.mime.html

def get_login_information(information_file):
    with open(information_file, 'r') as f:
        username = f.readline()
        password = f.readline()
    return username, password


def get_parser():
    parser = argparse.ArgumentParser(
        description="send file as email attachment")
    parser.add_argument("--recipient", type=str, required=True)
    parser.add_argument("--attachment", type=str, required=True)
    return parser


def get_mime_message(attachment, sender, recipient):

    file = open(attachment, 'rb')
    attachment_part = MIMEApplication(file.read())
    file.close()
    file_name = os.path.basename(attachment)
    attachment_part.add_header('Content-Disposition',
                    f"attachment; filename={file_name}")
    script_name = sys.argv[0]
    defaulttext_part = MIMEText(
        f"Sent with {script_name}\nBest,\nMarcus Soederberg", "plain")

    multipart = MIMEMultipart()
    multipart["Subject"] = f"Attachment: {file_name}"
    multipart["From"] = sender
    multipart["To"] = recipient
    multipart.attach(attachment_part)
    multipart.attach(defaulttext_part)
    return multipart.as_string()


def send_message(message, sender, password, recipient):
    # assuming gmail
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, recipient, message)


if __name__ == "__main__":

    # read user email information from text file
    # fist line is username, and second line is the password, file must be 
    # inside the current working directory when using script
    sender, password = get_login_information("myemailinfo.txt")
    parser = get_parser()
    args = parser.parse_args()
    message = get_mime_message(args.attachment, sender, args.recipient)
    send_message(message, sender, password, args.recipient)
