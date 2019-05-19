#!/bin/bash

# This script will generate and run inputs for the metrics_cli app to test how much time/memory it uses when running.
# You need to have GNU time installed!

GNU_TIME=/usr/bin/time          # the binary for GNU time, which helps us measure memory and time for a process
CLI_BIN=../metrics_cli.py       # the cli tool to run the benchmarks for
INPUT_GEN=./generate_inputs.py  # our script to generate inputs

TMP_DIR=`mktemp -d`
TIME_OUT=$TMP_DIR/gnu_time.out

INPUT_SIZES="1000 10000 100000 200000 300000 400000 500000" # defines the number of translations in a test
WINDOW_SIZES="10 1000 100000"                               # and the window_sizes to test


for i in $INPUT_SIZES; do
  $INPUT_GEN $i 0.04 > $TMP_DIR/dense_$i.in
done

for i in $INPUT_SIZES; do
  $INPUT_GEN $i 10.0 > $TMP_DIR/sparse_$i.in
done

echo -e "type\t#input\t#window\ttime\tpeakmem"

for test_type in dense sparse; do
  for w in $WINDOW_SIZES; do
    for i in $INPUT_SIZES; do

      # run GNU time, save its output to a temporary file (we have to redirect stdout to /dev/null and stderr to the file)
      $GNU_TIME -v $CLI_BIN --input_file $TMP_DIR/$test_type_$i.in --window_size $w 1>/dev/null 2> $TIME_OUT

      # get the peak memory usage and total user run time for the process from the gnu time output
      PEAK_MEM=`cat $TIME_OUT | grep Maximum | cut -d' ' -f 6`
      USR_TIME=`cat $TIME_OUT | grep User | cut -d' ' -f 4`

      # output the stats for this run
      echo -e "$test_type\t$i\t$w\t$USR_TIME\t$PEAK_MEM"
    done
  done
done

rm -r $TMP_DIR
