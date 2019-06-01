#!/bin/bash
for d in 0600 0800 1000 1200 1400;do
    for a in 0600 0800 1000 1200 1400;do
        for s in 1 2 3 4 5;do 
            for st in {0..999..10};do
                mkdir -p ./parameter_$d'_'$a/snapshot_000$s/start_$(printf '%04d' $st)
            done
        done
    done
done
