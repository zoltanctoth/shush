#!/usr/bin/env python3

import sys
import re
import os

from urllib.parse import urlencode
from urllib.request import Request, urlopen

DEFAULT_DND_MINS = 60


def get_tokens(file):
    with open(file) as f:
        s = f.read()
        candidates = re.findall(r"[\w\-]+|[^\w\s]", s, re.UNICODE)
        return filter(lambda c: c.startswith("xoxp-"), candidates)

def http_post(url, payload):
    request = Request(url, urlencode(payload).encode())
    urlopen(request).read()

if __name__ == "__main__":
    if len(sys.argv) > 1 and (not sys.argv[1].isdigit() and not sys.argv[1] == "stop"):
        print("Usage: \n   " + sys.argv[0] + " [snooze mins]", file=sys.stderr)
        print("   " + sys.argv[0] + " stop", file=sys.stderr)
        sys.exit(1)
 
    tokens = get_tokens(os.path.expanduser("~/.hushrc"))

    if len(sys.argv) > 1 and sys.argv[1] == "stop":
        url = "https://slack.com/api/dnd.endSnooze"
        for token in tokens:
            print("Stopping snooze for token " + token[:9] + "...")
            params = {
                'token': token
            }
            http_post(url, params)
        sys.exit(0)

    if len(sys.argv) == 1:
        mins = DEFAULT_DND_MINS
    else:
        mins = int(sys.argv[1])

    url = "https://slack.com/api/dnd.setSnooze"
    for token in tokens:
        print("Starting a " + str(mins) + " minute snooze for token " + token[:9] + "...")
        params = {
            'token': token,
            'num_minutes': mins
        }
        http_post(url, params)
    sys.exit(0)
