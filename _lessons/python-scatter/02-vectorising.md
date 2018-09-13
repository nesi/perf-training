---
layout: post
title: Vectorising
permalink: /python-scatter/vectorising
chapter: python-scatter
---

**Work in progress**

## Objectives

You will:

* understand what vectorisation is
* learn to recognise code that can benefit from vectorisation
* learn how to vectorise a loop

## What is vectorisation

Vectorisation is a programming style where loops are replaced by operations on arrays. Vectorisation typically improves the performance of a code.

In scripting languages, loops can be slow to execute because of the overhead of the interpreter which needs to parse each instruction, often many times when executed within a loop. Vectorisation removes the loop and replaces it with a set of array operations, which are exectuted once. This can significantly boost performance. 

Even in the case of a compiled language, vectorisation can significantly accelerate a code because modern computer hardware tends to be highly optimised for array operations. Depending on the hardware, up to 8 or more instructions can be executed simultaneously on different array elements for every CPU clock cycle. This provides a first level or parallelism, a first step before trying other approaches (OpenMP, GPU).

## Identifying code sections for vectorisation

Start by looking for loops in your code. The larger the loop the better.

 * the loop should have a pre-defined number of iterations with no premature exit condition. `For` loops can more easily be vectorised than `while` loops. 
 * each iteration in the loop should not depend on any previous iteration (no loop dependence). One should be able to execute a loop in any order.
 * it is best not to have many `if` statements inside the loop as these could cause some iterations to take longer than others
 * the more iterations the better

Good candidates are loops where the same function is applied to each element or a reduction operation is applied to the array. When considering nested loops, start by vectorising the inner most loop.

Array operations are available through the `numpy` Python module. Numpy arrays don't have all the flexibility of Python lists:

 * numpy arrays require each element of the array to have the same type
 * numpy arrays have a fixed size and are not suited for cases where elements are added or removed

On the other hand numpy arrays support elementwise operations and Python code using large numpy arrays can expect to run in par with C code. 

### Example 1: function applied to each array element

Consider computing the sine function of 10 million elements
```python
import numpy
n = 10000000
a = numpy.zeros((n,), numpy.float64)
for i in range(n):
  a[i] = numpy.sin(i)
```
This can be rewritten as
```python
import numpy
n = 10000000
a = numpy.sin(numpy.linspace(0, n - 1, n))
```
The second, vectorised version will run about 10 times faster.

### Example 2: total sum

```python
import numpy
n = 10000000
s = 0
for i in range(n):
  sum += i
```
can be rewritten as
```python
import numpy
n = 10000000
s = numpy.linspace(0, n).sum()
```
As in the previous case, the vectorised code is more concise.

## Vectorising the scatter code

We have written a partially vectorised version of `scatter`, check it out with
```
git checkout vectorise
```

There are several nested loops:
```python
# iteration of y cells
for j in range(ny + 1):
  ...
  # iteration over x cells
  for i in range(nx + 1):
    ...
    scat[j, i] = wave.computeScatteredWave(kvec, xc, yc, p)
```
in scatter.py.  

The inner most loop is in `wave.computeScatteredWave`:
```python
  res = 0j
  n = len(xc)
  for i0 in range(n - 1):
    ...
    res += computeScatteredWaveElement(kvec, p0, p1, point)
```
Here `n - 1` is the number of segments. We see that `res` adds the scattered wave contributions from each segment describing the geometry of the obstacle. These contributions can be added in any order. The vectorised version replaced the loop with index `i0` by a sum:
```python
    ...
    return numpy.sum( dsdt * (-g * gradIncident(kvec, nDotK, pmid) + \
                              shadow * dgdn * incident(kvec, pmid)) )  
```
where `dsdt`, `g`, etc. are all arrays of size `n - 1`. 


## Exercise

 * profile the vectorised code and compare to the non-vectorised code

 * in scatter.py, vectorise the `isInsideContour` function by eliminating the loop and working directly on the `xc` and `yc` arrays
 
 * report the performance improvement of the vectorised branch over the non-vectorised, master branch. 


