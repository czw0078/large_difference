#!/bin/bash
for d in 0000;do
    for a in 0000;do
        for s in 1;do 
            for st in {0..999..10};do
                mkdir -p ./parameter_$d'_'$a/snapshot_000$s/start_$(printf '%04d' $st)
            done
        done
    done
done
