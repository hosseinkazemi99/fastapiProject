import json
from datetime import datetime
from typing import BinaryIO
import requests


class Instagram:
    def __init__(self):
        self.session = None

    def load(self, session):
        self.session = session

    async def login(self, username: str, password: str) -> dict:
        url = 'https://www.instagram.com/accounts/login/'
        login_url = 'https://www.instagram.com/api/v1/web/accounts/login/ajax/'

        time = int(datetime.now().timestamp())

        response = requests.get(url)
        csrf = response.cookies.get('csrftoken')

        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        login_header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/77.0.3865.120 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "x-csrftoken": 'Vouc7J0oJSpBciIJptNQAxRA5dDkKWq2'
        }

        login_response = requests.post(login_url, data=payload, headers=login_header)
        json_data = json.loads(login_response.text)
        # print(json_data)
        if json_data.get("authenticated"):
            cookies = login_response.cookies
            cookie_jar = cookies.get_dict()

            self.session = {
                "csrftoken": cookie_jar['csrftoken'],
                "sessionid": cookie_jar['sessionid'],
                "ds_user_id": cookie_jar['ds_user_id'],
                "mid": cookie_jar['mid'],
                "ig_did": cookie_jar['ig_did'],
                "rur": cookie_jar['rur'],

            }

            return self.session

        raise Exception(login_response.text)


