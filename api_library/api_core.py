import hmac
import hashlib
import base64
import json
import time
import requests
import os

env_key = os.environ.get('COINDCX_API_KEY')
env_secret = os.environ.get('COINDCX_API_SECRET')

class CoinDCXAPICore:
    def __init__(self, api_key=None, secret_key=None):
        self.api_key = api_key if api_key else env_key
        self.base_url = 'https://api.coindcx.com'
        self.secret_bytes = bytes(secret_key if secret_key else env_secret, encoding='utf-8')

    def make_post_request(self, url: str, body: dict):
        body["timestamp"] = int(round(time.time() * 1000))
        json_body = json.dumps(body, separators = (',', ':'))
        signature = hmac.new(self.secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': self.api_key,
            'X-AUTH-SIGNATURE': signature
        }

        response = requests.post(url, data = json_body, headers = headers)
        data = response.json()
        return data
