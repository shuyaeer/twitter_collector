# TwitterCollector

TwitterCollector is a Python library for collecting mdia on Twitter.

## Installation

Clone the repo and exec  `pip install .`

After that, you can use the `twoker` command at command line and your Python code.

```bash
$ git clone git@github.com:shuyaeer/$twitter_collector.git
$ cd twitter_collector
$ pip install .
which twoker
/home/ubuntu/.pyenv/shims/twoker
```

## Configulation

This project use hte Twitter API, so u have to register and enable [twitter api](https://developer.twitter.com/en/docs/twitter-api)
When you gain the BERER TOKEN, you must export that token.

```bash
export TWITTER_BEARER_TOKEN="YOUR TOKEN"
```

*In the future, I'm suppose to make this tool executalbe without Twitter API*

## Usage

```text

twoker -h
usage: twoker [-h] --username USERNAME [--csv]

optional arguments:
  -h, --help            show this help message and exit
  --username USERNAME, -u USERNAME
  --csv export tweet contents as csv
```

```bash
$ twoker -u joymanjoyman --csv # export as csv
```
