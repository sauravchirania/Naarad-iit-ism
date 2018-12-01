import imaplib
import email
import email_class
import os

ORGANISATION = "@gmail.com"
EMAIL = "xxxxxxxx" + ORGANISATION
PASSWORD = "xxxxxxxx"
IMAP_SERVER = "imap.gmail.com"
ATTACHMENT_DIR = "/home/anupam/naarad_project/Naarad-iit-ism/attachment"

def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None,True)

def get_attachments(msg, mailobj):
    for part in msg.walk():
        if part.get_content_maintype()=='multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()

        if bool(fileName):
            filePath = os.path.join(ATTACHMENT_DIR, fileName)
            with open(filePath,'wb') as f:
                f.write(part.get_payload(decode=True))
            attachment_obj = email_class.attachment(fileName, filePath)
            mailobj.attachment_list.append(attachment_obj)


def readmail():
    mail_list = []
    connection = imaplib.IMAP4_SSL(IMAP_SERVER)
    connection.login(EMAIL, PASSWORD)
    connection.select('inbox')
    return_code , data = connection.search(None, '(FROM "Anupam" UNSEEN)')
    mail_ids_string = data[0]
    mail_ids = mail_ids_string.split()
    for mail_id in mail_ids:
        typ, response = connection.fetch(mail_id, '(RFC822)' )
        for response_part in response:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email_subject = msg['subject']
                email_from = msg['from']
                email_body = get_body(msg).decode('utf-8')
                mailobj = email_class.email(email_from,email_subject,email_body)
                get_attachments(msg, mailobj)
                print(mailobj.sender)
                print(mailobj.subject)
                print(mailobj.body)
                print("---------------------")
                mail_list.append(mailobj)
    return mail_list
