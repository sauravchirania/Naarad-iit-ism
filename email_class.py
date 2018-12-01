'''class for email objects which will be used for posting'''

class attachment:
    def __init__(self,name,url):
        self.name = name
        self.url = url

class email:

    #if any of the attribte is not present , pass None.
    def __init__(self, sender, subject, body):
        self.sender = sender;
        self.subject = subject
        self.body = body
        self.attachment_list = []