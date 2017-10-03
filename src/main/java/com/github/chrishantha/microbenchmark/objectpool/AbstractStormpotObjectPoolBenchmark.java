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
import org.openjdk.jmh.infra.Blackhole;
import stormpot.Allocator;
import stormpot.Config;
import stormpot.LifecycledPool;
import stormpot.Poolable;
import stormpot.Slot;
import stormpot.Timeout;

import java.util.concurrent.TimeUnit;

/**
 * Benchmark for Stormpot. Code is at https://github.com/chrisvest/stormpot
 */
public abstract class AbstractStormpotObjectPoolBenchmark extends ObjectPoolBenchmark<AbstractStormpotObjectPoolBenchmark.PoolableTestObject> {

    private LifecycledPool<PoolableTestObject> objectPool;

    private final Timeout timeout = new Timeout(2, TimeUnit.MINUTES);

    public static class PoolableTestObject extends TestObject implements Poolable {

        private final Slot slot;

        public PoolableTestObject(Slot slot) {
            super(true);
            this.slot = slot;
        }

        @Override
        public void release() {
            slot.release(this);
        }
    }

    @Override
    public void setupObjectPool() {
        Allocator allocator = new Allocator<PoolableTestObject>() {

            @Override
            public PoolableTestObject allocate(Slot slot) throws Exception {
                return new PoolableTestObject(slot);
            }

            @Override
            public void deallocate(PoolableTestObject poolable) throws Exception {

            }
        };

        Config<PoolableTestObject> config = new Config<PoolableTestObject>().setAllocator(allocator);
        config.setSize(poolSize);
        objectPool = buildPool(config);
    }

    protected abstract LifecycledPool<PoolableTestObject> buildPool(Config<PoolableTestObject> config);

    @Override
    public void tearDownObjectPool() throws Exception {
        objectPool.shutdown().await(timeout);
    }

    @Override
    public PoolableTestObject borrowObject() throws Exception {
        return objectPool.claim(timeout);
    }

    @Override
    public void releaseObject(PoolableTestObject object) throws Exception {
        object.release();
    }

    @Override
    public void useObject(PoolableTestObject object, Blackhole blackhole) {
        blackhole.consume(object.getData());
    }
}
