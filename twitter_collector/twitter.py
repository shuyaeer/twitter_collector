import os
import time
import json

import requests


class Twitter:
    def __init__(self, user_name, default_dir_path=None):
        self.user_name = user_name
        if default_dir_path is None:
            self.default_dir_path = f'./{user_name}'
        else:
            self.default_dir_path = default_dir_path
        if not os.path.isdir(self.default_dir_path):
            os.makedirs(self.default_dir_path)
        self.BEARER = os.environ['BEARER']

    def request_user_timeline(self, max_id=None):
        time.sleep(1)
        endpoint = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        params = {
            'screen_name': self.user_name,
            'count': 200,
            'exclude_replies': True,
            'include_trs': True,
            'max_id': max_id,
        }
        headers = {
            'Authorization': f"Bearer {self.BEARER}"
        }
        response = requests.get(endpoint, headers=headers,
                                params=params, timeout=5.5)
        return response.text

    def download_(self, url):
        response = requests.get(url, timeout=5.5)
        return response.content

    def images(self):
        if not os.path.isdir(f'./{self.default_dir_path}/images'):
            os.makedirs(f'./{self.default_dir_path}/images')
        json_response = twitter.request_user_timeline()
        tweets = json.loads(json_response)
        while True:
            max_id = tweets[-1]["id"] - 1
            for tweet in tweets:
                image_index = 1
                tweet_id = tweet['id']
                media_info = tweet["entities"].get("media")
                if media_info is None: continue
                additional = tweet["extended_entities"]
                if media_info is None: continue
                for media in media_info:
                    if media is None: continue
                    with open(f'{self.default_dir_path}/images/{tweet_id}_{image_index}.jpg', 'wb') as f:
                        f.write(self.download_(media['media_url_https']))
                    image_index += 1
                if additional is None: continue
                additional_images = additional['media']
                additional_images.pop(0)
                for image in additional_images:
                    if image is None: continue
                    with open(f'{self.default_dir_path}/images/{tweet_id}_{image_index}.jpg', 'wb') as f:
                        f.write(self.download_(media['media_url_https']))
                    image_index += 1
            json_obj = twitter.request_user_timeline(max_id)
            tweets = json.loads(json_obj)
            if tweets == []:
                break

if __name__ == '__main__':
    twitter = Twitter('joymanjoyman')
    twitter.images()
