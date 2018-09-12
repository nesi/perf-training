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

Vectorisation is a programming style where loops are replaced by operations on arrays.

In scripting languages, loops can be slow to execute because of the overhead of the interpreter which needs to parse each instruction. Vectorisation removes the loop and replaces it with a set of array operations, which are exectuted once. This can significantly boost performance. 

Modern computer hardware is highly optimised to work on arrays. Depending on the hardware, up to 8 or more instructions can be executed simultaneously on different array elements for every CPU clock tick. This provides a first level or parallelism, before other approaches (OpenMP, GPU) are to be attempted.

## Identifying code sections for vectorisation

Start by looking for loops in your code. The larger the loop the better.

 * the loop should have a pre-defined number of iterations with no premature exit condition. `For` loops, as opposed to `while` loops, are good candidates. 
 * each iteration in the loop should not depend on any previous iteration.
 * it is best not to have many `if` statements inside the loop as these could cause some iterations to take longer than others
 * the more iterations the better

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
As in the previous case, the vectorised code is more concise.

## Vectorising the scatter code

We have written a partially vectorised version of `scatter`
```
git checkout vectorise
```

There are three nested loops: (1) iteration over the y cells, (2) iteration over the x cells and (3) adding the contributions from each segment:
```python
for j in range(ny + 1):
  ...
  for i in range(nx + 1):
    ...
    scat[j, i] = wave.computeScatteredWave(kvec, xc, yc, p)
```
in scatter.py.  The inner most loop is in `wave.computeScatteredWave`:
```python
  res = 0j
  n = len(xc)
  for i0 in range(n - 1):
    ...
    res += computeScatteredWaveElement(kvec, p0, p1, point)
```
Here `n - 1` is the number of segments. We see that `res` adds the scattered wave contributions from each segment and these can be added in any order. The trick is to 
remove the loop is index `i0` by a sum:
```
    ...
    return numpy.sum( dsdt * (-g * gradIncident(kvec, nDotK, pmid) + \
                              shadow * dgdn * incident(kvec, pmid)) )  
```
where `dsdt`, `g`, etc. are all arrays of size `n - 1`. 


## Exercise

 * In scatter.py, vectorise the `isInsideContour` function by eliminating the loop and working directly on the `xc` and `yc` arrays
 
 * Report the performance improvement of the vectorised branch over the non-vectorised, master branch. 


