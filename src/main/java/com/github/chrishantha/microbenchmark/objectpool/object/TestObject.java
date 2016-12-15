package com.github.chrishantha.microbenchmark.objectpool.object;

/**
 * Test Object to be used in Object Pools
 */
public class TestObject {

    private final String data;

    private final long number;

    public TestObject(boolean expensive) {
        if (expensive) {
            long sum = 0;
            StringBuilder stringBuilder = new StringBuilder();
            for (int i = 0; i < 100; i++) {
                for (int j = '0'; j <= 'z'; j++) {
                    stringBuilder.append((char) j);
                    sum += j;
                }
            }
            data = stringBuilder.toString();
            number = sum;
        } else {
            data = "Test123";
            number = 16;
        }
    }


    public String getData() {
        return data;
    }

    public long getNumber() {
        return number;
    }

}
