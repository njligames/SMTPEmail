import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import time
import datetime

class SMTPEmail:
    def __init__(self):
        # Message Size — 25 MB per message, includes message header, body, and attachments
        # Message Subject Length — 255 characters
        # Message Rate (Outgoing) — 30 messages per minute, 10,000 messages per 24 hours
        # Recipients — 500 recipients per message
        # Attachment Size — 125 attachments per message, not exceeding the 25 MB message size limit
        self.subject = None
        self.htmlBody = None
        self.receiver_emails = []
        self.cc_emails = []
        self.bcc_emails = []
        self.MESSAGE_SIZE_BYTES = 25_000
        self.SUBJECT_LENGTH = 255
        self.MESSAGES_PER_MINUTE = 30
        self.MESSAGES_PER_MINUTE_BUFFER = 0.5
        self.RECIPIENTS_PER_MESSAGE = 500
        self.MESSAGES_IN_24HOURS = 10_000

    def __validate(self):
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
        if len(s) > self.SUBJECT_LENGTH:
            raise Exception(f"Message Subject Length — {self.SUBJECT_LENGTH} characters")

    def __validateSize(self, s):
        if len(s.encode('utf-8')) > self.MESSAGE_SIZE_BYTES:
            raise Exception(f"Message Size — {self.MESSAGE_SIZE_BYTES} bytes per message, includes message header, body, and attachments")

    def __validateEmails(self, lst):
        n = len(self.receiver_emails) + len(self.cc_emails) + len(self.bcc_emails) + len(lst)

        if n > self.RECIPIENTS_PER_MESSAGE:
            raise Exception(f"Recipients — {self.RECIPIENTS_PER_MESSAGE} recipients per message")

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

    # Assuming already validated
    def __getDivisor(self):
        divisor = 0

        if len(self.receiver_emails) != 0:
            divisor += 1
        if len(self.cc_emails) != 0:
            divisor += 1
        if len(self.bcc_emails) != 0:
            divisor += 1

        return divisor 

    def __getNextReceiverEmails(self, batch_size):
        if batch_size > self.RECIPIENTS_PER_MESSAGE:
            batch_size = self.RECIPIENTS_PER_MESSAGE

        emails = []
        if len(self.receiver_emails) > 0:
            for i in range(batch_size):
                eml = self.receiver_emails.pop()
                try:
                    self.__validateEmailAddress(eml)
                    emails.append(eml)
                except Exception as e:
                    print(e)

        return emails

    def __getNextCCEmails(self, batch_size):
        if batch_size > self.RECIPIENTS_PER_MESSAGE:
            batch_size = self.RECIPIENTS_PER_MESSAGE

        emails = []
        if len(self.cc_emails) > 0:
            for i in range(batch_size):
                eml = self.cc_emails.pop()
                try:
                    self.__validateEmailAddress(eml)
                    emails.append(eml)
                except Exception as e:
                    print(e)

        return emails

    def __getNextBCCEmails(self, batch_size):
        if batch_size > self.RECIPIENTS_PER_MESSAGE:
            batch_size = self.RECIPIENTS_PER_MESSAGE

        emails = []
        if len(self.bcc_emails) > 0:
            for i in range(batch_size):
                eml = self.bcc_emails.pop()
                try:
                    self.__validateEmailAddress(eml)
                    emails.append(eml)
                except Exception as e:
                    print(e)

        return emails

    def send(self, sender_email, password, smtp_address = "smtp-mail.outlook.com", smtp_port = 587):
        SLEEP_TIME = (60 / self.MESSAGES_PER_MINUTE) + self.MESSAGES_PER_MINUTE_BUFFER
        BATCH_SIZE = 1

        try:
            self.__validate()
            self.__validateEmailAddress(sender_email)

            receiver_emails = self.__getNextReceiverEmails(BATCH_SIZE)
            cc_emails = self.__getNextCCEmails(BATCH_SIZE)
            bcc_emails = self.__getNextBCCEmails(BATCH_SIZE)

            # Create SMTP session for sending the mail
            server = smtplib.SMTP(smtp_address, smtp_port)  # Use Gmail SMTP server
            server.starttls()  # Enable security

            # Login with mail_id and password
            server.login(sender_email, password)

            # TODO: get the start time
            message_sent = 0
            now = datetime.datetime.now()
            tomorrow = now + datetime.timedelta(hours=24)
            delta = tomorrow - now

            while len(receiver_emails) + len(cc_emails) + len(bcc_emails) > 0:

                now = datetime.datetime.now()
                delta = tomorrow - now

                if delta.total_seconds() <= 0:
                    message_sent = 0
                    now = datetime.datetime.now()
                    tomorrow = now + datetime.timedelta(hours=24)

                if message_sent < self.MESSAGES_IN_24HOURS:
                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = ', '.join(receiver_emails)
                    msg['CC'] = ', '.join(cc_emails)
                    msg['BCC'] = ', '.join(bcc_emails)
                    msg['Subject'] = self.subject
                    msg.attach(MIMEText(self.htmlBody, 'html'))

                    # Convert the Multipart msg into a string
                    text = msg.as_string()

                    # Send the mail to all recipients (including CC and BCC)
                    all_recipients = []
                    if None != receiver_emails:
                        all_recipients += receiver_emails
                    if None != cc_emails:
                        all_recipients += cc_emails
                    if None != bcc_emails:
                        all_recipients += bcc_emails
                    server.sendmail(sender_email, all_recipients, text)
                    messages_sent = message_sent + 1

                    numberOfRecipients = len(all_recipients)
                    print(f"Mail sent successfully to {numberOfRecipients} recipients!")

                    receiver_emails = self.__getNextReceiverEmails(BATCH_SIZE)
                    cc_emails = self.__getNextCCEmails(BATCH_SIZE)
                    bcc_emails = self.__getNextBCCEmails(BATCH_SIZE)

                    time.sleep(SLEEP_TIME)

            # Close the connection
            server.quit()
        except smtplib.SMTPAuthenticationError:
            print('Invalid email or password. Please check your credentials.')
        except smtplib.SMTPException as e:
            print('An error occurred while sending the email: ', str(e))
        except Exception as e:
            print('An unexpected error occurred: ', str(e))
