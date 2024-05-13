import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re

class SMTPEmail:
    def __init__(self):
        self.subject = None
        self.htmlBody = None
        self.receiver_emails = []
        self.cc_emails = []
        self.bcc_emails = []

    def __validate(self):
        # Message Size — 25 MB per message, includes message header, body, and attachments
        # Message Subject Length — 255 characters
        # Message Rate (Outgoing) — 30 messages per minute, 10,000 messages per 24 hours
        # Recipients — 500 recipients per message
        # Attachment Size — 125 attachments per message, not exceeding the 25 MB message size limit
        if not self.subject:
            raise Exception("No subject")
        if not self.htmlBody:
            raise Exception("No htmlBody")
        if 0 == len(self.receiver_emails) + len(self.cc_emails) + len(self.bcc_emails):
            raise Exception("No recipients")

    def __validateEmailAddress(self, email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.fullmatch(regex, email):
            raise Exception("Invalid Email - " + str(email))

    def __validateSubject(self, s):
        if len(s) > 255:
            raise Exception("Message Subject Length — 255 characters")

    def __validateSize(self, s):
        if len(s.encode('utf-8')) > 25_000:
            raise Exception("Message Size — 25 MB per message, includes message header, body, and attachments")

    def __validateEmails(self, lst):
        n = len(self.receiver_emails) + len(self.cc_emails) + len(self.bcc_emails) + len(lst)

        if n > 500:
            raise Exception("Recipients — 500 recipients per message")

    def setSubject(self, s):
        try:
            self.__validateSubject(s)
            self.subject = s
        except Exception as e:
            print(e)

    def setHTMLBody(self, s):
        try:
            self.__validateSize(s)
            self.htmlBody = s
        except Exception as e:
            print(e)

    def setReceiverEmails(self, lst):
        try:
            self.__validateEmails(lst)
            self.receiver_emails = lst
        except Exception as e:
            print(e)

    def setCCEmails(self, lst):
        try:
            self.__validateEmails(lst)
            self.cc_emails = lst
        except Exception as e:
            print(e)

    def setBCCEmails(self, lst):
        try:
            self.__validateEmails(lst)
            self.bcc_emails = lst
        except Exception as e:
            print(e)

    def send(self, sender_email, password, smtp_address = "smtp-mail.outlook.com", smtp_port = 587):
        try:
            self.__validate()
            self.__validateEmailAddress(sender_email)

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = ', '.join(self.receiver_emails)
            msg['CC'] = ', '.join(self.cc_emails)
            msg['BCC'] = ', '.join(self.bcc_emails)
            msg['Subject'] = self.subject
            msg.attach(MIMEText(self.htmlBody, 'html'))

            try:
                # Create SMTP session for sending the mail
                server = smtplib.SMTP(smtp_address, smtp_port)  # Use Gmail SMTP server
                server.starttls()  # Enable security

                # Login with mail_id and password
                server.login(sender_email, password)

                # Convert the Multipart msg into a string
                text = msg.as_string()

                # Send the mail to all recipients (including CC and BCC)
                all_recipients = []
                if None != self.receiver_emails:
                    all_recipients += self.receiver_emails
                if None != self.cc_emails:
                    all_recipients += self.cc_emails
                if None != self.bcc_emails:
                    all_recipients += self.bcc_emails
                server.sendmail(sender_email, all_recipients, text)

                # Close the connection
                server.quit()

                print('Mail sent successfully!')
            except smtplib.SMTPAuthenticationError:
                print('Invalid email or password. Please check your credentials.')
            except smtplib.SMTPException as e:
                print('An error occurred while sending the email: ', str(e))
            except Exception as e:
                print('An unexpected error occurred: ', str(e))
        except Exception as e:
            print(e)
