python generate_bucket_manifest.py -b htan-imaging-example-datasets -t aws -p htan-dev-admin > outputs/htan-imaging-example-datasets-manifest.tsv
python map_bucket_assets.py -b htan-dcc-ohsu -m outputs/htan-dcc-ohsu-manifest.tsv -a outputs/htan-imaging-example-datasets-manifest.tsv > outputs/assets-ohsu.json
python combine_validate_json.py --json-files outputs/assets-ohsu.json outputs/assets-hms.json outputs/assets-washu.json
