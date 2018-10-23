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

On way to speed up your application is using the available resources more efficiently. This approach we used while porting our python code to C++. This reduced the numerical overhead.
Another way of improving the performance is using more resources to compute our tasks. Most of modern computers have multi-core CPUs. Each of these cores can compute instructions. All of them can access the shared memory.

## What is OpenMP

OpenMP (Open Multi-Processing) is an application programming interface (API) for shared memory multiprocessing programming on various platforms in C, C++ and Fortran.  An OpenMP parallelized application starts as a serial application (on a single compute core). When defined by the programmer, the application spawns a certain amount of threads (which run on multiple cores). Thus, work can be distributed to a larger amount of resources. Just to note, OpenMP is also capable to parallelize on other architectures, like GPUs.

### Pros

* suitable for shared memory architectures and accelerators.
* can be implemented by pragmas and API  (see below)
* can be used in combination with other parallelisation methods, e.g. MPI

### Cons

* limited to the resources of one compute node

## How to use OpenMP
To use OpenMP we need to
* instruct the compiler to apply OMP threading
* add instruction in the code, specifying where and what to parallelise
* define the amount of threads used during run time

### Compiler switches
OpenMP parallelisation is applied by the compiler, controlled using following compiler switched:
* GNU: `-fopenmp`
* Intel: `-qopenmp`
* Cray: enabled by default, use `-noopenmp` to disable OpenMP

### Directives
OpenMP can be implemented using directives or/and the OpenMP Application Program Interface (API). The OpenMP API allows the programmer detailed control and provides extended functionality. Therefore, the programmer needs to refer and link the OpenMP library. For more information have a look to the latest [OpenMP standard](https://www.openmp.org/wp-content/uploads/openmp-4.5.pdf). Here we focus on OpenMP directives.

Directives are comments in the source code, which can be interpreted by the compiler. Thus the same source code can be used to build a serial or threaded version of the application, distinguished by a compiler switch.

The OpenMP directives always start with:
* C/C++: `#pragma omp`
* Fortran (free form): `!$omp`

These are followed by the _directive name_ and _clauses_, controlling parallelization and data handling. OpenMP directives can consist of multiple statements and can also be extended to multiple lines using line continuation statements.
There are various ways to distribute the workloads. The most common procedure is parallelizing a loop to a bunch of threads. This is schematically presented in the following figure:
[![example-mpi-gather](images/example_omp_threads.png)](images/example_omp_threads.png)
The application always starts as serial, the so called Master Thread. When requested, multiple threads are created/spawned. The amount of threads is determined by the environment variable `$OMP_NUM_THREADS`.

### Data handling
Because OpenMP is based upon the shared memory programming model, most variables are shared by default. Other variables like loop index are meant to be private. Thus every thread can have its own copy with a different value.
These data scoping can be defined/corrected by the programmer.  

### Example
In the following, we parallelise a loop with data mapping and computation.
```
#pragma omp parallel for private(arr) reduction(+:res)
for (int i = 0; i < nc - 1; ++i) {
   arr[0] = x[i]; arr[1] = y[i];
   res += computeProperty(arr);
}
```
With the `parallel` statment we spawn threads. The `for` loop construct specifies what to parallelise. As a result the different iterations of the loop can be handled by multiple threads. Therefore, each thread gets its own copy of the loop index variable. The arrays `x` and `y` are shared, thus all threads act (here only read) on the same memory. The data clause of the array `arr` needs to be defined as `private` thus each thread gets its own copy and race conditions are prevented. Furthermore, the values of `res` is meant to sum values of all iterations. Therefore, it needs to be collected from all threads. This operation is instructed using the `reduction(+:res)` directive, specifying the operation and the variables. 
