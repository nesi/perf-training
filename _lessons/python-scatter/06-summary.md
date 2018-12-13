---
layout: post
title: Summary
permalink: /python-scatter/summary
chapter: python-scatter
---

## What you have covered

You have learned that the computational efficiency of a program can be influenced by your coding style. A case in point is vectorisation (8x speedup). 

Additional improvements can be achieved by migrating code to C/C++. If the computational kernels are simple enough to be automatically translated to C then `numba` (15x) is an attractive option. Another factor 2x can be obtained by hand-writing the C/C++ extension (37x total).

Throwing more resources at the problem is another way to reduce wall clock time, but at the expense of higher overall computational cost. For our problem, you obtained a 4x speedup with using multiprocessing (8 threads). Better scalability resulted with MPI (7x for 8 processes). 

The above strategies can be combined. For our test problem, the best results were obtained by applying OpenMP threading to the loops coded in C/C++ (95x). 

![Speedup achieved by applying different high performance computing strategies](https://github.com/pletzer/perf-training/raw/summary/_lessons/python-scatter/images/speedup.png)


## Additional material

Want to learn more? Here are some sites' material which we have found useful:

 * [Python in high performance computing](https://events.prace-ri.eu/event/669/material/slides/0.pdf)

 * [High performance computing](https://cran.r-project.org/web/views/HighPerformanceComputing.html)

 * [Extending R with C](https://www.rstudio.com/resources/videos/extending-r-with-c-a-brief-introduction-to-rcpp/)

 * [Should I learn Fortran or C to extend R](https://stackoverflow.com/questions/3148763/should-i-learn-fortran-or-c-to-extend-r)

 * [High performance computing](http://blog.revolutionanalytics.com/high-performance-computing/)
