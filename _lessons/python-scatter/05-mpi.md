---
layout: post
title: MPI parallelism
permalink: /python-scatter/mpi
chapter: python-scatter
---


## Objectives

You will:

* learn how to parallelise code using the message passing interface (MPI)

We'll use the code in directory `mpi`. Start by
```
cd mpi
```

## What is MPI

MPI is a standard application programming interface for creating and executing parallel programs. MPI was originally written for C, C++ and Fortran code but implementations have since become available for a variety of other languages, including Python.

MPI programs start a number of processes at the beginning of the program. A process is an instance of an executable that runs concurrently with other processes.

As the process runs, the program may need to exchange data ("messages" - hence the name) with other processes. An example of data exchanges is point-to-point communication where one process sends data to another process. In other cases data may be "gathered" from multiple processes at once and sent to a root process. Inversely, data can be "scattered" from the root process to multiple other processes in one step.

### Pros

 * suitable for distributed memory computers, including supercomputers with thousands or hundreds of thousands of cores
 * thus overcomes resource limitations of shared memory approaches like OpenMP, e.g., if you don't have enough memory on a node
 * can be used in combination with OpenMP and other parallelisation methods

### Cons

 * there are no serial sections in MPI code and hence MPI programs need to be written to run in parallel from the beginning to the end
 * many algorithms are difficult to implement efficiently with MPI due its distributed memory approach and communication overheads
 * MPI parallelisation can therefore require redesign of code and algorithms
 * running MPI programs requires a runtime environment, which can be difficult to set up for inexperienced users
 * it is easy to create "dead locks" where one or more processes get stuck waiting for a message

## An example of MPI work load distribution

Say we need to compute the elements of a 4x5 array, shown below on the right, and the computation of each matrix element is very costly. We have 7 processes available for this task, shown on the left. 

In order to reduce the execution time of the program, we may decide to distribute the work between processes. Each (colour coded) process will compute a few elements in the matrix. For instance, process 0 (red) will compute the first three elements, process 1 (yellow) the next three elements, etc. until process 6 (grey) which will be computing the remaining two elements. Once the elements of the matrix are computed, a gather operation collects the results into a single array on process 6 - this is shown as converging arrows.

Neglecting the time it takes to gather the results, we can expect the execution time to be reduced from 20 (number of matrix elements) to 3 time units (maximum number of elements handled by a process). We get a speedup of 6.7x in this case. The ideal speedup is 7x but this cannot happen because process 6 has to wait until processes 0-5 finish. This is known as a *load balancing* problem, that is processes may take different amounts of time to a complete a parallel task, causing some processes to stall (dashed line). Naturally, we should always strive to assign the same amount of work to each process.   

Transferring data from processes 0-5 to 6 takes additional time. Hence 6.7x would be the maximum, achievable speedup for this case assuming that the work to compute each matrix element is the same.


[![example-mpi-gather](images/example-mpi-gather.png)](images/example-mpi-gather.png)

We will now implement the example using the `mpi4py` package in Python.

```python
from mpi4py import MPI
import numpy

# default communicator - grab all processes
comm = MPI.COMM_WORLD

# number of processes
nprocs = comm.Get_size()

# identiy of this process
pe = comm.Get_rank()

# special process responsible for administrative work
root = nprocs - 1

# global 2d array sizes
n0 = 4
n1 = 5

# total number of elements
ntot = n0 * n1

# get the start/end indices for each proc
n = int(numpy.ceil(ntot / float(nprocs)))
indxBeg = n * pe
indxEnd = min(n*(pe + 1), ntot)

# local number of elements
nLocal =  indxEnd - indxBeg

# allocate and set local array to the process rank
array = pe * numpy.ones((nLocal,), numpy.float64)

# gather all local arrays on process root
results_list = comm.gather(array, root=root)

if pe == root:
  results = numpy.concatenate(results_list).reshape((n0, n1))
  print(results)
```

We first need to get a "communicator" - this is our communication interface that allows us to exchange data with other MPI processes. `COMM_WORLD` is the default communicator that includes all the processes we launch, and we will use that in this simple example.

We can now ask our communicator how many MPI processes are running using the `Get_size()` method. The `Get_rank()` method returns the rank (a process number between 0 and `nprocs`) and stores the value in `pe`. Keep in mind that `pe` is the only differentiating factor between this and other MPI processes. Our program then needs to make decisions based on `pe`, to decide for instance on which subset of the data to operate on.

The process with rank `nprocs - 1` is earmarked here as "root". The root process often does administrative work, such as gathering results from other processes, as shown in the diagram above. We are free to choose any MPI rank as root.

Now each process works on its own, local `array`, which is smaller than the actual array as it contains only the data assigned to a given process. For good load balancing, we like the local array to have the same size across all processes so we allocate size `n` to each local array, except for the last process which gets the remaining number of elements. 

Each process then performs work on global index range `indxBeg` to `indxEnd` of the data. In this simple example, the data are set to `pe` but in more complex situations we should expect the data to depend on `indxBeg` and `indxEnd`.

To gather all results on `root`, we now call MPI's `gather` method on every process, hand over the different contributions, and tell MPI which rank we have chosen as root.

The last thing to do is to look at the results. It is very important to realise that variable `results_list` only contains data on our `root` rank and nowhere else (it will be set to `None` on all other processes). We therefore add an `if` statement to make sure that `concatenate` and `print` are only executed on our root process.

## Running the scatter code using multiple MPI processes


### On Mahuika

Type
```
srun --ntasks=4 python scatter.py
```
(with additional `srun` options such as `--account=` required). This will request 4 processes.  

### Interactive parallel execution 

To run interactively using 4 processes, type
```
mpiexec -n 4 python scatter.py
```

## How to use MPI to accelerate `scatter.py`

 * At the top: `from mpi4py import MPI`. This will initialise MPI. The number of processes is `nprocs`.
 * Assign a collection of scattered field elements to each MPI process. The process dependent start/end indices into the flat array are `indxBeg` and `indxEnd`. Compute the scattered field for indices `indxBeg` to `indxEnd - 1`.
 * Gather the fields from each process onto root process `nprocs - 1`, see [mpi4py](https://info.gwdg.de/~ceulig/docs-dev/doku.php?id=en:services:application_services:high_performance_computing:mpi4py) documentation.

## Exercises

 1. Implement the field computation in scatter.py after line `IMPLEMENT FIELD COMPUTATION HERE`.

 2. Implement the field gather operation where all the fields values are assembled onto the root process. This is required for the checksum and save operations to work.

 3. Measure the speedup compared to a single process execution
