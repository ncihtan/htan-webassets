NAME=htan-asset-mapping

all: generate mapping combine test

generate:
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
	python generate_bucket_manifest.py \
		-b htan-dcc-ohsu \
		-t aws \
		-p sandbox-developer \
		> outputs/htan-dcc-ohsu-manifest.tsv
	python generate_bucket_manifest.py \
		-b htan-dcc-washu \
		-t gcs \
		-p htan-gcs \
		> outputs/htan-dcc-washu-manifest.tsv
	python generate_synapse_manifest.py \
		-b htan-dcc-vanderbilt \
		-o outputs/htan-dcc-vanderbilt-manifest.tsv

mapping:
	python map_bucket_assets.py \
		-b htan-dcc-ohsu \
		-m outputs/htan-dcc-ohsu-manifest.tsv \
		-a outputs/htan-assets-bucket.tsv \
		--cdn d3p249wtgzkn5u.cloudfront.net \
		> outputs/mapped-assets-ohsu.json
	python map_bucket_assets.py \
		-b htan-dcc-washu \
		-m outputs/htan-dcc-washu-manifest.tsv \
		-a outputs/htan-assets-bucket.tsv \
		--cdn d3p249wtgzkn5u.cloudfront.net \
		> outputs/mapped-assets-washu.json
	python map_bucket_assets.py \
		-b htan-dcc-hms \
		-m outputs/htan-dcc-hms-manifest.tsv \
		-a outputs/htan-assets-bucket.tsv \
		--cdn d3p249wtgzkn5u.cloudfront.net \
		> outputs/mapped-assets-hms.json
	python map_bucket_assets.py \
		-b htan-dcc-vanderbilt \
		-m outputs/htan-dcc-vanderbilt-manifest.tsv \
		-a outputs/htan-assets-bucket.tsv \
		--cdn d3p249wtgzkn5u.cloudfront.net \
		> outputs/mapped-assets-vanderbilt.json

combine:
	python combine_validate_json.py \
		--json-files \
		outputs/mapped-assets-ohsu.json \
		outputs/mapped-assets-hms.json \
		outputs/mapped-assets-washu.json \
		outputs/mapped-assets-vanderbilt.json \
		> outputs/mapped-assets-all-combined.json

test:
	python combine_validate_json.py \
		--test-url-access \
		--json-files \
		outputs/mapped-assets-all-combined.json
clean:
	rm outputs/*.tsv
	rm outputs/*.json

update:
	aws s3 --profile htan-dev-admin cp outputs/mapped-assets-all-combined.json s3://htan-assets/assets-manifest.json

	
