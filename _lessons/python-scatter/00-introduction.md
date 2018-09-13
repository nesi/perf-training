---
layout: post
title: Introduction
permalink: /python-scatter/introduction
chapter: python-scatter
---

**Work in progress**

## Aim of this training

Develop the skills to write Python programs that run efficiently on high performance computers. At the end of this training you will:

 * be able to identify performance bottlenecks in your application
 * understand that there are many ways to write a program but some ways produce code that runs faster
 * know how to apply different strategies to accelerate a code


## Getting started

The training will be based on the *scatter* code, which computes wave scattering on a 2D obstacle.

Clone and switch to the repository:

```
git clone https://github.com/pletzer/scatter.git scatter
cd scatter
git fetch --all
```

This code uses Python. On Mahuika load the Python module:

```
module load Python/3.6.3-gimkl-2017a
```
