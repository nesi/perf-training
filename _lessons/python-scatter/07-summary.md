---
layout: post
title: Summary
permalink: /python-scatter/summary
chapter: python-scatter
---

## What you have covered

You have learned how to profile a Python code to identify performance hot spots. You also learned that the coding style can have an impact on the performance. Vectorisation, for instance, brought an 7-8x speedup over the original code. 

Additional improvements were achieved by migrating some parts of the code to C/C++. If the computational kernels are simple enough to be automatically translated to C then `numba` is an attractive option (16-17x speedup). Writing by hand the C/C++ extension brings a 20-30x speedup over the original code.

Throwing more resources at the problem is another way to reduce wall clock time. For our problem, we obtained a 3-4x speedup with 8 threads and a 5-6x speedup with MPI using 8 processes. 

The above strategies can be combined. For our test problem, the best results were obtained by applying OpenMP threading to the loops coded in C/C++. With a little additional tuning, a 110x speedup for 8 threads over the original code.

Your mileage may vary - all optimisation techniques presented here are problem type and size dependent. You should not expect the same speedup values for other problems.

![Speedup achieved by applying different high performance computing strategies](https://github.com/pletzer/perf-training/raw/summary/_lessons/python-scatter/images/speedup.png)


## Additional material

Want to learn more? Here is some material which we have found useful:

 * [Python in high performance computing](https://events.prace-ri.eu/event/669/material/slides/0.pdf)

 * [High performance computing](https://cran.r-project.org/web/views/HighPerformanceComputing.html)

 * [Extending R with C](https://www.rstudio.com/resources/videos/extending-r-with-c-a-brief-introduction-to-rcpp/)

 * [Should I learn Fortran or C to extend R](https://stackoverflow.com/questions/3148763/should-i-learn-fortran-or-c-to-extend-r)

 * [High performance computing](http://blog.revolutionanalytics.com/high-performance-computing/)
