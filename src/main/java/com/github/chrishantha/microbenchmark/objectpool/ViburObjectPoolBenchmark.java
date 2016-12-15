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
import org.vibur.objectpool.ConcurrentPool;
import org.vibur.objectpool.PoolObjectFactory;
import org.vibur.objectpool.util.ConcurrentLinkedQueueCollection;

/**
 * Benchmark for Vibur Object Pool. Code is at https://github.com/vibur/vibur-object-pool/
 */
public class ViburObjectPoolBenchmark extends ObjectPoolBenchmark<TestObject> {

    private ConcurrentPool<TestObject> objectPool;

    @Override
    public void setupObjectPool() {
        objectPool = new ConcurrentPool<>(new ConcurrentLinkedQueueCollection<>(), new PoolObjectFactory<TestObject>() {

            @Override
            public TestObject create() {
                return new TestObject(true);
            }

            @Override
            public boolean readyToTake(TestObject obj) {
                return true;
            }

            @Override
            public boolean readyToRestore(TestObject obj) {
                return true;
            }

            @Override
            public void destroy(TestObject obj) {

            }
        }, 1, poolSize, false);

    }

    @Override
    public void tearDownObjectPool() throws Exception {
        objectPool.close();
    }

    @Override
    public TestObject borrowObject() throws Exception {
        return objectPool.take();
    }

    @Override
    public void releaseObject(TestObject object) throws Exception {
        objectPool.restore(object);
    }

    @Override
    public void useObject(TestObject object, Blackhole blackhole) {
        blackhole.consume(object.getData());
    }
}
