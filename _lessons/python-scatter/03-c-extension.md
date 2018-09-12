---
layout: post
title: C Extension
permalink: /python-scatter/c-extension
chapter: python-scatter
---

**Content coming soon**

## Objectives

You will:

* how to extend your Python code with C++ compiled code
* how to tell Python to compile your C++ extension

## Why extending Python with C/C++

Python often runs an order of magnitude or more slowly than compiled code. Programming languages such as C and C++ are strongly typed and this allows the compiler to optimise code in ways the Python interpreter cannot. 

## Learn the basics 

We'll assume that you have profiled your code and found a performance bottleneck. For the sake of providing an example, we'll assume that the bottleneck is the sum of all the elements of a very large array. The C++ extension
```
double mysum(int n, double* array) {
	double res = 0;
	for (int i = 0; i < n; ++i) {
		res += array[i];
	}
	return res;
}
```
is written in file *mysum.cpp*. 

A convenient way to compile *mysum.cpp* is to write a *setup.py* file, which lists the source file to compile:
```python
from setuptools import setup, Extension

setup(
	...
	scripts=['scatter.py'],
	ext_modules=[Extension('mysum', ['mysum.cpp'],), ...],
)
```
Calling `python setup.py build` will compile the code and produce the shared library `mysum*.so`. Once the shared library is built, Python can call directly `mysum` using the `ctypes` module:

```
import ctypes
```

This involves the following steps:

 1. open the shared library `mylib = ctypes.CDLL('build/lib.linux-x86_64-3.6/wave.cpython-36m-x86_64-linux-gnu.so')` (the shared library name is platform dependent)
 2. describe the interface. To call the C/C++ function you need to specify the function return type, `mylib.mysum.restype = ctypes.c_double` in our case. You also need to specify the argument types, `mylib.mysum.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double)]` to match the function's signature `double mysum(int, double*)`.
 3. call the function in the shared library, ie `mylib.mysum(n, array.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))`. 

By default, arguments will be passed by value. To pass a pointer (`double*`) you need to declare the argument type to be `ctypes.POINTER(ctypes.c_double)`. You can declare `int*` similarly with `ctypes.POINTER(ctypes.c_int)`.

Our C++ routine expects a pointer to a double as argument, which you need to get from the numpy array. Numpy arrays have a `ctypes.data_as()` method which takes the `ctypes` type. For a `numpy.float64` array the pointer is `array.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))`.


## Exercises

We have created a version
```
git checkout cpp-external
```
that builds and calls a C++ external function `src/wave.cpp`. Compile the code using
```
module load Boost/1.61.0-gimkl-2017a
python setup.py build
```
(The C++ extension needs the Boost library.)

 1. profile the code and compare timings with the master and vectorise branches
 2. rewrite Python function `isInsideContour` defined in `scatter.py` in C++ and update file `setup.py` to compile your extension. 
 3. profile the code with your version of `isInsideContour` written in C++


