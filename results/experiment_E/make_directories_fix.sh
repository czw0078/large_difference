#!/bin/bash
for d in 0200 0400 1600 1800 2000;do
    for s in 1 2 3 4 5;do 
        for st in {0..999..10};do
            mkdir -p ./parameter_$d'_'$d/snapshot_000$s/start_$(printf '%04d' $st)
        done
    done
done
