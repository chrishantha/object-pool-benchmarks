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
# Benchmark using Throughput and Sample Modes
BM_MODE="thrpt,sample"
# Results will be in milliseconds
TIME_UNIT="ms"

if [[ ! -f $ROOT_DIR/target/benchmarks.jar  ]]; then
    echo "Please build the benchmark project"
    exit 1
fi

RESULTS_DIR=$ROOT_DIR/results
mkdir -p $RESULTS_DIR

forks=2
warmup_iterations=5
warmup_time=1
iterations=5
measurement_time=1
# Threads are in descending order to identify issues quickly
threads=(100 50 10)
# "poolSize" parameter to benchmarks
poolSizes="150,100,50,10"

objectpools_benchmark() {
    echo "# Running object pool benchmark. Benchmark Mode: $BM_MODE Time Unit: $TIME_UNIT Threads: $1 Pool Sizes: $poolSizes"
    java -Xms2g -Xmx2g -jar $ROOT_DIR/target/benchmarks.jar -jvmArgs "-Xms4g -Xmx4g" -bm $BM_MODE -tu $TIME_UNIT \
        -f $forks -wi $warmup_iterations -i $iterations -t $1 -p poolSize=$poolSizes \
        -w $warmup_time -r $measurement_time -v EXTRA -prof gc \
        -rff "$RESULTS_DIR/results-$1-threads.csv" -rf csv -e simple -e SoftReference
}

benchmark_iteration=0
# Running benchmarks
total=${#threads[@]}

for t in ${threads[@]}
do
    objectpools_benchmark $t
    benchmark_iteration=$(($benchmark_iteration + 1))
    awk -v i="$benchmark_iteration" -v t="$total" \
        'BEGIN{printf "# Object Pools Benchmark Progress: %.2f%s complete\n", i/t * 100, "%"}'
done
