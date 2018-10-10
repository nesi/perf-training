---
layout: post
title: Vectorising
permalink: /python-scatter/vectorising
chapter: python-scatter
---

**Work in progress**

## Objectives

You will:

* understand what vectorisation is...
* learn to recognise code that can benefit from vectorisation...
* learn how to vectorise a loop...

We'll use the code in directory `vect`. Start by
```
cd vect
```

## What is vectorisation

Vectorisation is a programming style where loops are replaced by operations on arrays. Vectorisation typically improves the performance of a code and can make the code more concise and easier to maintain.

In scripting languages, loops can be slow to execute because of the overhead of the interpreter, which needs to parse each instruction, often many times when executed within a loop. Vectorisation removes the loop and replaces it with array operations, which are exectuted once. This can significantly boost performance. 

Even in the case of a compiled language, vectorisation can significantly accelerate a code because modern computer hardware tends to be highly optimised for array operations. Depending on the hardware, up to 8 or more instructions can be executed simultaneously for every CPU clock cycle. This provides a first level or parallelism, use this before trying other approaches (OpenMP, GPU, ...).

## Identifying code sections for vectorisation

Start by looking for **loops** in your code. The more iterations the better. 

 * the loop should have a **pre-defined number of iterations** with no premature exit condition. `for` loops can more easily be vectorised than `while` loops. 
 * each iteration should **not** depend on any previous iteration. One should be able to execute the iterations in any order.
 * it is best not to have `if` statements inside the loop as these could cause some iterations to take longer than others

Good candidates are loops where the same function is applied to each element. Reduction operations (for example sum or product of all array elements) are also good candidates. 

When considering nested loops, start by vectorising the inner most loop.

Array operations are available through the `numpy` Python module. Numpy arrays in many respects behave like lists with the following caveats

 * all array elements must have the **same type** (integer, float, etc.)
 * array elements cannot be added or removed

On the other hand numpy arrays support elementwise operations. Python code using large numpy arrays can expect to run as fast as C code. 

### Example 1: function applied to each array element

Consider computing the sine function of 10 million elements and storing the result in a list
```python
import numpy
n = 10000000
a = numpy.zeros((n,), numpy.float64)
for i in range(n):
  a[i] = numpy.sin(i)
```

The equivalent, vectorised version
```python
import numpy
n = 10000000
a = numpy.sin(numpy.linspace(0, n - 1, n))
```
runs about 10 times faster.

### Example 2: total sum

```python
import numpy
n = 10000000
s = 0
for i in range(n):
  s += i
```
can be rewritten as
```python
import numpy
n = 10000000
s = numpy.linspace(0, n).sum()
```
As in the previous case, the vectorised code is more concise.

## Vectorising the scatter code

We have written a partially vectorised version of `scatter`. In `wave.py`, 
```python
  res = 0j
  n = len(xc)
  for i0 in range(n - 1):
    ...
    res += computeScatteredWaveElement(kvec, p0, p1, point)
  return res
```
was replaced with:
```python
    ...
    return numpy.sum( dsdt * (-g * gradIncident(kvec, nDotK, pmid) + \
                              shadow * dgdn * incident(kvec, pmid)) )  
```
where `dsdt`, `g`, etc. are all arrays of size `n - 1` (number of segments). 


## Exercises

 1. profile the vectorised code and compare to the non-vectorised code

 2. in scatter.py, vectorise the `isInsideContour` function by eliminating the loop and working directly on the `xc` and `yc` arrays
 
 3. report the performance improvement of the vectorised branch over the non-vectorised, master branch. 


