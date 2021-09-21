# Generate S3/GS manifests
python generate_bucket_manifest.py -b htan-assets -t aws -p htan-dev-admin > outputs/htan-assets-bucket.tsv

python generate_bucket_manifest.py -b htan-dcc-hms -t aws -p htan-dev-admin > outputs/htan-dcc-hms-manifest.tsv
python generate_bucket_manifest.py -b htan-dcc-ohsu -t aws -p htan-dev-admin > outputs/htan-dcc-ohsu-manifest.tsv
python generate_bucket_manifest.py -b htan-dcc-washu -t gcs -p htan-gcs > outputs/htan-dcc-washu-manifest.tsv


# Map Source Buckets to assets

python map_bucket_assets.py -b htan-dcc-ohsu -m outputs/htan-dcc-ohsu-manifest.tsv -a outputs/htan-assets-bucket.tsv --cdn d3p249wtgzkn5u.cloudfront.net > outputs/assets-ohsu.json
python map_bucket_assets.py -b htan-dcc-washu -m outputs/htan-dcc-washu-manifest.tsv -a outputs/htan-assets-bucket.tsv --cdn d3p249wtgzkn5u.cloudfront.net > outputs/assets-washu.json
python map_bucket_assets.py -b htan-dcc-hms -m outputs/htan-dcc-hms-manifest.tsv -a outputs/htan-assets-bucket.tsv --cdn d3p249wtgzkn5u.cloudfront.net > outputs/assets-hms.json


# Combine & test all asset urls

python combine_validate_json.py --json-files outputs/assets-ohsu.json outputs/assets-hms.json outputs/assets-washu.json --test-url-access

python combine_validate_json.py --json-files outputs/assets-ohsu.json outputs/assets-hms.json outputs/assets-washu.json > outputs/assets-manifest-combined-hms-ohsu-washu-210921.json
