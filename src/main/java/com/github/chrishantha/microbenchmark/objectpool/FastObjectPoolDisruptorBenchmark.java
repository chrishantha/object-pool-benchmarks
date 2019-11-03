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
import cn.danielw.fop.DisruptorObjectPool;
import cn.danielw.fop.PoolConfig;
import com.github.chrishantha.microbenchmark.objectpool.object.TestObject;

/**
 * Benchmark for Fast-Object-Pool. Code is at https://github.com/DanielYWoo/fast-object-pool
 */
public class FastObjectPoolDisruptorBenchmark extends AbstractFastObjectPoolBenchmark {

    public ObjectPool createPool(PoolConfig config, ObjectFactory<TestObject> factory) {
        return new DisruptorObjectPool<>(config, factory);
    }
}
