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

Multiprocessing is suitable when you have:

 * computational resources with many CPU cores. On Mahuika, you can access up to 36 cores (72 multithreads).
 * a large number of tasks to be executed in any order

### Pros

 * a way to leverage multiple CPU cores for increased performance
 * can handle different work load

### Cons

 * processes must typically run on the same node

## Learn the basics 

As an example, we'll assume that you have to apply a very expensive function to a large number of input values:
```python
import time
def f(x):
	# expensive function
	time.sleep(10)
	return value

res = [f(x) for x in input_values]
```
In its original form, function `f` is called sequentially for each value of `x`. The modified version using 8 processes reads:
```python
import multiprocessing
import time
def f(x):
	# expensive function
	time.sleep(10)
	return value

pool = multiprocessing.Pool(processes=8)
res = pool.map(f, input_values)
```
How it works: each input value of array `input_values` is put in a queue and handed over to a worker. Here, there are 8 workers who accomplish the task in parallel. When a worker has finished a task, a new task is assigned until the queue is empty. At which point all the elements of array `res` have been filled.

## Running the scatter code using multiple threads

To submit a multithreaded job on Mahuika, type
```
srun --ntasks=1 --cpus-per-task=8 python scatter.py
```
(with additional `srun` options such as `--account=` required). This will launch a single task with 8 threads.  

To run interactively using 8 threads, type
```
export OMP_NUM_THREADS=8
python scatter.py
```

## Exercises

We've created a version of `scatter.py` which reads the environment variable `OMP_NUM_THREADS` to set the number of threads.  In this version, the computation of the field values takes place in function 
```python
def  computeField(k):
	#...
```
with argument `k` being the flat index into the 2D field arrays representing the incident and scatted fields (i.e. `k = j*nx1 + i`). In our formulation, the field at any location depends only on the values on the domain and obstacle boundaries, not on neighbouring locations. This allows us to compute the scatted and incident fields
```python
# change the following for parallel execution
res = [computeField(k) for k in range(ny1 * nx1)]
 
# compute the field
inci = numpy.array([r[0] for r in res], numpy.complex64).reshape((ny1, nx1))
scat = numpy.array([r[1] for r in res], numpy.complex64).reshape((ny1, nx1))
```
in parallel.

1. adapt the code in scatter.py to evaluate `computeField` in parallel
2. show the speedup with increasing number of processes
