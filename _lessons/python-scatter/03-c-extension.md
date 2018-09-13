---
layout: post
title: C/C++ Extension
permalink: /python-scatter/c-extension
chapter: python-scatter
---

**Content coming soon**

## Objectives

You will:

* how to call C/C++ compiled code from Python
* how to compile a C++ extension using `setuptools`

## Why extend Python with C/C++

Python often runs an order of magnitude or slower than compiled C/C++ code. Sometimes numpy vectorisation is not enough to get the performance boost you need. In this case you will need to implement some parts of your code as C/C++ functions and invoke these functions from your Python script. 

There are multiple ways this can be achieved - we encourage you to look at Cython and numba as alternative approaches. Here we will write custom code, build the code in a shared library and tell Python how to call the C/C++ functions. 

## Learn the basics 

As an example, we'll assume that you have to compute the sum of all the elements of a very large array. You have written a C++ extension
```C++
extern "C"
double mysum(int n, double* array) {
	double res = 0;
	for (int i = 0; i < n; ++i) {
		res += array[i];
	}
	return res;
}
```
in file *mysum.cpp*. The `extern "C"` line is required if you compile in C++ but is not required in C.

The easiest way to compile *mysum.cpp* is to write a *setup.py* file, which lists the source file to compile:
```python
from setuptools import setup, Extension

setup(
	...
	ext_modules=[Extension('mysum', ['mysum.cpp'],), ...],
)
```
You might have to add *include* directories and libraries if your C++ extension depends on an external package. 

Calling `python setup.py build` will compile the code and produce the shared library, something like `mysum.cpython-36m-x86_64-linux-gnu.so`. Once the shared library is built, Python can call directly `mysum` using the `ctypes` module with a little help. Because C/C++ is a strongly typed language and Python is not, we need to tell Python what the arguments are and make sure the Python variables we provide can be passed to the C/C++ routine. 

 1. open the shared library `mylib = ctypes.CDLL('build/lib.linux-x86_64-3.6/wave.cpython-36m-x86_64-linux-gnu.so')` (the name of the shared library is platform dependent)
 2. prior to calling the C/C++ function you need to specify the function return type, `mylib.mysum.restype = ctypes.c_double` in our case
 3. you also need to specify the argument types, `mylib.mysum.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double)]` to match the function's signature `double mysum(int, double*)`
 4. call the function in the shared library, ie `mylib.mysum(n, array.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))`. By default, arguments will be passed by value. To pass a pointer (`double*`) you need to declare the argument type to be `ctypes.POINTER(ctypes.c_double)`. You can declare `int*` similarly with `ctypes.POINTER(ctypes.c_int)`.

In the above example, the C++ routine expects a pointer to a double as argument, which you need to get from the numpy array. Numpy arrays have a `ctypes.data_as()` method which can be used to adapt the numpy array into a `double*` pointer. For a `numpy.float64` array the pointer is `array.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))`.


## Exercises

We have created a version
```
git checkout cpp-external
```
that builds and calls a C++ external function `src/wave.cpp`. Load the Boost module
```
module load Boost/1.61.0-gimkl-2017a
```
and compile the code using
```
python setup.py build
```

 1. profile the code and compare timings with the master and vectorise branches
 2. rewrite Python function `isInsideContour` defined in `scatter.py` in C++ and update file `setup.py` to compile your extension. 
 3. profile the code with your version of `isInsideContour` written in C++


