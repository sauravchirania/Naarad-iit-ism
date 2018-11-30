import urllib.request
import urllib.parse
import json

user_access_token = input()
page_access_token = input()
host_url = 'https://graph.facebook.com/v3.2'
page_id = '445446012132531'

def connect(url,data=None):
    response = urllib.request.urlopen(url,data)
    response = json.loads(response.read().decode())
    return response

def my_detail():
    url = host_url+'/me'
    data = urllib.parse.urlencode({'fields' : 'id,name', 'access_token' : user_access_token}).encode('ascii')
    return connect(url,data)
    
def post_feed(msg):
    url = host_url+'/'+page_id+'/feed'
    data = urllib.parse.urlencode({'message' : msg, 'access_token' : page_access_token}).encode('ascii')
    return connect(url,data)

resp = my_detail()
print(resp)
