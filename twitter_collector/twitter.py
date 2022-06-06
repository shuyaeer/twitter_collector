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
        while True:
            max_id = tweets[-1]["id"] - 1
            for tweet in tweets:
                self.images(tweet)
            json_obj = self.request_user_timeline(max_id)
            tweets = json.loads(json_obj)
            if tweets == []:
                break
        return
    
    def create_csv(self):
        tweets = json.loads(self.request_user_timeline())
        file = open(f'{self.user_name}.csv', 'w')
        writer = csv.writer(file)
        index = 1
        while True:
            max_id = tweets[-1]["id"] - 1
            for tweet in tweets:
                tweet_id = tweet['id']
                row = [index, self.__text(tweet)]
                tweet_url = 'https://twitter.com/' + \
                    self.user_name + '/status/' + str(tweet_id)
                row.insert(1, tweet_url)
                print(row)
                writer.writerow(row)
                index += 1
            json_obj = self.request_user_timeline(max_id)
            tweets = json.loads(json_obj)
            if tweets == []:
                break
        file.close()
    
    def __text(self, tweet):
        text = tweet['text']
        text = re.sub(r'\n', ' ', text)
        return text


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--username", "-u", required=True)
    arg_parser.add_argument("--csv", action='store_true')
    args = arg_parser.parse_args()
    print('target user is', args.username)
    twitter = Twitter(args.username, csv_mode=args.csv)
    twitter.user_timeline()
