import requests
import os
import base64
from dotenv import load_dotenv
import time
import datetime

load_dotenv()
username = os.getenv("REDDIT_USERNAME")
password = os.getenv("REDDIT_PASSWORD")
client_id = os.getenv("REDDIT_PERSONAL_USE_SCRIPT")
client_secret = os.getenv("REDDIT_SECRET")
webhook_url = os.getenv("WEBHOOK_URL")

auth = requests.auth.HTTPBasicAuth(base64.b64decode(client_id), base64.b64decode(client_secret))

headers = {'User-Agent': 'reddit app to get saved list v1.0 (by /u/Rageacew)'}

data = {
    "grant_type": "password",
    "username": username,
    "password": base64.b64decode(password).decode('utf-8')
}

res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers).json()

# convert response to JSON and pull access_token value
TOKEN = res['access_token']

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# in the form of <t3_XXXXXX> or <t1_XXXXXX>
last_saved = requests.get('https://oauth.reddit.com/user/Rageacew/saved',
                          headers=headers, params={'limit': 1}).json()['data']['children'][0]['data']['name']

# this is horrible code
while True:
    # TODO: add error catching maybe
    # TODO: make it such that every two hours the auth token will refresh

    saved_list = requests.get('https://oauth.reddit.com/user/Rageacew/saved',
                      headers=headers, params={'before': last_saved}).json()['data']['children']

    if saved_list:
        print('New post detected in saved list!', datetime.datetime.now().time())
        for post in saved_list:
            if post['kind'] == 't3': # only posts
                requests.post(webhook_url, json={
                    "content": f"https://www.reddit.com{post['data']['permalink']}",
                })
        last_saved = saved_list[0]['data']['name']
    else:
        print('No new post detected', datetime.datetime.now().time())

    time.sleep(60)
