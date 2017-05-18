#!/bin/bash
# Copyright 2016 M. Isuru Tharanga Chrishantha Perera
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ----------------------------------------------------------------------------
# Run Benchmarks
# ----------------------------------------------------------------------------

ROOT_DIR=$(dirname "$0")
#JVM Args for main program
JVM_ARGS="-Xms2g -Xmx2g"
#JVM Args for the benchmarks
BM_JVM_ARGS="-Xms1g -Xmx1g"
MODE=""
RESULTS_DIR=""
# Benchmark using Throughput and Sample Modes
BM_MODE="thrpt,sample"
# Default results will be in nanoseconds
TIME_UNIT="ns"

function help {
    echo ""
    echo "Usage: "
    echo "benchmark.sh [options]"
    echo ""
    echo "-t: Benchmark duration. Available options are [quick, medium, long]"
    echo "-r: Results directory"
    echo "-m: Benchmark Mode. Default is $BM_MODE"
    echo "-u: Time Unit. Default is $TIME_UNIT"
    echo ""
}

while getopts "t:r:m:u:" opts
do
  case $opts in
    t)
        MODE=${OPTARG}
        ;;
    r)
        RESULTS_DIR=${OPTARG}
        ;;
    m)
        BM_MODE=${OPTARG}
        ;;
    u)
        TIME_UNIT=${OPTARG}
        ;;
    \?)
        help
        exit 1
        ;;
  esac
done

if [[ ! -f $ROOT_DIR/target/benchmarks.jar  ]]; then
    echo "Please build the benchmark project"
    exit 1
fi

#If no results directory was provided, we need to use the default one
if [[ -z $RESULTS_DIR ]]; then
    RESULTS_DIR=$ROOT_DIR/results
fi

mkdir -p $RESULTS_DIR

#Validate results directory
if [[ ! -d $RESULTS_DIR ]]; then
    echo "Please specify a valid directory to store results"
    exit 1
fi

if [[ "quick" == "$MODE" ]]; then
    forks=1
    warmup_iterations=1
    iterations=1
    threads=(1)
    poolSizes=(10)
elif [[ "medium" == "$MODE" ]]; then
    forks=2
    warmup_iterations=2
    iterations=5
    threads=(1 10)
    poolSizes=(10 50)
elif [[ "long" == "$MODE" ]]; then
    forks=3
    warmup_iterations=5
    iterations=5
    threads=(1 10 20)
    poolSizes=(10 50)
else
    echo "Please specify how long you need to run the benchmarks"
    help
    exit 1
fi

objectpools_benchmark() {
    echo "# Running object pool benchmark. Benchmark Mode: $1 Time Unit: $2 Threads: $3 Pool Size: $4"
    java $JVM_ARGS -jar $ROOT_DIR/target/benchmarks.jar -jvmArgs "$BM_JVM_ARGS" -bm $1 -tu $2 \
        -f $forks -wi $warmup_iterations -i $iterations -t $3 -p poolSize=$4 \
        -rff "$RESULTS_DIR/results-$3-$4.csv" -rf csv -e simple
}

benchmark_iteration=0
# Running benchmarks
total=$((${#threads[@]} * ${#poolSizes[@]}))

run_benchmark() {
    for t in ${threads[@]}
    do
        for p in ${poolSizes[@]}
        do
            objectpools_benchmark $1 $2 $t $p
            benchmark_iteration=$(($benchmark_iteration + 1))
            awk -v i="$benchmark_iteration" -v t="$total" \
                'BEGIN{printf "# Object Pools Benchmark Progress: %.2f%s complete\n", i/t * 100, "%"}'
        done
    done
}

# Run the benchmark
run_benchmark $BM_MODE $TIME_UNIT
