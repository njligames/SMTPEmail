# Import necessary libraries
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

password = os.environ["PASSWORD"]
sender_email = os.environ["EMAIL"]
smtp_address = os.environ["SMTP"]

# Define sender email address
# sender_email = 'your-email@gmail.com'

# Define receiver email addresses (multiple)
receiver_emails = ['user1-email@example.com', 'user2-email@example.com', 'user3-email@example.com']

# Define CC email addresses (optional)
cc_emails = ['cc-user1-email@example.com', 'cc-user2-email@example.com']

# Define BCC email addresses (optional)
bcc_emails = ['bcc-user1-email@example.com', 'bcc-user2-email@example.com']

# Define email subject and body
subject = 'Feedback Mail'
body = 'This is a feedback mail sent from Python script.'

# Create message object instance
msg = MIMEMultipart()

# Setup the parameters of the message
msg['From'] = sender_email
msg['To'] = ', '.join(receiver_emails)  # Join multiple receiver emails with comma
msg['Subject'] = subject

# Add CC and BCC recipients if present
if cc_emails:
    msg['CC'] = ', '.join(cc_emails)
if bcc_emails:
    msg['BCC'] = ', '.join(bcc_emails)

# Add body to the message
msg.attach(MIMEText(body, 'plain'))

try:
    # Create SMTP session for sending the mail
    server = smtplib.SMTP('smtp.gmail.com', 587)  # Use Gmail SMTP server
    server.starttls()  # Enable security

    # Login with mail_id and password
    server.login(sender_email, "your-password")

    # Convert the Multipart msg into a string
    text = msg.as_string()

    # Send the mail to all recipients (including CC and BCC)
    all_recipients = receiver_emails + cc_emails + bcc_emails
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
