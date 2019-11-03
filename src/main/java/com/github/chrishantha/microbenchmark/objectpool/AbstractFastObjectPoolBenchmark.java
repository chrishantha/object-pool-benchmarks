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

import cn.danielw.fop.ObjectFactory;
import cn.danielw.fop.ObjectPool;
import cn.danielw.fop.PoolConfig;
import cn.danielw.fop.Poolable;
import com.github.chrishantha.microbenchmark.objectpool.object.TestObject;
import org.openjdk.jmh.infra.Blackhole;

/**
 * Benchmark for Fast-Object-Pool. Code is at https://github.com/DanielYWoo/fast-object-pool
 */
public abstract class AbstractFastObjectPoolBenchmark extends ObjectPoolBenchmark<Poolable<TestObject>> {

    private ObjectPool<TestObject> objectPool;

    public abstract ObjectPool createPool(PoolConfig config, ObjectFactory<TestObject> factory);

    @Override
    public void setupObjectPool() {
        PoolConfig config = new PoolConfig();
        config.setMaxSize(poolSize);
        objectPool = createPool<>(config, new ObjectFactory<TestObject>() {
            @Override
            public TestObject create() {
                return new TestObject(true);
            }

            @Override
            public void destroy(TestObject o) {
            }

            @Override
            public boolean validate(TestObject o) {
                return true;
            }
        });
    }

    @Override
    public void tearDownObjectPool() throws Exception {
        objectPool.shutdown();
    }

    @Override
    public Poolable<TestObject> borrowObject() throws Exception {
        return objectPool.borrowObject();
    }

    @Override
    public void releaseObject(Poolable<TestObject> object) throws Exception {
        objectPool.returnObject(object);
    }

    @Override
    public void useObject(Poolable<TestObject> object, Blackhole blackhole) {
        blackhole.consume(object.getObject().getData());
    }
}
