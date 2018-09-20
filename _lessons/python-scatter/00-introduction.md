---
layout: post
title: Introduction
permalink: /python-scatter/introduction
chapter: python-scatter
---

**Work in progress**

## Aim of this training

Learn how to write Python programs that run efficiently on high performance computers. At the end of this training you will:

 * be able to identify performance bottlenecks in your application
 * understand that there are many ways to write a program (but some ways are better than others)
 * know how to apply different strategies to get your code to run faster


## Getting started

The training will be based on the *scatter* code, which computes the wave scattering on a 2D obstacle.

Clone and switch to the repository:

```
git clone https://github.com/pletzer/scatter.git scatter
cd scatter
```

This code uses Python. On Mahuika load the Python module:

```
module load Python/3.6.3-gimkl-2017a
module load Boost/1.61.0-gimkl-2017a
```
