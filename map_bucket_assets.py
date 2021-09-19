
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
    parser.add_argument('-s', '--schematic-bucket-manifest', help='A schematic manifest file with relevant metadata')
    parser.add_argument('-m', '--bucket-manifest', help='')
    parser.add_argument('-a', '--assets', help='')
    args = parser.parse_args()
    return args


def main():
    args = process_args()
    bucket_manifest = args.bucket_manifest
    bucket = args.bucket
    assets = args.assets

    # S3_ASSETS_BUCKET = 'https://htan-imaging-example-datasets.s3.amazonaws.com'
    # S3_ASSETS_URL_FORMAT = '{S3_ASSETS_BUCKET}/{S3_KEY}'
    S3_ASSETS_URL_FORMAT = 'https://htan-imaging-example-datasets.s3.amazonaws.com/{S3_KEY}'

    # Parse bucket_manifest
    manifest_headers = ['bucket_name', 'prefix']
    keys = []
    with open(bucket_manifest, 'r') as fh:
        for line in fh:
            bucket_name, s3key = line.strip().split('\t')
            keys.append(s3key)

    # Parse target assets
    thumbnails = defaultdict(str)
    m_stories = defaultdict(list)

    thumbnail_loc = f'miniature-drafts/{bucket_name}/'
    m_stories_gsloc = f'auto-minerva-drafts/gs/{bucket_name}/'
    m_stories_s3loc = f'auto-minerva-drafts/s3/{bucket_name}/'
    with open(assets, 'r') as fh:
        for line in fh:
            bucket_name, s3key = line.strip().split('\t')
            if s3key.startswith(thumbnail_loc):
                thumbnails['/'.join(s3key.split('/')[2:])] = s3key
            elif s3key.startswith(m_stories_s3loc) or s3key.startswith(m_stories_gsloc):
                if 'Group' in s3key:
                    pass
                else:
                    asset_lookup_name = '/'.join(s3key.split('/')[3:-1])  # indexOf "imaging_level_2"
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

    # Map bucket manifest objects with available thumbnails
    """
    [
      {
        "htan_center": "HTAN HMS",
        "filename": "imaging_level_2/CRC202105/CRC17.ome.tif",
        "htan_parent_biospecimen_id": "HTA7_982_2",
        "htan_data_file_id": "HTA7_982_1000",
        "imaging_assay_type": "t-CyCIF",
        "size_c": 36,
        "thumbnail": "CRC17.ome.png"
      },
      {
        "htan_center": "HTAN HMS",
        "filename": "imaging_level_2/CRC202105/CRC09.ome.tif",
        "htan_parent_biospecimen_id": "HTA7_989_2",
        "htan_data_file_id": "HTA7_989_1000",
        "imaging_assay_type": "t-CyCIF",
        "size_c": 36,
        "thumbnail": "CRC09.ome.png"
      }
    ]
    """


if __name__ == '__main__':
    main()
