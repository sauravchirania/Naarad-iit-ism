import os

import fb_posts
import read_emails

if not os.path.isdir('attachments'):
    os.mkdir('attachments',0o775)

fb_posts.set_access_token(input('Set fb page access token: '))
read_emails.set_access_token(input('Set dropbox access token: '))
read_emails.set_email_credentials(input('Email: '),input('Password: '))

fb_posts.fetch_and_post()
