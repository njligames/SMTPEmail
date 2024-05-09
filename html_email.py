import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, recipient, html_content):
    # Email configuration
    smtp_server = 'your_smtp_server'
    smtp_port = 587  # or 465 for SSL/TLS
    sender_email = 'your_email@example.com'
    sender_password = 'your_email_password'

    # Create a multipart message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient
    message['Subject'] = subject

    # Add HTML content to email
    html_part = MIMEText(html_content, 'html')
    message.attach(html_part)

    # Connect to SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Enable TLS encryption
        server.login(sender_email, sender_password)
        server.send_message(message)

# Example usage
subject = "Join Our AI Model Training Community!"
recipient = "recipient@example.com"

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Join Our AI Model Training Community!</title>
</head>
<body>
    <h1>Welcome to Our AI Community!</h1>
    <p>Dear [Recipient's Name],</p>
    <p>Are you passionate about AI and eager to contribute to cutting-edge research? We're thrilled to invite you to join our community of AI enthusiasts and help train our next-generation AI model!</p>
    <p>...</p>
    <p>Best regards,<br>[Your Name]<br>[Your Title/Position]</p>
</body>
</html>
"""

send_email(subject, recipient, html_content)
