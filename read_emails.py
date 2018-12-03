import imaplib
import email
import email_class
import os
import db

ORGANISATION = input()
EMAIL = input() + ORGANISATION
PASSWORD = input()
IMAP_SERVER = 'imap.gmail.com'
ATTACHMENT_DIR = 'attachments'
DROPBOX_ACCESS_TOKEN = input()

def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)

def get_attachments(msg, mail_obj):
    uploader= db.Uploader()
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        file_name = part.get_filename()

        if bool(file_name):
            file_path = os.path.join(ATTACHMENT_DIR, file_name)
            with open(file_path,'wb') as f:
                f.write(part.get_payload(decode=True))
            if (len(mail_obj.attachment_list) == 0):
                uploader.connect_to_server(DROPBOX_ACCESS_TOKEN)
            link = uploader.upload_file(file_name, file_path)
            attachment_obj = email_class.Attachment(file_name, link)
            mail_obj.attachment_list.append(attachment_obj)

def read_mail():
    connection = imaplib.IMAP4_SSL(IMAP_SERVER)
    connection.login(EMAIL, PASSWORD)
    connection.select('inbox')
    return_code , data = connection.search(None, '(FROM "Saurav" UNSEEN)')
    mail_ids_string = data[0]
    mail_ids = mail_ids_string.split()
    mail_obj_list = []
    for mail_id in mail_ids:
        typ, response = connection.fetch(mail_id, '(RFC822)' )
        for response_part in response:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email_subject = msg['subject']
                email_from = msg['from']
                email_body = get_body(msg).decode('utf-8')
                mail_obj = email_class.Email(email_from, email_subject, email_body)
                get_attachments(msg, mail_obj)
                print(mail_obj.sender)
                print(mail_obj.subject)
                print(mail_obj.body)
                print('---------------------')
                mail_obj_list.append(mail_obj)
    return mail_obj_list
