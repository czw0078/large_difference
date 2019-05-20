#!/bin/bash
for i_start in {0..999..10}
do
    let "i_end = i_start + 10"
    echo $1, $i_start, $i_end 
    qsub -v START=$i_start,END=$i_end $1
done
