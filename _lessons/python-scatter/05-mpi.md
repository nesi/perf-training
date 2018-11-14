---
layout: post
title: MPI parallelism
permalink: /python-scatter/mpi
chapter: python-scatter
---


## Objectives

You will:

* learn how to parallelise code using the message passing interface (MPI)...

We'll use the code in directory `mpi`. Start by
```
cd mpi
```

## What is MPI

MPI is a standard application programming interface for executing programs in parallel. MPI was originally written for C, C++ and Fortran code but implementations have since been written for a variety of other languages including Python. 

MPI programs start a number of processes at the beginning of the program. A process is an instance of an executable that runs typically on a CPU core. As the process runs, the program can exchange data with other processes. An example of data exchanges is point-to-point communication where a process sends data to another process. In other cases data may be "gathered" from processes and sent to a root process. Inversely, data can be scattered from the root process to the other processes.

An example of an MPI program is shown below (left) with the vertical axis indicating time (top to bottom). There are 7 processes: 0=red, 1=yellow, 2=green, 3=magenta, 4=blue, 5=orange and 6=grey. Each process is responsible for computing a few elements in a 4 times 5 matrix (right). The first 3 elements are computed by process 0, the next three elements by process 1, etc. The last process only gets two elements since the number of elements is not divisible by 7. Once the elements of the matrix are computed, a gather operation collects the sub-arrays into a single array on process 6 - this is shown as converging arrows. Neglecting the time it takes to gather the sub-arrays, we can expect the execution time to be reduced from 20 to 3 time units, a speedup of 6.7x, in this case. Perfect speedup 7x is not expected because process 6 has to wait until processes 0-5 finish (load imbalance). Transferring data from processes 0-5 to 6 takes additional time. Hence 6.7x would be the maximum, achievable speedup for this case assuming that the work to compute each matrix element is the same.

In other scenarios, process 0 might communicate with process 1, process 1 with process 2, etc.

[![example-mpi-gather](images/example-mpi-gather.png)](images/example-mpi-gather.png)

### Pros

 * suitable for distributed memory computers, including massively parallel architectures with thousands of cores
 * a viable approach if you don't have enough memory on a node
 * can be used in combination with OpenMP and other parallelisation methods

### Cons

 * there are no serial sections in MPI code and hence MPI programs tend to be written to run in parallel from the beginning to the end

## Running the scatter code using multiple MPI processes

To submit a parallel job on Mahuika, type
```
srun --account="myAccount" --ntasks=4 python scatter.py
```
where "myAccount" is your account on Mahuika (e.g. nesi12345). This will launch a single task with 4 processes.  

To run interactively using 4 processes, type
```
mpiexec -n 4 python scatter.py
```

## How to use MPI to accelerate `scatter.py`

 * At the top: `from mpi4py import MPI`. This will initialise MPI. The number of processes is `nprocs`.
 * Assign a collection of scattered field elements to each MPI process. The process dependent start/end indices into the flat array are `indxBeg` and `indxEnd`. Compute the scattered field for indices `indxBeg` to `indxEnd - 1`.
 * Gather the fields from each process onto root process `nprocs - 1`, see (MPI4PY)[https://info.gwdg.de/~ceulig/docs-dev/doku.php?id=en:services:application_services:high_performance_computing:mpi4py].

## Exercises

 1. Implement the field computation in scatter.py after line `IMPLEMENT FIELD COMPUTATION HERE`.

 2. Implement the field gather operation where all the fields values are assembled onto the root process. This is required for the checksum and save operations to work.

 3. Measure the speedup compared to a single process execution
