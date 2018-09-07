---
layout: post
title: Profiling
permalink: /python-scatter/profiling
chapter: python-scatter
---

**Work in progress**

## Objectives

You will:

* understand what vectorisation is
* learn to recognise code that can benefit from vectorisation
* leanr how to vectorise a loop

## What is vectorisation

Vectorisation is a programming style where operations are applied to multiple array elements at one time. Modern computer hardware is designed to work very efficiently on arrays through native support for vector operations (e.g. AVX-512). In the case of AVX-512, up to 8 instructions can be executed simultaneously and this provide a first level or parallelism, before other approaches (OpenMP, GPU) are attempted. 

Vectorisation is applicable to loops and scripting languages are notoriously slow when it comes to executing loops. Hence the benefit of vectorisation is even greater for scripting languages since it replaces loops with procedure calls that run at the speed of compiled code. 

## Identifying code for potential vectorisation

Start by looking for loops in your code. The larger the loop the better. Moreover:

 * the loop should have a pre-defined number of iterations with no premature exit condition. `For` loops are good, `while` loops are not good candidates. 
 * iterations should not depend on the previous iteration. Time stepping loops are typically not appropriate because each time step depends on the previous time step.
 * the loop should not have many if statements, which could cause some iterations to take longer than others

 Good candidates are loops where the same function is applied to each element or a reduction operation is applied to the array. For instance the sum of all the elements of an array can be vectorised. (The sum does not depend on the order in which the elements are added.) The "dot" product between matrices is another good example of a reduction operation that can be vectorised. 

 When considering nested loops, start by vectorising the inner most loop.


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

The branch `vectorized` 
```
git pull https://github.com/pletzer/scatter vectorized
git checkout vectorized
```
has a modified version of the scatter code.  

## Exercise

Report the performance improvement of the vectorized branch over master. 


