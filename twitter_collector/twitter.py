import argparse
import csv
import sys
import os
import re
import time
import json

import requests

class Twitter:
    def __init__(self, user_name, default_dir_path=None, csv_mode=False):
        self.user_name = user_name
        self.is_csv = csv_mode
        if default_dir_path is None:
            self.default_dir_path = f'./output/{user_name}'
        else:
            self.default_dir_path = default_dir_path
        if not os.path.isdir(self.default_dir_path):
            os.makedirs(self.default_dir_path)
        try:
            self.BEARER = os.environ['TWITTER_BEARER_TOKEN']
        except KeyError as e:
            print(e)
            sys.exit()

    def request_user_timeline(self, max_id=None):
        time.sleep(1)
        endpoint = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        params = {
            'screen_name': self.user_name,
            'count': 200,
            'exclude_replies': True,
            'include_trs': False,
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

    def images(self, tweet):
        tweet_id = tweet['id']
        media_info = tweet["entities"].get("media")
        if media_info is None: return
        self.dl_images(tweet_id, media_info, image_index=1)
        additional = tweet["extended_entities"]
        if additional is None: return
        additional_images = additional['media']
        additional_images.pop(0)
        self.dl_images(tweet_id, additional_images)
        return
    
    def text(self, id, tweet):
        url = None
        text = tweet['text']
        text = re.sub(r'\n', ' ', text)
        if 'http' in text:
            url = re.findall(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', text)
            print(url)
        return [id, text, url]
    
    def dl_images(self, tweet_id, media_info, image_index=2):
        for media in media_info:
            if media is None:
                continue
            url = media['media_url_https']
            print(url)
            with open(f'{self.default_dir_path}/images/{tweet_id}_{image_index}.jpg', 'wb') as f:
                f.write(self.download_(url))
            image_index += 1
        return image_index


    def user_timeline(self):
        tweets = json.loads(self.request_user_timeline())
        if not os.path.isdir(f'./{self.default_dir_path}/images'):
            os.makedirs(f'./{self.default_dir_path}/images')
        id = 1    
        while True:
            max_id = tweets[-1]["id"] - 1
            if self.is_csv:
                for tweet in tweets:
                    with open(f'{self.user_name}.csv', 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow(self.text(id, tweet))
                    id += 1
            else:
                for tweet in tweets:
                    self.images(tweet)
            json_obj = self.request_user_timeline(max_id)
            tweets = json.loads(json_obj)
            if tweets == []:
                break
        return



if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--csv", help="optional")
    args = arg_parser.parse_args()
    twitter = Twitter('joymanjoyman', csv_mode=args.csv)
    twitter.user_timeline()
