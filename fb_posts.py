import urllib.request
import urllib.parse
import json
import email_class
import read_emails
import img_uploader
import attachtype
#import ex

user_access_token = input()
page_access_token = input()
host_url = 'https://graph.facebook.com/v3.2'
page_id = '445446012132531'

def construct_msg(mail):
    msg = ''
    msg += mail.sender + ' has mailed\n\n'
    msg += 'Subject : '+mail.subject + '\n\n'
    msg += mail.body + '\n\n'
    attached_media_list = []
    if(len(mail.attachment_list)):
        msg += 'Attachment list :\n\n'
        count = 0
        for attachment in mail.attachment_list:
            type = attachtype.attachmentType(attachment.name)
            if type == 2:
                count += 1
                msg += str(count) + '. ' + attachment.name + '\n'
                msg += attachment.url + '\n'
            elif type == 0:
                attached_media_list.append(attachment)

    return (msg,attached_media_list)

def connect(url,data=None):
    response = urllib.request.urlopen(url,data)
    response = json.loads(response.read().decode())
    return response

def my_detail():
    url = host_url+'/me'
    data = urllib.parse.urlencode({'fields' : 'id,name', 'access_token' : user_access_token}).encode('ascii')
    return connect(url,data)

def post_feed(msg,attached_media_data_dict):
    if(attached_media_data_dict==None):
        attached_media_data_dict = {}
    url = host_url+'/'+page_id+'/feed'
    data_dict = {'message' : msg, 'access_token' : page_access_token}
    data_dict.update(attached_media_data_dict)
    data = urllib.parse.urlencode(data_dict).encode('ascii')
    return connect(url,data)
 
def post_pic(img_url,published='false', caption=None):
    url = host_url+'/'+page_id+'/photos'
    data_dict = {'url' : img_url, 'published' : published,'access_token' : page_access_token}
    if(caption):
        data_dict.update({'caption' : caption})
    data = urllib.parse.urlencode(data_dict).encode('ascii')
    return connect(url,data)

def makeAttachedMediaDataDict(attached_media_list):
    attached_media_data_dict = {}
    for i in range(len(attached_media_list)):
        resp = post_pic(img_url=attached_media_list[i].url, caption=attached_media_list[i].name)
        attached_media_data_dict['attached_media['+str(i)+']'] = '{"media_fbid":"'+resp['id']+'"}'
    return attached_media_data_dict

def fetchAndPost():
    resp = my_detail()
    print("user : "+resp['name'])
    mail_list = read_emails.readmail()
    #mail_list = ex.generate_mail()
    print('mail count : ', len(mail_list))
    print('posting mails form mail_list')
    for mail in mail_list:
        msg,attached_media_list = construct_msg(mail)
        print("attached_media_list : ",attached_media_list)
        attached_media_data_dict = makeAttachedMediaDataDict(attached_media_list)
        print('attached_media_data_dict : ', attached_media_data_dict)
        resp = post_feed(msg,attached_media_data_dict)
        print(resp)

fetchAndPost()