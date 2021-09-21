
import argparse
import json
from collections import defaultdict

# TODO
"""
1. Probably use regexes to handle prefixes a bit better
    a) Sep out "imaging_level_2"+ web-assets prefix so it aligns with DCC source bucket
    b) Replacing `tif` ext with `png`
    c) Getting basename of prefix without any ext
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

    # Parse bucket_manifest
    keys = []
    with open(bucket_manifest, 'r') as fh:
        for line in fh:
            bucket_name, s3key = line.strip().split('\t')
            keys.append(s3key)

    # Parse target assets
    thumbnails = defaultdict(str)
    m_stories = defaultdict(list)

    thumbnails_prefix = f'thumbnails/{bucket_name}/'
    minerva_stories_prefix = f'minerva_stories/{bucket_name}/'
    with open(assets, 'r') as fh:
        for line in fh:
            bucket_name, s3key = line.strip().split('\t')
            if s3key.startswith(thumbnails_prefix):
                thumbnails['/'.join(s3key.split('/')[2:])] = s3key
            elif s3key.startswith(minerva_stories_prefix):
                if 'Group' in s3key:
                    pass
                else:
                    asset_lookup_name = '/'.join(s3key.split('/')[2:-1])  # indexOf "imaging_level_2"
                    m_stories[asset_lookup_name].append(s3key)

    # for k, v in m_stories.items():
    #     print(f'{k} => {v}')

    # Map available thumbnail assets
    records = []
    for key in keys:
        basename = key.split('.')[0]
        png = key.replace('.tif', '.png')

        rec = {
            "htan_bucket": bucket,
            "origin": key,
            "thumbnail": None,
            "minerva_story": None,
        }

        if png in thumbnails:
            rec['thumbnail'] = {
                "file": thumbnails[png],
                "url": S3_ASSETS_URL_FORMAT.format(S3_KEY=thumbnails[png]),
            }

        if basename in m_stories:
            files = m_stories.get(basename, [])
            urls = [S3_ASSETS_URL_FORMAT.format(S3_KEY=f) for f in files]
            rec['minerva_story'] = {'files': files, 'urls': urls}

        if rec['thumbnail'] or rec['minerva_story']:
            records.append(rec)

    print(json.dumps(records))


if __name__ == '__main__':
    main()
