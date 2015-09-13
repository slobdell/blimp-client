import json
import urllib
import requests


class FacebookRestClient(object):

    BASE_URL = 'https://graph.facebook.com'
    ACCOUNTS = 'me/accounts'
    PHOTOS = 'me/photos'

    VERSION = "v2.4"

    def __init__(self, access_token):
        self.access_token = access_token

    def _make_get_request(self, endpoint, params=None):
        params = params or {}
        params["access_token"] = self.access_token
        full_url = "{base_url}/{version}/{endpoint}/?{get_params}".format(
            base_url=self.BASE_URL,
            version=self.VERSION,
            endpoint=endpoint,
            get_params=urllib.urlencode(params)
        )
        response = requests.get(full_url)
        response.raise_for_status()
        return json.loads(response.content)

    def _make_post_request(self, endpoint, params=None):
        params = params or {}
        params["access_token"] = self.access_token
        full_url = "{base_url}/{version}/{endpoint}/".format(
            base_url=self.BASE_URL,
            version=self.VERSION,
            endpoint=endpoint,
        )
        response = requests.post(full_url, data=params)
        response.raise_for_status()
        return json.loads(response.content)

    def get_my_accounts(self):
        params = {
            'fields': ["id", "name", "access_token"],
        }
        return self._make_get_request(self.ACCOUNTS, params=params)

    def post_photo(self, image_url, caption):
        params = {
            "url": image_url,
            "caption": caption
        }
        return self._make_post_request(self.PHOTOS, params=params)
