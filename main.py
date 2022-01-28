import requests
import os
import base64
from dotenv import load_dotenv
import time

load_dotenv()
username = os.getenv("REDDIT_USERNAME")
password = os.getenv("REDDIT_PASSWORD")
client_id = os.getenv("REDDIT_PERSONAL_USE_SCRIPT")
client_secret = os.getenv("REDDIT_SECRET")
webhook_url = os.getenv("REDDIT_WEBHOOK_URL")

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

while True:


    time.sleep(30)
