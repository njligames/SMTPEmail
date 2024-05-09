# Import necessary libraries
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

password = os.environ["PASSWORD"]
sender_email = os.environ["EMAIL"]
smtp_address = os.environ["SMTP"]

# Define sender and receiver email addresses
sender_email = 'james@njligames.com'
receiver_email = 'jamesfolk1@gmail.com'

# Define email subject and body
subject = 'Feedback Mail'
body = 'This is a feedback mail sent from Python script.'

# Create message object instance
msg = MIMEMultipart()

# Setup the parameters of the message
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

# Add body to the message
msg.attach(MIMEText(body, 'plain'))

# Create SMTP session for sending the mail
server = smtplib.SMTP(smtp_address, 587)  # Use Gmail SMTP server
server.starttls()  # Enable security

# Login with mail_id and password
server.login(sender_email, password)

# Convert the Multipart msg into a string
text = msg.as_string()

# Send the mail
server.sendmail(sender_email, receiver_email, text)

# Close the connection
server.quit()

print('Mail sent successfully!')
