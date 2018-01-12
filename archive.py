import json
import os

import dateutil.parser
import requests
import time

token = ""

feed_url = "https://graph.facebook.com/v2.11/me/posts?access_token=%s" % token

try:
    os.makedirs("./messages")
except OSError:
    pass

feed = {}
p = 0
while feed == {} or len(feed['data']) > 0:
    p += 1
    try:
        feed = requests.get(feed_url).json()

        if p < 55:
            feed_url = feed['paging']['next']
            continue
            
        for msg in feed['data']:
            ts = time.mktime(dateutil.parser.parse(msg['created_time']).timetuple())
            path = "./messages/%s.json" % ts
            
            if os.path.exists(path):
                continue
    
            likes_url = "https://graph.facebook.com/v2.11/%s/reactions?access_token=%s" % (msg['id'], token)
            likes_data = requests.get(likes_url).json()
            msg['reactions'] = len(likes_data.get('data', []))
    
            comments_url = "https://graph.facebook.com/v2.11/%s/comments?access_token=%s" % (msg['id'], token)
            comments_data = requests.get(comments_url).json()
            msg['comments'] = len(comments_data.get('data', []))
    
            if msg['reactions'] + msg['comments'] > 20:
                f = open(path, 'w')
                json.dump(msg, f)
                f.close()
        
        print("Pulled page %s" % p)
        feed_url = feed['paging']['next']
    except Exception as e:
        print(e)
        print(feed)
        time.sleep(5)
        
        
