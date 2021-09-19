
import argparse
import json

import requests

# TODO
"""
1) Combine multi center results into a single json assets mapping file
2) [OPTIONAL] Grab urls from each json output & test urls against endpoint
"""

def process_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--json-files', nargs='+')
    parser.add_argument('--test-url-access', default=False, action='store_true')

    args = parser.parse_args()
    return args

def main():
    args = process_args()
    json_files = args.json_files
    test_url_access = args.test_url_access

    # Combine data
    records = []
    for f in json_files:
        with open(f, 'r') as fh:
            records += json.load(fh)

    # Grab all urls
    thumbnail_urls = []
    minerva_story_urls = []
    for rec in records:
        thumbnail = rec.get('thumbnail', None)
        minerva_story = rec.get('minerva_story', None)

        # Some centers have either thumbnails or minerva_stories
        if thumbnail:
            thumbnail_urls.append(thumbnail['url'])
        if minerva_story:
            minerva_story_urls += minerva_story['urls']

    # Request access
    def get_url(url):
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            print(url, r.status_code)
        else:
            print(url)
            print(r.text)

    if test_url_access:
        [get_url(t) for t in thumbnail_urls]
        [get_url(m) for m in minerva_story_urls]
    else:
        print(json.dumps(records))


if __name__ == '__main__':
    main()
