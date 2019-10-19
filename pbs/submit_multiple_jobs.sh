#!/bin/bash
for i_start in {0..999..10}
do
    let "i_end = i_start + 10"
    result_folder=$(printf 'parameter_%04d_%04d/snapshot_%04d/start_%04d' $2 $3 $4 $i_start)
    echo $1, start: $i_start, end: $i_end, defense: $2, attack: $3, output: $result_folder
    qsub -v START=$i_start,END=$i_end,N_DEFENSE=$2,N_ATTACK=$3,SNAPSHOT=$4,RESULT_FOLDER=$result_folder $1
    echo ""
done
