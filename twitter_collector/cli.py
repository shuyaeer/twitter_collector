import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ''))
from twitter import Twitter

def main():
    twitter = Twitter('joymanjoyman')
    twitter.user_timeline()
    return


if __name__ == '__main__':
    main()