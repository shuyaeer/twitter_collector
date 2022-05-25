# TwitterCollector

TwitterCollector is a Python library for collecting mdia on Twitter.

## Installation

Clone the repo and exec  `pip install .`

```bash
git clone git@github.com:shuyaeer/twitter_collector.git
cd twitter_collector
pipenv install 
```

## Configulation

This project use hte Twitter API, so u have to register and enable [twitter api](https://developer.twitter.com/en/docs/twitter-api)
When you gain the BERER TOKEN, you must export that token.

```bash
export TWITTER_BEARER_TOKEN="YOUR TOKEN"
```

## Usage

```python
from twitter import Twitter
twitter = Twitter('joymanjoyman')
twitter.images()
```
