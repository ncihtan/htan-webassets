
import sys
import argparse
import boto3


# Basic python script skeleton
def process_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-b', '--bucket', type=str, required=True, help='Bucket name')
    parser.add_argument('-t', '--bucket-type', default='aws', const='aws', nargs='?', choices=['aws', 'gcs'], type=str, help='Bucket name')
    parser.add_argument('-p', '--profile', default='default', type=str, help='AWS profile to use')

    parser.add_argument('-o', '--output-file', type=str)

    args = parser.parse_args()
    return args

def main():
    # Handle input args
    args = process_args()
    bucket_name = args.bucket
    bucket_type = args.bucket_type
    profile = args.profile
    outfile = args.output_file

    # Configure boto3 session and client
    session = boto3.session.Session(profile_name=profile)
    if bucket_type == 'aws':
        s3 = session.resource('s3')
    elif bucket_type == 'gcs':
        # This endpoint is urlencoding spaces into '+' signs prematurely
        s3 = session.resource('s3', endpoint_url='https://storage.googleapis.com')

    # List bucket items
    bucket = s3.Bucket(bucket_name)
    for f in bucket.objects.all():
        # Keys should be keys
        key = f.key
        if bucket_type == 'gcs':
            key = key.replace('+', ' ')

        print('\t'.join((bucket_name, key)))



if __name__ == '__main__':
    main()
