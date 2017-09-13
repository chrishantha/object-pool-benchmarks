# Object Pool Benchmarks

This repository has [JMH](http://openjdk.java.net/projects/code-tools/jmh/) benchmarks for different object pool
 implementations.

Following are the object pools used in this project.

* [Commons Pool Generic Object Pool](https://commons.apache.org/proper/commons-pool/api-1.6/org/apache/commons/pool/impl/GenericObjectPool.html)
* [Commons Pool Soft Reference Object Pool](https://commons.apache.org/proper/commons-pool/api-1.6/org/apache/commons/pool/impl/SoftReferenceObjectPool.html)
* [Commons Pool Stack Object Pool](http://commons.apache.org/proper/commons-pool/api-1.6/org/apache/commons/pool/impl/StackObjectPool.html)
* [Commons Pool 2 Generic Object Pool](https://commons.apache.org/proper/commons-pool/apidocs/org/apache/commons/pool2/impl/GenericObjectPool.html)
* [Commons Pool 2 Soft Reference Object Pool](https://commons.apache.org/proper/commons-pool/apidocs/org/apache/commons/pool2/impl/SoftReferenceObjectPool.html)
* [Fast Object Pool](https://github.com/DanielYWoo/fast-object-pool)
* [Furious Object Pool](https://code.google.com/archive/p/furious-objectpool/)
* [Stormpot Blaze Pool](http://chrisvest.github.io/stormpot/)
* [Stormpot Queue Pool](http://chrisvest.github.io/stormpot/performance.html)
* [Vibur Object Pool](http://www.vibur.org/vibur-object-pool/)

## Building the project

Build the benchmarks using Apache Maven

    mvn clean package

## Running the benchmarks

Run the benchmarks using the `benchmark.sh` script.

    ./benchmark.sh

This script will run the benchmarks for different number of threads and different number of object pool sizes.

All parameters are defined using variables in the script. You can change the parameters by editing the script.

The results of the all benchmarks will be saved in `results` directory.

## Plotting Charts from the results

The results from all benchmarks can be visualized using the `create-charts.py` Python script.

The script must be run inside the `results` directory.

    cd results
    ../create-charts.py

## License

Copyright 2016 M. Isuru Tharanga Chrishantha Perera

Licensed under the Apache License, Version 2.0
