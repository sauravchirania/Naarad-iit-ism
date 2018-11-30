import imaplib
import email

ORGANISATION = "@cse.ism.ac.in"
EMAIL = "saurav.16je002321" + ORGANISATION
PASSWORD = "XXXXXXXXXXXX"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993

def readmail():
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')
    typ , data = mail.search(None, '(FROM "Director")')
    mail_ids = data[0]
    id_list = mail_ids.split()
    for i in id_list:
        print (i)
    for i in id_list:
        t, d = mail.fetch(i, '(RFC822)' )
        for response_part in d:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1].decode("utf-8"))
                email_subject = msg['subject']
                email_from = msg['from']
                print ('From : ' + email_from + '\n')
                print ('Subject : ' + email_subject + '\n')

readmail()