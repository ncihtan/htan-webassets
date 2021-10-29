#!/usr/bin/env bash

backup="outputs/$(date '+%Y-%m-%d_%H%M')"

# Check if archive directory exists, otherwise create it 
if [ ! -d $backup ]
then
    echo "Creating Directory $backup"
    mkdir $backup
fi

# Make a copy 
mv outputs/*.tsv $backup
mv outputs/*.json $backup
mv outputs/*.txt $backup

ls $backup

