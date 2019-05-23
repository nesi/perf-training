---
layout: post
title: Multiprocessing
permalink: /python-scatter/multiprocessing
chapter: python-scatter
---

## Objectives

Learn how to call a function in parallel using shared memory multiprocessing.

We'll use the code in directory `multiproc`. Start by
```
cd multiproc
```

## Why multiprocessing

Multiprocessing is suitable when:

 * your computational resources have many CPU cores. On Mahuika, you can access up to 36 cores (72 hyperthreads) within a single node.
 * you have a large number of tasks that need to be executed in any order

### Pros

 * decreases your execution time by leveraging multiple CPU cores
 * suitable when the workload of each process varies

### Cons

 * uses more resources
 * processes must typically run on the same node

## Learn the basics 

As an example, we'll assume that you have to apply a very expensive function `f` to a number of input values:

```python
import time

def f(x):
    # expensive function
    time.sleep(10)
    return x

# call the function sequentially for input values 0, 1, 2, 3 and 4
input_values = [x for x in range(5)]
res = [f(x) for x in input_values]
```

In its original form, function `f` is called sequentially for each value of `x`. The modified version using 3 processes is:

```python
import multiprocessing
import time

def f(x):
    # expensive function
    time.sleep(10)
    return x

# create a "pool" of 3 processes to do the calculations
pool = multiprocessing.Pool(processes=3)

# the function is called in parallel, using the number of processes 
# we set when creating the Pool
input_values = [x for x in range(5)]
res = pool.map(f, input_values)
```

How it works: each input value of `input_values` is put in a queue and handed over to a worker. Here, there are 3 workers who accomplish the task in parallel. When a worker has finished a task, a new task is assigned until the queue is empty. At which point all the elements of array `res` have been filled.

The serial version takes about 50 seconds - there are 5 tasks each taking 10 seconds. The multiprocessing version takes about 20 seconds as some processes need to complete two tasks and others only one. Naturally, it would be more efficient to match the number of tasks to the number of processes. In many cases, however, the number of tasks exceeds the number of processes available on the system, meaning that some processes will need to work on several tasks.


## Running the scatter code using multiple threads

We've created a version of `scatter.py` which reads the environment variable `OMP_NUM_THREADS` to set the number of processes. We've also modified our `scatter.sl` script to set the number of processes using `--cpus-per-task=4`. To prevent two processes to be placed on each core, we use `--hint=nomultithread`. 

To run interactively using 4 processes, type
```
export OMP_NUM_THREADS=4
python scatter.py
```

## Exercises

 This version of *scatter.py* has been slightly adapted so that, with a few code changes, you can turn the serial version into one where function `computeField` can execute in parallel. Function `computeField` takes input argument `k`, the flat index into the 2D field arrays representing the incident and scatted fields (i.e. `k = j*nx1 + i`), and returns the incident and scattered field values for each grid node. The incident and scattered field values
```python
# change the following for parallel execution
res = [computeField(k) for k in range(ny1 * nx1)]
```
can be computed in any order.

1. adapt the code in scatter.py to call `computeField` in parallel (the number of processes is `nproc`)
2. what is the speedup (timing of `--cpus-per-task=1` over `--cpus-per-task=8`)?
