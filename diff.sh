#!/usr/bin/env bash
for i in $(ls -d outputs/*/ ); 
do
    latest=${i%%/}; 
done

echo $latest

# Do diff
diff $latest/all-combined-urls-tested.txt outputs/all-combined-urls-tested.txt
