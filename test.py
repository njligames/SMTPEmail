# project/test.py

import unittest

import os
import csv
from SMTPEmail import SMTPEmail

class TestCalculations(unittest.TestCase):

    def getEmails(self, filename):
        emails = None
        with open(filename, mode ='r')as file:    
            csvFile = csv.DictReader(file)
            emails = []
            for lines in csvFile:
                emails.append(lines["email"])
        return emails

    def getFileContent(self, filename):
        content = ""
        with open(filename, 'r') as reader:
            content = reader.read()
        return content

    def test_class(self):
        sender_email = os.environ["EMAIL"]
        password = os.environ["PASSWORD"]
        content_file = os.environ['HTMLFILE']
        subject_file = os.environ['SUBJECTFILE']
        bcc_file = os.environ['BCCFILE']

        htmlContent = self.getFileContent(content_file)
        subject = self.getFileContent(subject_file)
        bccEmails = self.getEmails(bcc_file)

        smtpEmail = SMTPEmail()
        smtpEmail.setSubject(subject)
        smtpEmail.setHTMLBody(htmlContent)
        smtpEmail.setBCCEmails(bccEmails)
        smtpEmail.send(sender_email, password)



if __name__ == '__main__':
    unittest.main()

