---
layout: post
title: Numba
permalink: /python-scatter/numba
chapter: python-scatter
---

## Objectives

You will:

* learn how to accelerate code with numba

## Why use numba

Python often runs an order of magnitude or slower than compiled C/C++ code and sometimes numpy vectorisation is not enough to get the performance boost you need. In this case you will need to implement some parts of your code as C/C++ functions and invoke these functions from your Python script.

Numba will translate Python functions into C and compile the code automatically, under the hood.

### Pros

 * There is no need to know how to program C
 * Very little code change is in general required
 * Works well with numpy arrays
 * Numba supports multiple hardware (CPUs and GPUs), vectorisation, and can make your code run in parallel

### Cons

 * Not all functions can be successfully processed by numba - if your function calls another function implemented in another Python module then the chances are that the function cannot be accelerated. 


## Learn the basics 

As an example, we'll assume that you have to compute the sum of all the elements of a very large array:
```python
def mysum(array):
        res = 0
        for i in range(len(array)):
                res += array[i];
        return res;
```
The following will convert `mysum` into a C callable function and compile the code:
```python
from numba import jit

@jit(nopython=True)
def mysum(array):
        res = 0
        for i in range(len(array)):
                res += array[i];
        return res;
```
The version with decorator `@jit(nopython=True)` runs 20x faster for an array of size 100 million.

## How it works

Numba generates specialised, "just-in-time" from Python code. In the above example, the Python code defining function `mysum` is translated into C code, compiled and executed when you run the script, all completely transparently. Argument `nopython=True` indicates that the generated code will not access the Python interpreter. This produces the best performance but requires that all argument types can be inferred, which may not always be the case.


## Exercises
We'll use the code in directory `numba`. Start by
```
cd numba
```

We've created a version of `scatter.py` to which numba decorators can be freely added to its functions. The original version was calling the Hankel function `hankel1` from `scipy.special` and this prevented numba to generate the code. In the modified the version we call the Bessel functions from the C++ Boost library. Compile the code under `src/`
```
python setup.py build
```
(Make sure you have the `BOOST_DIR` environment set as described [here.](https://nesi.github.io/perf-training/python-scatter/introduction))


 1. profile the code to get baseline timings
 2. incrementally add `@jit` decorators to the most time consuming functions
 3. compare the performance with the original code
