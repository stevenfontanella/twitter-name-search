from itertools import *
import json
import twitter
import sys
from string import ascii_lowercase
from functools import wraps
import time

import pdb

creds = json.loads(open("creds.json").read())
api = twitter.Api(**creds)

def loginfo(s):
    print(s)

# seems like 800 per 15 minute period
def rate_limit(f, delay=60):
    @wraps(f)
    def limited(*args, **kwargs):
        while True:
            try:
                return f(*args, **kwargs)
            except twitter.error.TwitterError as e:
                code = e.args[0][0]["code"]
                if code == 88:
                    loginfo("Rate limiting...")
                    time.sleep(delay)
                else:
                    loginfo(f"Unhandled exception: {e}")
                    raise
    return limited

@rate_limit
def user_exists(username):
    try:
        # TODO: maybe I should write my own getUser that is rate-limited, then leave the catching logic here
        api.GetUser(screen_name=username)
    except twitter.error.TwitterError as e:
        code = e.args[0][0]["code"]
        # user is suspended
        if code == 63:
            return True
        elif code == 50:
            return False
        raise
    return True

def search(names):
    try:
        for i, name in enumerate(names, 1):
            exists = user_exists(name)
            if not exists:
                print(f"{name} is available")
    finally:
        print(f"Processed {i} names")
        print(f"Finished with {name}")
    # for name in filterfalse(user_exists, names):
    #     print(f"{name} is available")

def names():
    with open("fivewords.txt") as f:
        for line in f:
            yield line.rstrip("\n")

def main():
    # start = 0
    # count = 100

    # tries = islice(names(), start, start + count)
    # tries = names()

    tries = ("".join(chain("qu", *p)) for p in product(ascii_lowercase, repeat=3))
    # print(list(islice(tries, 100)))
    # tries = islice(tries, 100)
    # print(list(tries))

    # tries = islice(("".join(chain(fst, cs)) for fst, cs in product(ascii_lowercase[ascii_lowercase.find("q"):], product(ascii_lowercase, repeat=4))), start, start + count)
    # print(list(tries))
    # print(list(tries))
    search(tries)

if __name__ == "__main__":
    main()

