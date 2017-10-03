package com.github.chrishantha.microbenchmark.objectpool.object;

import org.openjdk.jmh.infra.Blackhole;

/**
 * Test Object to be used in Object Pools
 */
public class TestObject {

    private final String data = TestObject.class.getName();

    public TestObject(boolean expensive) {
        if (expensive) {
            Blackhole.consumeCPU(10_000L);
        }
    }


    public String getData() {
        return data;
    }

}
