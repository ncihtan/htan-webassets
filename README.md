# HTAN web assets
Using the DCC source bucket, find available public webassets and create valid CDN backed urls.

### Steps
1. Generate manifest file for the htan-assets bucket and also one manifest file per DCC center source buckets.
2. Create a mapping file for each `DCC manifest` to the `asset manifest`
3. Combine all mapping `<center>` => `<asset>` files into one
4. Test CDN urls
5. Push update back to bucket

## Options
```
make all [generate, mapping, combine, test] # Run all the steps
make [generate, mapping, combine, test, clean, update] # Options
```

## Example usage
1. Generate manifest files for each DCC. 
    - You need to generate atleast one manifest for the htan-assets bucket (thumbnails, minerva stories). 
    - And one DCC `bucket`
```
make generate
-- OR --
python generate_bucket_manifest.py \
    -b htan-assets \
    -t aws \
    -p htan-dev-admin \
    > outputs/htan-assets-bucket.tsv
python generate_bucket_manifest.py \
    -b htan-dcc-hms \
    -t aws \
    -p sandbox-developer \
    > outputs/htan-dcc-hms-manifest.tsv
```
2. Map the DCC `bucket` manifest against the htan-assets `bucket` manifest.
```
make mapping
-- OR --
python map_bucket_assets.py \
    -b htan-dcc-ohsu \
    -m outputs/htan-dcc-ohsu-manifest.tsv \
    -a outputs/htan-assets-bucket.tsv \
    --cdn d3p249wtgzkn5u.cloudfront.net \
    > outputs/mapped-assets-ohsu.json
```
3. Combine mapping files
```
make combine
-- OR --
python combine_validate_json.py \
    --json-files \
    outputs/mapped-assets-ohsu.json \
    outputs/mapped-assets-hms.json \
    outputs/mapped-assets-washu.json \
    outputs/mapped-assets-vanderbilt.json \
    > outputs/mapped-assets-all-combined.json
```
4. Test urls
```
make test
-- OR --
python combine_validate_json.py \
    --test-url-access \
    --json-files \
    outputs/mapped-assets-all-combined.json
```

5. Push mapping file to htan-assets bucket
```
make update
-- OR --
aws s3 --profile <AWS_PROFILE> cp outputs/mapped-assets-all-combined.json s3://htan-assets/assets-manifest.json
```

