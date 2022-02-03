import requests
import os
import base64
from dotenv import load_dotenv
import time
import datetime
import asyncio

load_dotenv()
username = os.getenv("REDDIT_USERNAME")
password = os.getenv("REDDIT_PASSWORD")
client_id = os.getenv("REDDIT_PERSONAL_USE_SCRIPT")
client_secret = os.getenv("REDDIT_SECRET")
webhook_url = os.getenv("WEBHOOK_URL")

auth = requests.auth.HTTPBasicAuth(base64.b64decode(client_id), base64.b64decode(client_secret))

temp_headers = {'User-Agent': 'reddit app to get saved list v1.0 (by /u/Rageacew)'}

data = {
    "grant_type": "password",
    "username": username,
    "password": base64.b64decode(password).decode('utf-8')
}

res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=temp_headers).json()

# convert response to JSON and pull access_token value
TOKEN = res['access_token']

# add authorization to our headers dictionary
headers = {**temp_headers, **{'Authorization': f"bearer {TOKEN}"}}



# this is horrible code
async def get_posts():
    # in the form of <t3_XXXXXX> or <t1_XXXXXX>
    last_saved = requests.get('https://oauth.reddit.com/user/Rageacew/saved',
                              headers=headers, params={'limit': 1}).json()['data']['children'][0]['data']['name']
    print(f"Last saved: {last_saved}")
    
    while True:
        # TODO: add error catching maybe

        saved_list = requests.get('https://oauth.reddit.com/user/Rageacew/saved',
                          headers=headers, params={'before': last_saved}).json()['data']['children']

        if saved_list:
            print('New post detected in saved list!', datetime.datetime.now().strftime('%c'))
            for post in saved_list:
                if post['kind'] == 't3': # only posts
                    requests.post(webhook_url, json={
                        "content": f"https://www.reddit.com{post['data']['permalink']}",
                    })
            last_saved = saved_list[0]['data']['name']
        else:
            print('No new post detected', datetime.datetime.now().strftime('%c'))

        await asyncio.sleep(60)

async def refresh_tokens():
    while True:
        await asyncio.sleep(3570)  # staggered in case weird shit happens
        print('Refreshing tokens...', datetime.datetime.now().strftime('%c'))
        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=temp_headers).json()
        TOKEN = res['access_token']
        headers['Authorization'] = f'bearer {TOKEN}'


async def main():
    await asyncio.gather(get_posts(), refresh_tokens())

asyncio.run(main())