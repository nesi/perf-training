---
layout: post
title: Summary
permalink: /python-scatter/summary
chapter: python-scatter
---

## What you have covered

You have learned how to profile a Python code to identify performance hot spots. You also learned that the coding style can have an impact on the performance. Vectorisation, for instance, brought 8x speedup over the original code. 

Additional improvements were achieved by migrating some parts of the code to C/C++. If the computational kernels are simple enough to be automatically translated to C then `numba` (15x) is an attractive option. Another factor 2x was obtained by hand-writing the C/C++ extension (37x over original code).

Throwing more resources at the problem is another way to reduce wall clock time. For our problem, we obtained a 4x speedup with 8 multiprocessing threads. Higher scalability resulted with MPI (7x speedup for 8 processes). 

The above strategies can be combined. For our test problem, the best results were obtained by applying OpenMP threading to the loops coded in C/C++, yielding a 95x speedup. 

Further performance improvements could potentially be achieved by combining MPI with C++ extensions and OpenMP. Alternatively, one could also consider offloading computations to a graphical processing unit (GPU). We need to keep in mind, however, that performance gains come at the cost of code development. The law of diminishing returns says that there is a point where the benefits gained are smaller than the amount of energy invested. 


![Speedup achieved by applying different high performance computing strategies](https://github.com/pletzer/perf-training/raw/summary/_lessons/python-scatter/images/speedup.png)


## Additional material

Want to learn more? Here are some sites' material which we have found useful:

 * [Python in high performance computing](https://events.prace-ri.eu/event/669/material/slides/0.pdf)

 * [High performance computing](https://cran.r-project.org/web/views/HighPerformanceComputing.html)

 * [Extending R with C](https://www.rstudio.com/resources/videos/extending-r-with-c-a-brief-introduction-to-rcpp/)

 * [Should I learn Fortran or C to extend R](https://stackoverflow.com/questions/3148763/should-i-learn-fortran-or-c-to-extend-r)

 * [High performance computing](http://blog.revolutionanalytics.com/high-performance-computing/)
