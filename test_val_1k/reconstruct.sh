#!/bin/bash
for n in 0200 0400 0600 0800 1000 1200 1400 1600 1800 2000; do
    echo $n;
    let c=0;
    for each in resize/*; do
        output_filename=$(basename $each);
        ~/go/bin/primitive -i $each -o reconstruct/parameter_$n/$output_filename -n $n -s 299;
        let c++;
        if (( $c % 100 == 0 )); then
            echo generate$c;
        fi
    done
done
