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

if [[ ! -f $ROOT_DIR/target/benchmarks.jar  ]]; then
    echo "Please build the benchmark project"
    exit 1
fi


RESULTS_DIR=$ROOT_DIR/results
mkdir -p $RESULTS_DIR

forks=3
warmup_iterations=5
iterations=5
threads=(1 10 20)
poolSizes=(10 50)

objectpools_benchmark() {
    # Benchmark using Throughput and Sample Modes
    BM_MODE="thrpt,sample"
    # Results will be in milliseconds
    TIME_UNIT="ms"
    echo "# Running object pool benchmark. Benchmark Mode: $BM_MODE Time Unit: $TIME_UNIT Threads: $1 Pool Size: $2"
    java -Xms1g -Xmx1g -jar $ROOT_DIR/target/benchmarks.jar -jvmArgs "-Xms1g -Xmx1g" -bm $BM_MODE -tu $TIME_UNIT \
        -f $forks -wi $warmup_iterations -i $iterations -t $1 -p poolSize=$2 \
        -rff "$RESULTS_DIR/results-$1-threads-with-pool-size-$2.csv" -rf csv -e simple
}

benchmark_iteration=0
# Running benchmarks
total=$((${#threads[@]} * ${#poolSizes[@]}))

for t in ${threads[@]}
do
    for p in ${poolSizes[@]}
    do
        objectpools_benchmark $t $p
        benchmark_iteration=$(($benchmark_iteration + 1))
        awk -v i="$benchmark_iteration" -v t="$total" \
            'BEGIN{printf "# Object Pools Benchmark Progress: %.2f%s complete\n", i/t * 100, "%"}'
    done
done
