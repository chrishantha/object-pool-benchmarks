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

JVM_ARGS="-Xms1g -Xmx1g"
MODE=""
RESULTS_DIR=""

function help {
    echo ""
    echo "Usage: "
    echo "benchmark.sh [options]"
    echo ""
    echo "-t: Benchmark duration. Available options are [quick, medium, long]"
    echo "-r: Results directory"
    echo ""
}

while getopts "t:r:" opts
do
  case $opts in
    t)
        MODE=${OPTARG}
        ;;
    r)
        RESULTS_DIR=${OPTARG}
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

#Validate java directory
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
    forks=5
    warmup_iterations=10
    iterations=10
    threads=(1 10 50 100)
    poolSizes=(10 50 100)
else
    echo "Please specify how long you need to run the benchmarks"
    help
    exit 1
fi

objectpools_benchmark() {
    echo "# Running object pool benchmark. Benchmark Mode: $1 Threads: $2 Pool Size: $3 Time Unit: $4"
    java -jar $ROOT_DIR/target/benchmarks.jar -jvmArgs "$JVM_ARGS" -bm $1 \
        -f $forks -wi $warmup_iterations -i $iterations -t $2 -p poolSize=$3 -tu $4 \
        -rff "$RESULTS_DIR/results-$1-$2-$3.csv" -rf csv -e simple
}

benchmark_iteration=0
# Running benchmarks for two modes
total=$((${#threads[@]} * ${#poolSizes[@]} * 2))

run_benchmark() {
    for t in ${threads[@]}
    do
        for p in ${poolSizes[@]}
        do
            objectpools_benchmark $1 $t $p $2
            benchmark_iteration=$(($benchmark_iteration + 1))
            awk -v i="$benchmark_iteration" -v t="$total" \
                'BEGIN{printf "# Object Pools Benchmark Progress: %.2f%s complete\n", i/t * 100, "%"}'
        done
    done
}

# Benchmark using Throughput Mode with results in seconds
run_benchmark thrpt s
# Benchmark using Sample Mode with results in nanoseconds
run_benchmark sample ns
