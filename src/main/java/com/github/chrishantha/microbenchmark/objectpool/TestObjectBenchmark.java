/*
 * Copyright 2016 M. Isuru Tharanga Chrishantha Perera
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.github.chrishantha.microbenchmark.objectpool;

import com.github.chrishantha.microbenchmark.objectpool.object.TestObject;
import org.openjdk.jmh.annotations.Benchmark;
import org.openjdk.jmh.annotations.BenchmarkMode;
import org.openjdk.jmh.annotations.Fork;
import org.openjdk.jmh.annotations.Measurement;
import org.openjdk.jmh.annotations.Mode;
import org.openjdk.jmh.annotations.Threads;
import org.openjdk.jmh.annotations.Warmup;
import org.openjdk.jmh.infra.Blackhole;

/**
 * Benchmark object creation
 */
@BenchmarkMode(Mode.Throughput)
@Warmup(iterations = 5)
@Measurement(iterations = 5)
@Fork(1)
@Threads(10)
public class TestObjectBenchmark {

    @Benchmark
    public void simpleObjectCreate(Blackhole blackhole) {
        TestObject testObject = new TestObject(false);
        blackhole.consume(testObject.getData());
    }

    @Benchmark
    public void expensiveObjectCreate(Blackhole blackhole) {
        TestObject testObject = new TestObject(true);
        // Consume the CPU for same number of tokens as in ObjectPoolBenchmark class
        Blackhole.consumeCPU(1_000L);
        blackhole.consume(testObject.getData());
    }

}
