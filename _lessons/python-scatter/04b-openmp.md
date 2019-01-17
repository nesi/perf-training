---
layout: post
title: OpenMP
permalink: /python-scatter/openmp
chapter: python-scatter
---

## Objectives

You will:

* learn how to spawn OpenMP threads in your C/C++ code
* how to compile C/C++ code with OpenMP enabled using `setuptools`

We will use the code in directory `openmp`. Start by
```
cd openmp
```

## Why implement OpenMP parallelisation

One way to speed up your application is using the available resources more efficiently. This approach was used while porting our Python code to C++ by removing the interpreter's overhead. Here we will improve performance by using more resources instead.

Most modern computers have multi-core CPUs and we can use two or more of these cores to execute instructions in parallel. All cores can access the same, shared memory.

## What is OpenMP

OpenMP (Open Multi-Processing) is an application programming interface (API) for shared memory multiprocessing programming in C, C++ and Fortran.  An OpenMP-parallelised application starts as a serial application that runs on a single compute core. When instructed by the programmer, the application spawns a number of threads, which can run concurrently on separate cores. Thus, work can be distributed to leverage more resources.

Note that the OpenMP standard was recently extended to enable offloading computations to GPUs and other accelerators. However, not all compilers support this feature yet and there is a similar, competing standard called OpenACC that addresses the same use case. We will limit this lesson to multicore computing without offloading.

### Pros

* supported by a large range of shared memory multicore architectures (virtually all modern CPUs have several cores) and accelerators
* the same source code can be used to compile in OpenMP and non-OpenMP mode
* can be easier to implement than MPI parallelisation in existing code - a few lines of code may yield significant speedups
* can be more efficient than MPI as data in memory can be shared between multiple threads
* can be used in combination with other parallelisation methods and APIs, e.g., MPI or CUDA

### Cons

* limited to the resources of a single compute node
* spawning threads incurs a small overhead - OpenMP code using one thread runs slower than non-OpenMP code
* it is easy to create "race conditions" where multiple threads overwrite each other's work and such errors can be difficult to debug
* can thus be very cumbersome to implement safely in complex cases, as the entire parallel region will need to be inspected carefully for potential race conditions
* some external libraries implement code that is not "thread-safe", which means that these library functions cannot be used by more than one thread in a parallel program - OpenMP offers ways to deal with such cases, but thread-safety always needs to be verified for each individual library function!

## How to use OpenMP

To use OpenMP we need to
* tell the compiler to apply OpenMP
* add directives to the code, specifying where and what to parallelise
* set the number of threads to be used at run time

### Compiler switches

Use the following compiler switches:
* GNU: `-fopenmp`
* Intel: `-qopenmp`
* Cray: OpenMP is enabled by default, use `-h noomp` to disable OpenMP

### Directives

Parallelisation with OpenMP is implemented using directives, which are written as pragmas (C/C++) or specially formatted comments (Fortran). OpenMP also provides an additional Application Program Interface (API) that allows the program to configure and query the runtime environment, e.g., to find out how many threads are running in parallel and which thread ID is running a given parallel section. For more information, have a look at the latest [OpenMP standard](https://www.openmp.org/wp-content/uploads/openmp-4.5.pdf).

Here we focus on OpenMP directives in the source code that are interpreted by the compiler. The same source code can be used to build a serial or threaded version of the application by simply turning the OpenMP compiler switch on or off, and a non-OpenMP compiler will ignore the directives as unknown pragmas (C/C++) or as comments (Fortran).

OpenMP directives always start with:
* C/C++: `#pragma omp`
* Fortran (free form): `!$omp`

These are followed by the _directive names_ and _clauses_, controlling parallelisation and data handling. OpenMP directives can consist of multiple statements and can be extended to multiple lines using line continuation characters such as `&` (Fortran) or `\` (C/C++) at the end of the line.

There are various ways to distribute workloads for parallel execution, the most common being the parallel loop represented below:

[![example-mpi-gather](images/example_omp_threads.png)](images/example_omp_threads.png)

The application always starts in serial mode on a single thread (single arrow at the top). When requested, multiple threads are created/spawned (multiple arrows at the top). In this particular case, the number of threads is 3 (coloured boxes), and each thread performs three iterations (9 iterations altogether). Results are stored in separate elements of array `a` for each loop index `i`, so we do not create a race condition when the loop is executed in parallel. The program then resumes running on a single thread (single arrow at the bottom).

### Data handling
Because OpenMP is based on the shared memory programming model, most variables are shared by default. Other variables like loop index are meant to be private. By private we mean that the variable can take a different value for each thread. The programmer determines which variables are private and which are shared.

### Example
As an example, we’ll assume that you have to compute the sum of the square of each element of an array.
```cpp
/**
 * Compute the sum an array
 * @param n number of elements
 * @param arr input array
 * @return sum
 */
extern "C"
double mysum(int n, double* arr) {
    double res = 0;
    #pragma omp parallel for default(none) shared(arr) reduction(+:res)
    for (int i = 0; i < n; ++i) {
        // all variables defined inside the loop (here sq) and also index i are private
        double sq = arr[i] * arr[i];
        res += sq;
    }
    return res;
}
```

With the `parallel` statement we ask the compiler to spawn threads. The number of threads can be set using environment variable `OMP_NUM_THREADS`, which can be anything between 1 and the number of cores on a node, e.g., `export OMP_NUM_THREADS=36`.

The `for` construct specifies that we want to parallelise the `for` loop that immediately follows the pragma. The different iterations of the loop will be then handled by different threads.

It is good practice to always use the `default(none)` clause, which forces us to declare the `shared` or `private` status of each variable defined _above_ the parallel region. Variables that are defined _inside_ the parallel region, such as loop index variable `i` or helper variables `sq`, are automatically private. Each thread gets its own copy of `i`, and `sq`.

It is generally good practice to define local variables such as `sq` inside the loop where possible. This will make your program easier to read and maintain and you won't have to worry about creating race conditions by erroneously sharing a variable between threads. If you still need to declare, e.g., `myvariable` outside the loop, add the clause `private(myvariable)` to the OpenMP pragma.

Loop trip count `n` and data arrays `arr` can be shared as they are not changed inside the loop. Each thread will access the same data in memory, which is very efficient.

Variable `res` is special - it has to store the sum across all loop iterations at the end of the loop, even though individual iterations are executed by different threads. So `res` needs to be private to each thread at first and store partial sums. These partial sums then need to be collected by the original thread at the end of the loop to compute a grand total, which will be stored in `res` on that thread. The `reduction(+:res)` clause makes sure that the compiler will insert all required code to accomplish this.

## Exercises

 1. Add OpenMP pragma at line indicated by `// ADD OPENMP PRAGMA HERE` in `src/wave.cpp`. Assume that function `computeScatteredWaveElement` is thread-safe.

 2. Measure the speedup vs the number of threads (`OMP_NUM_THREADS` values) using problem size `-nx 256 -ny 256 -nc 1024`
