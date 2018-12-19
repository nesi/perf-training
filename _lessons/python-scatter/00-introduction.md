---
layout: post
title: Introduction
permalink: /python-scatter/introduction
chapter: python-scatter
---

## Aim of this training

Learn how to write Python programs that run efficiently on high performance computers. At the end of this training you will:

 * be able to identify performance bottlenecks in your application
 * understand that there are many ways to write a program (but some ways are better than others)
 * know how to apply different strategies to get your code to run faster

## Getting ready

The training requires:

 * Python 3 (tested with version 3.6.3)
 * numpy (1.13.3)
 * scipy (1.0.0)
 * setuptools (28.8.0)
 * Boost library (1.61)

Set environment variable 
```
export BOOST_DIR=<top-directory-where-boost-is-installed>
```


On NeSI's Mahuika Cray CS400 cluster, 

```
module load Python/3.6.3-gimkl-2017a
module load Boost/1.61.0-gimkl-2017a
```
and there is no need to set `BOOST_DIR`.

## Scattering wave example problem

We will run the *scatter* code. Clone and switch to the repository:

```
git clone https://github.com/pletzer/scatter.git scatter
cd scatter/original
```

The code computes the scattering of a plane wave against a two-dimensional obstacle

[Click here to see the incident wave in action](https://youtu.be/FIKSUGk68z8)

As the incoming wave moves from left to right, it encounters the obstacle and gets reflected. 
The obstacle is represented by segments, each responsible for partially reflecting and scattering the wave. 
The sum of the contributions from each segments gives the total scattered wave. 

[Click here to see the scattered wave](https://youtu.be/7ds4S5DCTB8)

[Click here to see the total, incident plus scattered wave](https://youtu.be/zxVEIxZkWyk)

Notice the small wave amplitude on the shadow side of the obstacle. 

### How to run the scatter code

You can run the code interactively
```
python scatter.py
```
or by submitting a job to the scheduler. On Mahuika
```
srun --account="myAccount" python scatter.py
```
where "myAccount" is your account on Mahuika (e.g. nesi12345). This will launch a single task. 

### Adjusting the domain size and contour resolution

As you improve the performance of the code, you'll find it useful to increase the problem resolution. This can be done by passing command line options to `scatter.py`. Type `python scatter.py -h` to see the full list of options. The options that control the grid size are `-nx # -ny #` for the number of cells in the x and y direction. Option `-nc #` sets the number of segments. 

The default values are `-nx 128`, `-ny 128` and `-nc 128`. The execution time scales linearly with the values of options `-nx`, `-ny` and `-nc`. For example:
```
python scatter.py -nx 256 -ny 256 -nc 512
```
will run the code using 256x256 cells and 512 obstacle segments and we expect the code to run `2*2*4 = 16` times longer compare to the default resolution.


### How to check if the results have changed

When modifying the code, it is important to check that the results haven't changed. Use
```
python scatter.py -c 
```
to record the sum of the field values squared (4686.33935546875). Make sure this value does not change after code editing. 

Note: the check sum changes with resolution and other parameters. 

## Measuring execution time

You can use the `time` command
```
time python scatter.py
```
which may return something like
```
real	1m21.575s
user	1m21.215s
sys	0m0.243s
```
The relevant time is `real`, the wall clock time.
