---
layout: post
title: Profiling
permalink: /python-scatter/profiling
chapter: python-scatter
---

## Objectives

Learn how to profile Python code:

* use different tools to gather profiling information
* visualise the profiling data
* interpret the profiling results

## Introduction to profiling

Profiling tools help you understand how much time is spent in different
parts of your code when it runs. This can be function, loop, or source code line based. This information is important for optimising code, as it
enables you to focus your efforts on improving the parts of the code that
will result in the biggest gains in performance.

Due to possible overhead the code could run slower than normal. Therefore it is generally advisable to choose a small but representative case to profile, i.e. something that is representative of what you eventually want to run but completes in a short time frame.

Here we are going to profile the scatter code to understand where we should
focus our efforts when we try to improve its performance.

## Profiling Python code with *cProfile*
We'll use the code in directory `original`. Start by

```
cd original
```

The *cProfile* profiler is one implementation of the Python profiling interface. It measures the time spent within a function and the amount of calls.

**Note:** The timing information should not be taken as absolute values, since the profiling itself could possibly extend the run time, in some cases.

Run the following command to profile the code:

```
python -m cProfile -o output.pstats scatter.py
```

Notice the `-m cProfile -o output.pstats` in the above command. This enables
profiling and stores the profiling results in a file called *output.pstats*.
If you leave out these options the code will just run normally.

**Note:** the code will take longer to run when profiling is enabled, due to
the overhead involved in collecting the profiling information.

A nice way to visualise the  *output.pstats* file is with *gprof2dot*.

### Visualising the profiling output with *gprof2dot*

**Note:** `gprof2dot` is installed on Mahuika already. If you need to install it
elsewhere you can try `pip install gprof2dot` or search online for documentation.

Run `gprof2dot` to generate a PNG image file:

```
gprof2dot --colour-nodes-by-selftime -f pstats output.pstats | dot -Tpng -o output.png
```

The `dot` program comes from *Graphviz*, which is already installed on
Mahuika.

Now view *output.png* by copying it to your local machine or running
`display output.png` (if you enabled X11 forwarding).

It should look something like this:

[![profiling-results](images/scatter-profile.png)](images/scatter-profile.png)

### Interpreting the *gprof2dot* output

What does the image show:

* Each box represents a function
  - the percentage of total run time spent in this function, including time
    spent in other functions that are called by this function
  - (in brackets) the percentage of total run time spent in this function
    only, i.e. excluding time spent in other functions that are called by this
    function. We call this *self time*.
  - the number of times this function was called
* Arrows indicate which functions are called by other functions
  - information about the number of times called and percentage of total run
    time
* We used the option `--colour-nodes-by-selftime`, so boxes are coloured by
  self time (the number in brackets)
  - red coloured boxes are the functions that have the most time spent in them
  - blue boxes have the least time
* Some functions that take a very low percentage of total run time may not
  show up

What to look for:

* Typically you would look for functions that have a lot of *self* time (the
  number in brackets). We call these functions *hotspots*.
  - 58.31% of total time is spent in `computeScatteredWaveElement` (the red
    box), so this would be a good place to start when trying to optimise this
    code.
* Sometimes functions show up from libraries that you call (e.g. *scipy* or
  *numpy*), for example the green box calling `dot` that takes 10.82% total
  time.
  - Usually you don't want to change code from external libraries, but you can
    look at your functions that call that function, by going back along the
    arrow. You might be able to optimise the way your code calls the external
    function, use a more optimised library, or remove the call entirely.



## Profiling Python code with *line_profiler*

The *cProfile* tool only times function calls. This is a good first step to
find hotspots in your code (and often this is enough by itself). However, in
some cases knowing that a particular function takes a lot of time is not
particularly helpful. For example, it could be a very long function with multiple loops and computations.

With *line_profiler* you have to explicitly tell it which functions you would
like to be profiled, by modifying the source code slightly. Then
*line_profiler* will time the execution of individual lines within those
functions.

**Note:** *line_profiler* is installed in the Python module we loaded earlier.
You can check it is installed by running `kernprof --help`, which should print
help information for the `kernprof` (*line_profiler*) program that we are going
to use. (If not then `pip install line_profiler`.)

To demonstrate the use of *line_profiler* we will use it to profile the
`isInsideContour` function.

**Note:** we chose this function because it is short, which means we can
include the output here and explain it. Typically, you would use
*line_profiler* to gather more information about functions that *cProfile* has
identified as hotspots.

1. Edit the file *scatter.py*. Find the line that starts with:
   ```
   def isInsideContour(p, xc, yc):
   ```
   On the previous line add `@profile`, which is known as a *decorator* and
   tells *line_profiler* that we want to profile this function:
   ```
   @profile
   def isInsideContour(p, xc, yc):
   ```
2. Run *line_profiler*:
   ```
   kernprof -l -v scatter.py
   ```
   The `-l` flag tells *line_profiler* to do line-by-line profiling and `-v`
   tells it to print the profiling information out at the end of the run.

Detailed documentation about *line_profiler* can be found
[here](https://github.com/rkern/line_profiler).

### Interpreting *line_profiler* output

You should see something like this after *line_profiler* has run:

```
Wrote profile results to scatter.py.lprof
Timer unit: 1e-06 s

Total time: 16.5079 s
File: scatter.py
Function: isInsideContour at line 28

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    28                                           @profile
    29                                           def isInsideContour(p, xc, yc, tol=0.01):
    30                                               """
    31                                               Check is a point is inside closed contour by summing the
    32                                               the angles between point p, (xc[i], yc[i]) and (xc[i+1], yc[i+1]).
    33                                               Point p id declared to be inside if the total angle amounts to
    34                                               2*pi.
    35                                           
    36                                               @param p point (2d array)
    37                                               @param xc array of x points, anticlockwise and must close
    38                                               @param yc array of y points, anticlockwise and must close
    39                                               @param tol tolerance
    40                                               @return True if p is inside, False otherwise
    41                                               """
    42     16641      14072.0      0.8      0.1      tot = 0.0
    43   2146689     984225.0      0.5      6.0      for i0 in range(len(xc) - 1):
    44   2130048     971130.0      0.5      5.9          i1 = i0 + 1
    45   2130048    5104259.0      2.4     30.9          a = numpy.array([xc[i0], yc[i0]]) - p[:2]
    46   2130048    4860154.0      2.3     29.4          b = numpy.array([xc[i1], yc[i1]]) - p[:2]
    47   2130048    4548639.0      2.1     27.6          tot += math.atan2(a[0]*b[1] - a[1]*b[0], a.dot(b))
    48     16641      10751.0      0.6      0.1      tot /= twoPi
    49     16641      14653.0      0.9      0.1      return (abs(tot) > tol)
```

* Line numbers and the contents of each line are shown
* The "% Time" column is useful; it shows the percentage of time in that
  function that was spent on that line
* "Hits" shows the number of times that line was run
* We can see that lines 45, 46 and 47 each take around 30% of the time spent
  in this function.

## Memory Profiler

There is another useful Python profiling tool called [memory_profiler](https://pypi.org/project/memory_profiler/),
which can monitor memory consumption in a Python script on a line-by-line basis.
The memory profiler tool is used in a similar way to the *line_profiler* tool we
already covered, i.e. you have to use the `@profile` decorator to explicitly
tell *memory_profiler* which functions you wish to profile.

We will not cover memory profiler in detail here but more information can be found
at the page linked above.

## ARM MAP

Another useful profiler is provided on the NeSI system, the [ARM MAP](https://www.arm.com/products/development-tools/server-and-hpc/forge/map) (previous Allinea MAP) profiler, which is part of the `forge` module (as well as the parallel debugger DDT).

In contrast to cProfile, MAP is a commercial product, which can profile parallel, multi-threaded and single-threaded C/C++, Fortran and F90, as well as Python codes.
It can be used without code modification.
MAP can be launched with a GUI and without. The GUI allows the user to navigate through the code and enables them to focus on specific source lines. The "Express Launch", without a GUI, enables easy usage of existing submission scripts and workflows. For more details see the [ARM MAP manual](https://developer.arm.com/docs/101136/latest/map)). On the NeSI system you can start it by loading `module load forge` and launching `map`.

## Summary

You should now be able to profile code to help understand where time is being
spent in a Python code.
