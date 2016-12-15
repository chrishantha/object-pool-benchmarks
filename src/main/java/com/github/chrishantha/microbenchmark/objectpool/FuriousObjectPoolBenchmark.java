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
import nf.fr.eraasoft.pool.ObjectPool;
import nf.fr.eraasoft.pool.PoolException;
import nf.fr.eraasoft.pool.PoolSettings;
import nf.fr.eraasoft.pool.PoolableObjectBase;
import nf.fr.eraasoft.pool.impl.PoolControler;
import org.openjdk.jmh.infra.Blackhole;

/**
 * Benchmark for Furious-Object-Pool. Code is at https://code.google.com/archive/p/furious-objectpool/
 */
public class FuriousObjectPoolBenchmark extends ObjectPoolBenchmark<TestObject> {

    private ObjectPool<TestObject> objectPool;

    @Override
    public void setupObjectPool() {
        PoolSettings<TestObject> settings = new PoolSettings<>(new PoolableObjectBase<TestObject>() {
            @Override
            public TestObject make() throws PoolException {
                return new TestObject(true);
            }

            @Override
            public void activate(TestObject testObject) throws PoolException {

            }
        });
        settings.min(0).max(poolSize);
        objectPool = settings.pool();
    }

    @Override
    public void tearDownObjectPool() throws Exception {
        PoolControler.shutdown();
    }

    @Override
    public TestObject borrowObject() throws Exception {
        return objectPool.getObj();
    }

    @Override
    public void releaseObject(TestObject object) throws Exception {
        objectPool.returnObj(object);
    }

    @Override
    public void useObject(TestObject object, Blackhole blackhole) {
        blackhole.consume(object.getData());
    }
}
