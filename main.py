# Import necessary libraries
import os
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

password = os.environ["PASSWORD"]
sender_email = os.environ["EMAIL"]
smtp_address = os.environ["SMTP"]

content_file = os.environ['HTMLFILE']
subject_file = os.environ['SUBJECTFILE']
to_file = os.environ['TOFILE']
cc_file = os.environ['CCFILE']
bcc_file = os.environ['BCCFILE']

def setSubject(msg, filename):
    subject = "Subject"
    with open(filename, 'r') as reader:
        subject = reader.read()
    msg['Subject'] = subject

def setContent(msg, filename):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Join Our AI Model Training Community!</title>
    </head>
    <body>
    </body>
    </html>
    """
    with open(filename, 'r') as reader:
        html_content = reader.read()

    # Add HTML content to email
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)

def getEmails(filename):
    emails = None
    with open(filename, mode ='r')as file:
        csvFile = csv.reader(file)
        emails = []
        for lines in csvFile:
            emails.append(lines["email"])
    return emails

def setReceiverEmails(msg, filename):
    emails = getEmails(filename)
    if emails:
        msg['To'] = ', '.join(emails)
    return emails

def setCCEmailse(msg, filename):
    emails = getEmails(filename)
    if emails:
        msg['CC'] = ', '.join(emails)
    return emails

def setBCCEmails(msg, filename):
    emails = getEmails(filename)
    if emails:
        msg['BCC'] = ', '.join(emails)
    return emails

msg = MIMEMultipart()
msg['From'] = sender_email
receiver_emails = setReceiverEmails(msg, to_file)
cc_emails = setCCEmails(msg, cc_file)
bcc_emails = setBCCEmails(msg, bcc_file)
setSubject(msg, subject_file)
setContent(msg, content_file)
try:
    # Create SMTP session for sending the mail
    server = smtplib.SMTP(smtp_address, 587)  # Use Gmail SMTP server
    server.starttls()  # Enable security

    # Login with mail_id and password
    server.login(sender_email, password)

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

    # Close the connection
    server.quit()

    print('Mail sent successfully!')
except smtplib.SMTPAuthenticationError:
    print('Invalid email or password. Please check your credentials.')
except smtplib.SMTPException as e:
    print('An error occurred while sending the email: ', str(e))
except Exception as e:
    print('An unexpected error occurred: ', str(e))


#           # Define sender and receiver email addresses
#           # sender_email = 'james@njligames.com'
#           receiver_email = 'jamesfolk1@gmail.com'
#
#           # Define email subject and body
#           subject = 'Feedback Mail'
#           # body = 'This is a feedback mail sent from Python script.'
#
#           # Create message object instance
#           msg = MIMEMultipart()
#
#           # Setup the parameters of the message
#           msg['From'] = sender_email
#           msg['To'] = receiver_email
#           msg['Subject'] = subject
#
#           # Add body to the message
#           # msg.attach(MIMEText(body, 'plain'))
#
#
#
#           html_content = """
#           <!DOCTYPE html>
#           <html lang="en">
#           <head>
#               <meta charset="UTF-8">
#               <meta name="viewport" content="width=device-width, initial-scale=1.0">
#               <title>Join Our AI Model Training Community!</title>
#           </head>
#           <body>
#           </body>
#           </html>
#           """
#           with open(html_file, 'r') as reader:
#               html_content = reader.read()
#
#           # Add HTML content to email
#           html_part = MIMEText(html_content, 'html')
#           msg.attach(html_part)
#
#
#           # Create SMTP session for sending the mail
#           server = smtplib.SMTP(smtp_address, 587)  # Use Gmail SMTP server
#           server.starttls()  # Enable security
#
#           # Login with mail_id and password
#           server.login(sender_email, password)
#
#           # Convert the Multipart msg into a string
#           text = msg.as_string()
#
#           # Send the mail
#           server.sendmail(sender_email, receiver_email, text)
#
#           # Close the connection
#           server.quit()
#
#           print('Mail sent successfully!')
