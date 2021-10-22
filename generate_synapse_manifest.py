import os
import argparse

import synapseclient
import synapseutils
from synapseclient import EntityViewType

"""
Walking through synapse at the root level causes some performance instabilities. Maybe cause the walk function to hang in some cases.

Use the synId of the datatype instead.
e.g. 'h_and_e_level_1'
"""

# Login to Synapse
syn = synapseclient.Synapse()
syn.login()  # Read from .synapseConfig authtoken=<PAT>

# Reference synapseIds, Entity keys
ENTITY_KEYS = ['properties', 'annotations', 'path', 'cacheDir', 'files', 'synapseStore', '_file_handle']

CENTERS = {
    'htan-dcc-vanderbilt': {
        'h_and_e_level_1': 'syn25054230',  # h_and_e
    }
}

def manifest_from_sync(syn, entity):
    entities = synapseutils.sync.syncFromSynapse(syn, entity, downloadFile=False)

    for f in entities:
        d = f.__dict__.keys()
        print(f.name)

def manifest_from_walk(syn, root_synId):
    walkedPath = synapseutils.walk(syn, root_synId)
    for dirpath, dirname, files in walkedPath:
        path, id = dirpath
        for f in files:
            filename, synId = f
            print(os.path.join(path, filename))


def process_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-b', '--bucket', required=True)
    parser.add_argument('-o', '--out-file', required=True)
    args = parser.parse_args()
    return args

def main():
    args = process_args()
    bucket = args.bucket
    outfile = args.out_file

    # Given an entity, grab all children entities via walk()
    records = []
    for datatype, synId in CENTERS.get(bucket).items():
        for dirpath, dirname, files in synapseutils.walk(syn, synId):
            path, id = dirpath
            for f in files:
                filename, synId = f
                s3Key = os.path.join(path, filename)
                output = f'{bucket}\t{s3Key}\n'
                records.append(output)

    with open(outfile, 'w') as fh:
        fh.writelines(records)


if __name__ == '__main__':
    main()
