import json
import urllib.request
import urllib.parse

import attachtype
import read_emails

PAGE_ACCESS_TOKEN = 'xxxxxxxxxxxx'
HOST_URL = 'https://graph.facebook.com/v3.2'
PAGE_ID = '445446012132531'

def set_access_token(access_token):
    global PAGE_ACCESS_TOKEN
    PAGE_ACCESS_TOKEN = access_token

def construct_msg(mail):
    msg = 'Naarayan, Naarayan!\n\n'
    msg += mail.sender + ' has mailed\n'
    msg += 'Subject : ' + mail.subject + '\n\n'
    msg += mail.body + '\n\n'
    attached_media_list = []
    count = 0
    for attachment in mail.attachment_list:
        type = attachtype.attachmentType(attachment.name)
        print(attachment.name)
        if type == 2:
            count += 1
            if count == 1:
                msg += 'Attachment list: \n\n'
            msg += str(count) + '. ' + attachment.name + '\n'
            msg += attachment.url + '\n'
        elif type == 0:
            attached_media_list.append(attachment)
    return (msg,attached_media_list)

def connect(url, data = None):
    response = urllib.request.urlopen(url,data)
    response = json.loads(response.read().decode())
    return response

def post_feed(msg, attached_media_data_dict):
    if attached_media_data_dict == None:
        attached_media_data_dict = {}
    url = HOST_URL + '/' + PAGE_ID + '/feed'
    data_dict = {'message' : msg, 'access_token' : PAGE_ACCESS_TOKEN}
    data_dict.update(attached_media_data_dict)
    data = urllib.parse.urlencode(data_dict).encode('ascii')
    return connect(url,data)
 
def post_pic(img_url, published = 'false', caption = None):
    url = HOST_URL + '/' + PAGE_ID + '/photos'
    data_dict = {'url' : img_url, 'published' : published, 'access_token' : PAGE_ACCESS_TOKEN}
    if caption:
        data_dict.update({'caption' : caption})
    data = urllib.parse.urlencode(data_dict).encode('ascii')
    return connect(url,data)

def make_attached_media_data_dict(attached_media_list):
    attached_media_data_dict = {}
    for i in range(len(attached_media_list)):
        resp = post_pic(img_url=attached_media_list[i].url, caption=attached_media_list[i].name)
        attached_media_data_dict['attached_media[' + str(i) + ']'] \
            = '{"media_fbid":"' + resp['id'] + '"}'
    return attached_media_data_dict

def fetch_and_post():
    mail_list = read_emails.read_mail()
    print('mail count : ', len(mail_list))
    print('posting mails form mail_list')
    for mail in mail_list:
        print('sender  : ' + mail.sender)
        print('subject : ' + mail.subject)
        print('attachment count:', len(mail.attachment_list))
        msg,attached_media_list = construct_msg(mail)
        attached_media_data_dict = make_attached_media_data_dict(attached_media_list)
        print('posting')
        resp = post_feed(msg,attached_media_data_dict)
        print(resp)
        print('--------------------------')
