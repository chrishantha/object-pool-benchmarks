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

import org.openjdk.jmh.annotations.Benchmark;
import org.openjdk.jmh.annotations.BenchmarkMode;
import org.openjdk.jmh.annotations.CompilerControl;
import org.openjdk.jmh.annotations.Fork;
import org.openjdk.jmh.annotations.Measurement;
import org.openjdk.jmh.annotations.Mode;
import org.openjdk.jmh.annotations.Param;
import org.openjdk.jmh.annotations.Scope;
import org.openjdk.jmh.annotations.Setup;
import org.openjdk.jmh.annotations.State;
import org.openjdk.jmh.annotations.TearDown;
import org.openjdk.jmh.annotations.Threads;
import org.openjdk.jmh.annotations.Warmup;
import org.openjdk.jmh.infra.Blackhole;

@BenchmarkMode(Mode.Throughput)
@Warmup(iterations = 5)
@Measurement(iterations = 5)
@Fork(1)
@Threads(10)
@State(Scope.Benchmark)
public abstract class ObjectPoolBenchmark<T> {

    @Param({"100"})
    protected int poolSize;

    @Setup
    public abstract void setupObjectPool();

    @TearDown
    public abstract void tearDownObjectPool() throws Exception;

    @CompilerControl(CompilerControl.Mode.INLINE)
    protected abstract T borrowObject() throws Exception;

    @CompilerControl(CompilerControl.Mode.INLINE)
    protected abstract void releaseObject(T object) throws Exception;

    @CompilerControl(CompilerControl.Mode.INLINE)
    protected abstract void useObject(T object, Blackhole blackhole);

    @Benchmark
    public void useObject(Blackhole blackhole) throws Exception {
        T object = borrowObject();
        Blackhole.consumeCPU(1_000L);
        useObject(object, blackhole);
        releaseObject(object);
    }

}
