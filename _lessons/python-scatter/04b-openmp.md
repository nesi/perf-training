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

We will use the code in directory `openmp`. Start with
```
cd openmp
```

## Why implement OpenMP parallelisation

One way to speed up your application is using the available resources more efficiently. This approach was used while porting our Python code to C++ by removing the interpreter's overhead. Here we will improve performance by using more resources instead.

Most modern computers have multi-core CPUs, and we can use two or more of these cores to compute instructions in parallel. All cores can access the same, shared memory. We will need to be careful about instructions stepping over each other and undoing or modifying each other's work, the so-called race conditions.

## What is OpenMP

OpenMP (Open Multi-Processing) is an application programming interface (API) for shared memory multiprocessing programming in C, C++ and Fortran.  An OpenMP-parallelised application starts as a serial application that runs on a single compute core. When instructed by the programmer, the application spawns a number of threads, which can be run concurrently on separate cores by the operating system. Thus, work can be distributed to leverage more resources.

Note that the OpenMP standard was recently extended to allow offloading computations to GPUs. However, not all compilers support this feature yet, and there is a similar, competing standard called OpenACC that addresses the same use case. We will limit this lesson to multicore computing without offloading.

### Pros

* supported by a large range of shared memory multicore architectures and accelerators - virtually all modern CPUs have several cores
* uses pragmas (C/C++) or specially formatted comments (Fortran) that can be ignored by non-OpenMP compilers to help code portability and avoid forking code
* can be easier to implement than MPI parallelisation in existing code - a few short directives often suffice to obtain significant speedups
* can be more efficient than MPI as data in memory can be shared between parallel threads
* can be used in combination with other parallelisation methods and APIs, e.g., MPI or CUDA
* does not require a specific runtime environment (unlike, e.g., MPI)

### Cons

* limited to the resources of a single compute node
* not all compilers support OpenMP
* it is easy to create "race conditions" where multiple parallel threads overwrite each other's work, and such errors can be difficult to debug
* can thus be very cumbersome to implement safely in complex cases, as the entire parallel region will need to be inspected carefully for potential race conditions
* some external libraries implement code that is not "thread-safe", which means that these library functions cannot be used by more than one thread in a parallel program, e.g., because of a race condition

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

Parallelisation with OpenMP is implemented using directives, which are written as pragmas (C/C++) or specially formatted comments (Fortran). OpenMP also provides an additional Application Program Interface (API) that allows the programm to configure and query the runtime environment, e.g., to find out how many threads are running in parallel and which thread ID is running a given parallel section. For more information, have a look at the latest [OpenMP standard](https://www.openmp.org/wp-content/uploads/openmp-4.5.pdf).

Here we focus on OpenMP directives in the source code that are interpreted by the compiler. The same source code can be used to build a serial or threaded version of the application by simply turning the OpenMP compiler switch on or off, and a non-OpenMP compiler will ignore the directives as unknown pragmas (C/C++) or as comments (Fortran).

OpenMP directives always start with:
* C/C++: `#pragma omp`
* Fortran (free form): `!$omp`

These are followed by the _directive names_ and _clauses_, controlling parallelisation and data handling. OpenMP directives can consist of multiple statements and can be extended to multiple lines using line continuation statements (Fortran) or `\` (C/C++) at the end of the line.

There are various ways to distribute workloads for parallel execution, the most common being the parallel loop represented below:

[![example-mpi-gather](images/example_omp_threads.png)](images/example_omp_threads.png)

The application always starts in serial mode on a single thread (single arrow at the top). When requested, multiple threads are created/spawned (multiple arrays at the top). In this particular case, the number of threads is 3 (coloured boxes), and each thread performs three iterations (9 iterations altogether). In this simple example, each thread stores its results in separate elements of array `a`, and no additional processing is needed at the end of the parallel region (this would be different if we wanted to, e.g., compute a global sum of all elements of `a` - see the next example). The program then resumes running on a single thread (single arrow at the bottom).

### Data handling
Because OpenMP is based on the shared memory programming model, most variables are shared by default. Other variables like loop index are meant to be private. By private we mean that every thread gets its own copy of the variable - the variable can take a different value for each thread. The programmer determines which variables are private and which are shared.

### Example
In the following, we parallelise a loop computing a sum.
```
#pragma omp parallel for default(none) shared(nc,x,y) reduction(+:res)
for (int i = 0; i < nc - 1; ++i) {
   double arr[2];
   arr[0] = x[i]; arr[1] = y[i];
   res += computeProperty(arr);
}
```
With the `parallel` statement we ask the compiler to spawn threads. The number of threads can be set using environment variable `OMP_NUM_THREADS`: Choosing `export OMP_NUM_THREADS=1` will cause the program to run on a single thread only, while any number above that will result in parallel execution. A useful upper limit is the number of cores on a node, e.g., `export OMP_NUM_THREADS=36`. Note that this does not necessarily mean that your program will run 36 times faster, it can be much less than that (this is what we call "scaling").

The `for` construct specifies that we want to parallelise the `for` loop that immediately follows the pragma. The different iterations of the loop will be then handled by different threads.

It is good practice to always use the `default(none)` clause, which forces us to declare the `shared` or `private` status of each variable that was defined _prior_ to the parallel region. Variables that are defined _inside_ the parallel region, such as the loop index variable `i` or helper variable `arr`, are automatically private; each thread will get its own copy of `i` and `arr`. The same is true for variables that are declared inside functions such as `computeProperty`.

It is generally good practice to define local variables such as `arr` inside the loop where possible. This will make your program easier to read and maintain, and you don't have to worry about creating race conditions by erroneously sharing a variable between threads. If you still need to declare, e.g., `myvariable` outside the loop, add the clause `private(myvariable)` to the OpenMP pragma.

The loop trip count `nc` and data arrays `x` and `y` can be shared as they are not changed inside the loop. Each thread will access the same data in memory, which is very efficient.

Variable `res` is special - it has to store the sum across all loop iterations at the end of the loop, even though the iterations are executed by different threads. So `res` needs to be private to each thread at first and store partial sums. These partial sums need to be collected by the original thread at the end to compute a grand total, which will then be stored in `res` on that thread. The `reduction(+:res)` clause makes sure that the compiler will insert all the required code to accomplish this.

## Exercises

 1. Add OpenMP pragma at line indicated by `// ADD OPENMP PRAGMA HERE` in `src/wave.cpp`

 2. Measure the speedup vs the number of threads (`OMP_NUM_THREADS` values) using problem size `-nx 256 -ny 256 -nc 1024`

