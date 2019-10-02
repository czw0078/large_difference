#!/bin/bash

p4=2

p2=200
p3=200
# for i_start in 230 340
for i_start in 650 780 840 990
do
    let "i_end = i_start + 10"
    result_folder=$(printf 'parameter_%04d_%04d/snapshot_%04d/start_%04d' $p2 $p3 $p4 $i_start)
    echo $1, start: $i_start, end: $i_end, defense: $p2, attack: $p3, snapshot: $p4, output: $result_folder
    qsub -v START=$i_start,END=$i_end,N_DEFENSE=$p2,N_ATTACK=$p3,SNAPSHOT=$p4,RESULT_FOLDER=$result_folder $1
    echo ""
done

p2=400
p3=400
for i_start in 450 530
do
    let "i_end = i_start + 10"
    result_folder=$(printf 'parameter_%04d_%04d/snapshot_%04d/start_%04d' $p2 $p3 $p4 $i_start)
    echo $1, start: $i_start, end: $i_end, defense: $p2, attack: $p3, snapshot: $p4, output: $result_folder
    qsub -v START=$i_start,END=$i_end,N_DEFENSE=$p2,N_ATTACK=$p3,SNAPSHOT=$p4,RESULT_FOLDER=$result_folder $1
    echo ""
done

p2=600
p3=600
for i_start in 570 590 690 970
do
    let "i_end = i_start + 10"
    result_folder=$(printf 'parameter_%04d_%04d/snapshot_%04d/start_%04d' $p2 $p3 $p4 $i_start)
    echo $1, start: $i_start, end: $i_end, defense: $p2, attack: $p3, snapshot: $p4, output: $result_folder
    qsub -v START=$i_start,END=$i_end,N_DEFENSE=$p2,N_ATTACK=$p3,SNAPSHOT=$p4,RESULT_FOLDER=$result_folder $1
    echo ""
done

p2=1200
p3=1200
for i_start in 160 400 430 550 700
do
    let "i_end = i_start + 10"
    result_folder=$(printf 'parameter_%04d_%04d/snapshot_%04d/start_%04d' $p2 $p3 $p4 $i_start)
    echo $1, start: $i_start, end: $i_end, defense: $p2, attack: $p3, snapshot: $p4, output: $result_folder
    qsub -v START=$i_start,END=$i_end,N_DEFENSE=$p2,N_ATTACK=$p3,SNAPSHOT=$p4,RESULT_FOLDER=$result_folder $1
    echo ""
done

p2=1400
p3=1400
for i_start in 170 190 350 840 950
do
    let "i_end = i_start + 10"
    result_folder=$(printf 'parameter_%04d_%04d/snapshot_%04d/start_%04d' $p2 $p3 $p4 $i_start)
    echo $1, start: $i_start, end: $i_end, defense: $p2, attack: $p3, snapshot: $p4, output: $result_folder
    qsub -v START=$i_start,END=$i_end,N_DEFENSE=$p2,N_ATTACK=$p3,SNAPSHOT=$p4,RESULT_FOLDER=$result_folder $1
    echo ""
done


p2=1600
p3=1600
for i_start in 300 730 820
do
    let "i_end = i_start + 10"
    result_folder=$(printf 'parameter_%04d_%04d/snapshot_%04d/start_%04d' $p2 $p3 $p4 $i_start)
    echo $1, start: $i_start, end: $i_end, defense: $p2, attack: $p3, snapshot: $p4, output: $result_folder
    qsub -v START=$i_start,END=$i_end,N_DEFENSE=$p2,N_ATTACK=$p3,SNAPSHOT=$p4,RESULT_FOLDER=$result_folder $1
    echo ""
done

p2=1800
p3=1800
for i_start in 410 420 430 440 450 460 470 480 490 500 510 520 530 540 550 560 570 580 590 600 940
do
    let "i_end = i_start + 10"
    result_folder=$(printf 'parameter_%04d_%04d/snapshot_%04d/start_%04d' $p2 $p3 $p4 $i_start)
    echo $1, start: $i_start, end: $i_end, defense: $p2, attack: $p3, snapshot: $p4, output: $result_folder
    qsub -v START=$i_start,END=$i_end,N_DEFENSE=$p2,N_ATTACK=$p3,SNAPSHOT=$p4,RESULT_FOLDER=$result_folder $1
    echo ""
done

p2=2000
p3=2000
for i_start in 10 170 180 330 380
do
    let "i_end = i_start + 10"
    result_folder=$(printf 'parameter_%04d_%04d/snapshot_%04d/start_%04d' $p2 $p3 $p4 $i_start)
    echo $1, start: $i_start, end: $i_end, defense: $p2, attack: $p3, snapshot: $p4, output: $result_folder
    qsub -v START=$i_start,END=$i_end,N_DEFENSE=$p2,N_ATTACK=$p3,SNAPSHOT=$p4,RESULT_FOLDER=$result_folder $1
    echo ""
done

