---
layout: post
title: OpenMP
permalink: /python-scatter/openmp
chapter: python-scatter
---

**Content coming soon**

## Objectives

You will:

* learn how to spawn OpenMP threads
* how to compile OpenMP sources using `setuptools`

We'll use the code in directory `openmp`. Start by
```
cd openmp
```

## Why implement OpenMP parallelization

On way to speed up your application is using the available resources more efficiently. This approach was used while porting our python code to C++ by removing the interpreter's overhead.
Another way of improving performance is by using more resources. Most of modern computers have multi-core CPUs. Each of these cores can in principle compute instructions in parallel. All cores can access the same, shared memory so we will need to be careful about instructions stepping over each other (race condition).

## What is OpenMP

OpenMP (Open Multi-Processing) is an application programming interface (API) for shared memory multiprocessing programming on various platforms in C, C++ and Fortran.  An OpenMP parallelised application starts as a serial application (on a single compute core). When defined by the programmer, the application spawns a number of threads (which run on multiple cores). Thus, work can be distributed to leverage more resources. Just to note, OpenMP can also parallelise on other architectures, like GPUs.

### Pros

* suitable for shared memory architectures and accelerators.
* can be implemented by pragmas and API (see below)
* can be used in combination with other parallelisation methods, e.g. MPI

### Cons

* limited to the resources of one compute node

## How to use OpenMP
To use OpenMP we need to
* instruct the compiler to apply OpenMP threading
* add instruction in the code, specifying where and what to parallelise
* define the amount of threads used during run time

### Compiler switches
OpenMP parallelisation is applied by the compiler and is controlled by the following compiler switches:
* GNU: `-fopenmp`
* Intel: `-qopenmp`
* Cray: OpenMP is enabled by default, use `-noopenmp` to disable OpenMP

### Directives
OpenMP can be implemented using directives or/and the OpenMP Application Program Interface (API). The OpenMP API gives the programmer detailed control and provides extended functionality. Therefore, the programmer needs to refer and link the OpenMP library. For more information have a look at the latest [OpenMP standard](https://www.openmp.org/wp-content/uploads/openmp-4.5.pdf). Here we focus on OpenMP directives.

Directives are comments in the source code, which can be interpreted by the compiler. Thus the same source code can be used to build a serial or threaded version of the application, distinguished by a compiler switch.

The OpenMP directives always start with:
* C/C++: `#pragma omp`
* Fortran (free form): `!$omp`

These are followed by the _directive names_ and _clauses_, controlling parallelization and data handling. OpenMP directives can consist of multiple statements and can also be extended to multiple lines using line continuation statements (C/C++ using '\' at the end of the line).
There are various ways to distribute the workloads. The most common procedure is parallelising a loop. This is schematically presented in the following figure:
[![example-mpi-gather](images/example_omp_threads.png)](images/example_omp_threads.png)
The application always starts in serial. When requested, multiple threads are created/spawned. The number of threads is determined by the environment variable `$OMP_NUM_THREADS`.

### Data handling
Because OpenMP is based upon the shared memory programming model, most variables are shared by default. Other variables like loop index are meant to be private. By private we mean that every thread gets its own copy of the variable - the variable takes can take a different value for each thread. The programer determines which variables are private and which are shared.

### Example
In the following, we parallelise a loop with data mapping and computation.
```
#pragma omp parallel for private(arr) reduction(+:res)
for (int i = 0; i < nc - 1; ++i) {
   arr[0] = x[i]; arr[1] = y[i];
   res += computeProperty(arr);
}
```
With the `parallel` statement we spawn threads. The number of threads is set by the environment variable `OMP_NUM_THREADS`, which can be set to anything from 1 to the number of cores on a nodes, e.g. `export OMP_NUM_THREADS=36`. The `for` loop construct specifies what to parallelise. As a result the different iterations of the loop can be handled by multiple threads. Therefore, each thread gets its own copy of the loop index variable. Arrays `x` and `y` are shared - each thread has access to the same arrays `x` and `y`. Array `arr` is declared as `private` with each thread getting its own copy to prevent race conditions. The sum across iterations is stored in `res`, the value of which must be collected from all thread. This is indicated by the `reduction(+:res)` directive.
