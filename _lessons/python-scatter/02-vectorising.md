---
layout: post
title: Vectorising
permalink: /python-scatter/vectorising
chapter: python-scatter
---


## Objectives

You will:

* understand what vectorisation is
* learn to recognise code that can benefit from vectorisation
* learn how to vectorise a loop

We'll use the code in directory `vect`. Start with
```
cd vect
```

## What is vectorisation

Vectorisation in Python is a programming style where operations on a single piece of data, typically in a loop, are replaced by operations on entire arrays. Vectorisation can improve the performance of a code, and can make the code more concise and easier to maintain.

In scripting languages, loops can be slow to execute because of the overhead of the interpreter, which may need to parse each expression, perform various input data checks and more. These overheads add up when expressions are repeated many times in a loop. Vectorisation avoids the issue by replacing the loop with a single array operation, which can significantly boost performance. 

## Identifying code sections for vectorisation

Start by looking for **loops** in your code. The more iterations the better. 

 * the loop should have a **pre-defined number of iterations** with no premature exit condition. `for` loops can more easily be vectorised than `while` loops. 
 * each iteration should **not** depend on any previous iteration. One should be able to execute the iterations in any order.
 * it is best not to have `if` statements inside the loop as these could cause some iterations to take longer than others

Good candidates are loops where the same function is applied to each element. Reduction operations (for example sum or product of all array elements) are also good candidates. 

When considering nested loops, start by vectorising the innermost loop, unless the innermost loop only performs very few iterations.

Array operations are available through the `numpy` Python module. `numpy` arrays in many respects behave like lists with the following caveats:

 * all array elements must have the **same type** (integer, float, etc.)
 * array elements cannot be added or removed (without having to recreate the array)

On the other hand, `numpy` arrays support elementwise operations.

Python code using large `numpy` arrays should almost always run much faster than plain Python code, and it can run as fast as C code in some cases. If your algorithm has high "algorithmic intensity", where many operations are done on the same piece of data, you may find that implementing loops with Numba or a low-level language like C provides yet better performance - these methods can often use fast processor caches more efficiently, avoiding the cost of repeatedly fetching data form memory. They also avoid temporary arrays that `numpy` code sometimes requires.

### Example 1: function applied to each array element

Consider computing the sine function of 10 million elements and storing the result in a list
```python
import numpy

n = 10000000
a = numpy.zeros([n], numpy.float64)
for i in range(n):
  a[i] = numpy.sin(i)
```

The equivalent, vectorised version
```python
import numpy

n = 10000000
a = numpy.sin(numpy.linspace(0, n - 1, n))
```
runs 20 or more times faster.

Note that the vectorised version requires more memory since a temporary array will need to be created to hold `numpy.linspace(0, n - 1, n)`. In general, the vectorised version may contain many more temporary arrays, so a trade-off must be made between memory usage and performance.

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
s = numpy.linspace(0, n-1, n).sum()
```
As in the previous case, the vectorised code is more concise.

## Vectorising the scatter code

We have written a partially vectorised version of `scatter`. In `wave.py`, 
```python
  res = 0j
  n = len(xc)
  for i0 in range(n - 1):
    #...
    res += computeScatteredWaveElement(kvec, p0, p1, point)
  return res
```
was replaced with:
```python
    #...
    return numpy.sum( dsdt * (-g * gradIncident(kvec, nDotK, pmid) + \
                              shadow * dgdn * incident(kvec, pmid)) )  
```
where `dsdt`, `g`, etc. are all arrays of size `n - 1` (number of segments). 


## Exercises

 1. profile the vectorised code and compare to the non-vectorised code

 2. in scatter.py, vectorise function `isInsideContour` by eliminating the loop computing the sum `tot` and report the new timing
 

