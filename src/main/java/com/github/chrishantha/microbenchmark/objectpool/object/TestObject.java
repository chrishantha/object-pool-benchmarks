package com.github.chrishantha.microbenchmark.objectpool.object;

import org.openjdk.jmh.infra.Blackhole;

/**
 * Test Object to be used in Object Pools
 */
public class TestObject {

    private String data = TestObject.class.getName();

    public TestObject(boolean expensive) {
        if (expensive) {
            Blackhole.consumeCPU(10_000L);
            StringBuilder stringBuilder = new StringBuilder();
            for (int i = 0; i < 10_000L; i++) {
                for (int j = '0'; j <= 'z'; j++) {
                    stringBuilder.append((char) j);
                }
            }
            data = stringBuilder.toString();
        }
    }


    public String getData() {
        return data;
    }

}
