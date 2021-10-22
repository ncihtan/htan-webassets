
import sys
import argparse
import json
from collections import defaultdict

from requests.utils import requote_uri

# TODO
"""
1. Probably use regexes to handle prefixes a bit better
2. Expand past imaging_level_2 mapping
3. Could cleanup thumbnail + minerva_story dict and turn it into a class
"""


def process_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-b', '--bucket', type=str, required=True, help='Bucket name')
    parser.add_argument('-m', '--bucket-manifest', help='')
    parser.add_argument('-a', '--assets', help='')
    parser.add_argument('--cdn', required=True, help='Domain name for AWS Cloudfront CDN')
    args = parser.parse_args()
    return args


def main():
    args = process_args()
    bucket_manifest = args.bucket_manifest
    bucket = args.bucket
    assets = args.assets
    domain_name = args.cdn

    S3_ASSETS_URL_FORMAT = 'https://%s/{S3_KEY}' % domain_name

    # Load up a centers bucket_manifest
    keys = []
    with open(bucket_manifest, 'r') as fh:
        for line in fh:
            _, s3key = line.strip().split('\t')
            if 'metadata' in line:
                continue
            keys.append(s3key)

    # Generate assets LIST, group by thumbnail or minerva_story
    thumbnails = defaultdict(str)
    m_stories = defaultdict(list)

    thumbnails_prefix = f'thumbnails/{bucket}/'
    minerva_stories_prefix = f'minerva_stories/{bucket}/'
    with open(assets, 'r') as fh:
        for line in fh:
            _, s3key = line.strip().split('\t')

            if s3key.startswith(thumbnails_prefix):
                thumbnails['/'.join(s3key.split('/')[2:])] = s3key
            elif s3key.startswith(minerva_stories_prefix):
                if 'Group' in s3key:
                    pass
                else:
                    asset_lookup_name = '/'.join(s3key.split('/')[2:-1])  # indexOf "imaging_level_2"
                    m_stories[asset_lookup_name].append(s3key)

    # for k, v in thumbnails.items():
    #     print(f'{k} => {v}')
    # for k, v in m_stories.items():
    #     print(f'{k} => {v}')

    # Map available thumbnail assets
    records = []
    for key in keys:
        if 'metadata' in key:
            continue

        basename = key.split('.')[0].strip()

        if key.endswith('.tif'):
            png = key.replace('.tif', '.png').strip()
        elif key.endswith('.tiff'):
            png = key.replace('.tiff', '.png').strip()
        elif key.endswith('.svs'):
            png = key.replace('.svs', '.png').strip()
        else:
            # Skip every other filetype, like csvs
            continue

        rec = {
            "htan_bucket": bucket,
            "origin": key,
            "thumbnail": None,
            "minerva_story": None,
        }

        # Check if BUCKET_KEY has a thumbnail ASSET
        if png and png in thumbnails:
            rec['thumbnail'] = {
                "file": thumbnails[png],
                "url": requote_uri(S3_ASSETS_URL_FORMAT.format(S3_KEY=thumbnails[png])),
            }

        # Check if BUCKET_KEY has a minerva story ASSET
        if basename in m_stories:
            files = m_stories.get(basename, [])
            urls = [requote_uri(S3_ASSETS_URL_FORMAT.format(S3_KEY=f)) for f in files]
            rec['minerva_story'] = {'files': files, 'urls': urls}

        # Keep record if either contains thumbnail or minerva_story
        if rec['thumbnail'] or rec['minerva_story']:
            records.append(rec)

    print(json.dumps(records))


if __name__ == '__main__':
    main()
