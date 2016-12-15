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
import org.apache.commons.pool2.BasePooledObjectFactory;
import org.apache.commons.pool2.PooledObject;
import org.apache.commons.pool2.impl.DefaultPooledObject;
import org.apache.commons.pool2.impl.SoftReferenceObjectPool;
import org.openjdk.jmh.infra.Blackhole;

/**
 * Benchmark for {@link SoftReferenceObjectPool} in Apache Commons Pool2
 */
public class CommonsPool2SoftReferenceObjectPoolBenchmark extends ObjectPoolBenchmark<TestObject> {

    private SoftReferenceObjectPool<TestObject> objectPool;

    @Override
    public void setupObjectPool() {
        objectPool = new SoftReferenceObjectPool<>(new BasePooledObjectFactory<TestObject>() {
            @Override
            public TestObject create() throws Exception {
                return new TestObject(true);
            }

            @Override
            public PooledObject<TestObject> wrap(TestObject testObject) {
                return new DefaultPooledObject<>(testObject);
            }
        });
    }

    @Override
    public void tearDownObjectPool() throws Exception {
        objectPool.close();
    }

    @Override
    public TestObject borrowObject() throws Exception {
        return objectPool.borrowObject();
    }

    @Override
    public void releaseObject(TestObject object) throws Exception {
        objectPool.returnObject(object);
    }

    @Override
    public void useObject(TestObject object, Blackhole blackhole) {
        blackhole.consume(object.getData());
    }
}
