"""Class for email objects which will be used for posting emails"""

class Attachment:
    def __init__(self, name, url):
        self.name = name
        self.url = url

class Email:

    #If any of the attributes isn't present, pass None.
    def __init__(self, sender, subject, body):
        self.sender = sender;
        self.subject = subject
        self.body = body
        self.attachment_list = []