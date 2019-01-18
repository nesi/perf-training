---
layout: post
title: Numba
permalink: /python-scatter/numba
chapter: python-scatter
---

## Objectives

You will learn:

* what numba is 
* how to accelerate code with numba 

We'll use the code in directory `numba`. Start by
```
cd numba
```

## Why use numba

Python often runs an order of magnitude or slower than compiled C/C++ code and sometimes numpy vectorisation is not enough to get the performance boost you need. In this case you will need to implement some parts of your code as C/C++ functions and invoke these functions from your Python script. 

Numba will translate Python functions into C and compile the code automatically, under the hood.

### Pros

 * there is no need to know how to program C
 * very little code change is in general required by the programer
 * works well with numpy arrays
 * numba supports multiple hardware (CPUs and GPUs), vectorisation, and can make your code run in parallel

### Cons

 * not all functions can be successfully processed by numba - if your function calls another function implemented in another Python module then the chances are that the function cannot be accelerated. 


## Learn the basics 

As an example, we'll assume that you have to compute the sum of all the elements of an array:
```python
import numpy

def mysum(array):
    res = 0
    for i in range(len(array)):
        res += array[i]
    return res

# print the sum of 0, 1, ... 99999999
print(mysum(numpy.arange(0, 100000000)))
```
The following will convert `mysum` into a C callable function and compile the code:
```python
import numpy
from numba import jit

@jit(nopython=True)
def mysum(array):
    res = 0
    for i in range(len(array)):
        res += array[i];
    return res;

# print the sum of 0, 1, ... 99999999
print(mysum(numpy.arange(0, 100000000)))
```
The version with decorator `@jit(nopython=True)` runs 20x faster.

*Notes*: 

 * be sure to pass a numpy array to `mysum`, passing a Python list will cause the numba version to run slower than the original version
 * it is possible to apply `@jit` decorators to loops that contain function calls. However, these functions need to be either implemented in C or have the `@jit` decorator

## How it works

Numba generates specialised, "just-in-time" code from Python source code. In the above example, the Python function `mysum` is translated into C code, compiled and executed when you run the script. Argument `nopython=True` indicates that the generated code will not access the Python interpreter. This produces the best performance but requires that all argument types can be inferred, which may not always be the case.

*Note*: there is a one off cost when calling the function the first time. Translating the code from Python to C and compiling the C code will consume time.



## Exercises

We've created a version of `scatter.py` to which numba decorators can be freely added to its functions. The original version was calling the Hankel function `hankel1` from `scipy.special` and this prevented numba to generate the code. In the modified the version we call the Bessel functions from the C++ Boost library. Compile the code under `src/`
```
python setup.py build
```
(Make sure you have the `BOOST_DIR` environment set as described [here.](introduction))


 1. profile *scatter.py* to get a baseline timing using the approach described [here](profiling)
 2. incrementally add `@jit` decorators to the most time consuming functions. Start with the lowest level functions and move up the call stack
 3. compare the performance with the original code


