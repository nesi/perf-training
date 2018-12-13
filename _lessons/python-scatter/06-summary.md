---
layout: post
title: Summary
permalink: /python-scatter/summary
chapter: python-scatter
---

## What you have covered

You have learned that the computational efficiency of a program can be influenced by your coding style. A case in point is vectorisation (8x speedup). 

Additional improvements can be achieved by migrating code to C/C++. If the computational kernels are simple enough to be automatically translated to C then `numba` (15x) is an attractive solution. Another factor 2x can be obtained by hand-writing the C/C++ extension (37x total).

Throwing more resources at the problem can reduce wall clock time, but at the expense of higher overall computational cost. For our problem, we obtained a 4x speedup with using multiprocessing (8 threads). Better scalability resulted with MPI (7x for 8
processes). 

The above strategies can be combined. For our test problem, the best results were obtained by applying OpenMP threading to the loops coded in C/C++ (95x). 

![Speedup from applying different strategies](https://github.com/pletzer/perf-training/summary/_lessons/python-scatter/images/speedup.png)


## Other topics not covered here

PROVIDE LIST OF REFERENCES
