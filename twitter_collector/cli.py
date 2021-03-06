import argparse
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ''))
from twitter import Twitter

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--username", "-u", required=True)
    arg_parser.add_argument("--csv", action='store_true')
    arg_parser.add_argument("--media", action='store_true')
    args = arg_parser.parse_args()
    print('Target user is', args.username)
    twitter = Twitter(args.username)
    if args.csv:
        twitter.create_csv()
    if args.media:
        twitter.user_timeline()
    return


if __name__ == '__main__':
    main()