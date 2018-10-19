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
There are various ways to distribute the workloads. The most common procedure is parallelizing a loop.
