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

Vectorisation is a programming style where operations are applied to multiple array elements at one time. Modern computer hardware is designed to work very efficiently on arrays through native support for vector operations (e.g. AVX-512). In the case of AVX-512, up to 8 instructions can be executed simultaneously and this provide a first level or parallelism, before other approaches (OpenMP, GPU) are attempted. 

Vectorisation is applicable to loops and scripting languages are notoriously slow when it comes to executing loops. Hence the benefit of vectorisation is even greater for scripting languages since it replaces loops with procedure calls that run at the speed of compiled code. 

## Identifying code sections for vectorisation

Start by looking for loops in your code. The larger the loop the better.

 * the loop should have a pre-defined number of iterations with no premature exit condition. `For` loops are good, `while` loops are not good candidates. 
 * iterations should not depend on the previous iteration. Time stepping loops are typically not appropriate because each time step depends on the previous time step.
 * the loop should not have many if statements, which could cause some iterations to take longer than others
 * there should be a significant number of iterations, ideally hundreds or more

 Good candidates are loops where the same function is applied to each element or a reduction operation is applied to the array. When considering nested loops, start by vectorising the inner most loop.


### Example 1: function applied to each array element

Consider
```
import numpy
n = 10000000
a = numpy.zeros((n,), numpy.float64)
for i in range(n):
  a[i] = numpy.sin(i)
```
This can be rewritten as
```
import numpy
n = 10000000
a = numpy.sin(numpy.linspace(0, n))
```
The second, vectorised version will run about 10 times faster.

### Example 2: total sum

```
import numpy
n = 10000000
s = 0
for i in range(n):
  sum += i
```
can be rewritten as
```
import numpy
n = 10000000
s = numpy.linspace(0, n).sum()
```
As in the previous case, the vectorised code is more concise. The `for` loop has disappeared from the Python code, having been moved to C code.

## Vectorising the scatter code

There are three nested loops: (1) iteration over the y cells, (2) iteration over the x cells and (3) adding the contributions from each segment:
```python
for j in range(ny + 1):
  ...
  for i in range(nx + 1):
    ...
    scat[j, i] = wave.computeScatteredWave(kvec, xc, yc, p)
```
in scatter.py.  The inner most loop `wave.computeScatteredWave` is:
```python
  res = 0j
  n = len(xc)
  for i0 in range(n - 1):
    ...
    res += computeScatteredWaveElement(kvec, p0, p1, point)
```
where `n - 1` is the number of segments. We see that `res` adds the scattered wave contributions from each segment. These contributions can be added in any order. 

The aim here is to replace the above `for` loop by a set of `numpy` calls, which work with arrays instead of scalar numbers. 

First start by replacing scalar quantities with arrays of dimensions `n` and 3-vectors with arrays of size `n` times 3. Next apply element by element operations and reduction operations (e.g. `numpy.sum`) to compute each individual contribution. 

Switch to the `vectorise` branch:
```
git checkout vectorise
```
which has a modified version of the scatter code.  

## Exercise

 * In scatter.py, vectorise the `isInsideContour` function by eliminating the loop and working directly on the `xc` and `yc` arrays
 
 * Report the performance improvement of the vectorized branch over master. 


