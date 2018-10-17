---
layout: post
title: MPI parallelism
permalink: /python-scatter/mpi
chapter: python-scatter
---


## Objectives

You will:

* how to parallelise code using the message passing interface (MPI)...

We'll use the code in directory `mpi`. Start by
```
cd mpi
```

## What is MPI

MPI is a programming application interface which supports message passing between processes in C, C++ and Fortran. MPI implentations mimicking the C/C++ and Fortran interfaces exist for a variety of languages including Python. 

A process is an instance of an executable that runs typically on a core but may map to CPUs or nodes. As the process runs, there methods to exchange data with other processes, to 
gather data from other processes onto a root process and to scatter data from one process to other processes.

An example of an MPI program is shown below (left) with the vertical axis indicating time (top to bottom). There are 7 processes: 0=red, 1=yellow, 2=green, 3=magenta, 4=blue, 5=orange and 6=grey. Each process computes an element in a 4 times 5 matrix (right). The first 3 elements are attached to process 0, the next three elements to process 1, etc. The last process only gets two elements since the number of elements is not divisible by 7. Once the elements of the matrix are computed, a gather operation collects the sub-arrays into a single array on process 6 (converging arrows). Neglecting the time it takes to gather the sub-arrays, the execution time is reduced from 20 to 3 time units, a speedup of 6.7x, in this case. The reason we did not get perfect speedup 7x is because process 6 has to wait until processes 0-5 finish (load imbalance). Transferring data from processes 0-5 to 6 takes additional time. Hence 6.7x is the maximum, achievable speedup assuming that the work to compute each element is the same. 

In other scenarios, process 0 might communicate with process 1, process 1 with process 2, etc. 

[![example-mpi-gather](images/example-mpi-gather.png)](images/example-mpi-gather.png)

### Pros

 * suitable for distributed memory computers, including massively parallel architectures
 * viable approach if you don't have enough memory on a node
 * can be used in combination with OpenMP and other acceleration methods

### Cons

 * processes start at the begginning of the execution and terminate at the end, hence there are no serial sections in MPI code

## Example how MPI works


## Exercises

 1. 
 2. 


