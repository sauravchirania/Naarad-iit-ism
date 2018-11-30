'''class for email objects which will be used for posting'''

class attachment:
    def __init__(self,name,url):
        self.name = name
        self.url = url

class email:

    #if any of the attribte is not present , pass None.
    def __init__(self,name, email_addr, subject, body, attachment_list):
        self.name = name;
        self.email_addr = email_addr
        self.subject = subject
        self.body = body
        self.attachment_list = attachment_list