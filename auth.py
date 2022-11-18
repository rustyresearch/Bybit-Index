from pybit import spot
import json

with open('index/keys.json') as j:
    keys = json.load(j)

session_auth = spot.HTTP(
    endpoint='https://api.bybit.com',
    api_key=keys['api_key'],
    api_secret=keys['api_secret']
)
