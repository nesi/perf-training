---
layout: post
title: Calling C/C++ extensions with ctypes
permalink: /python-scatter/ctypes
chapter: python-scatter
---

## Objectives

You will:

* learn how to call C/C++ compiled code from Python
* how to compile a C++ extension using `setuptools`

We'll use the code in directory `cext`. Start by
```
cd cext
```

## Why extend Python with C/C++

You want to call a function implemented in C, C++ or Fortran. Here we'll write custom code, build the code in a shared library and tell Python how to call the C/C++ functions. 

### Pros

 * A good way to glue Python with an external library
 * Can be used to incrementally migrate code to C/C++
 * Very flexible
 * Simpler and easier to maintain than custom C extensions 

### Cons

 * Significant learning curve, must understand how Python and C work

## Learn the basics 

As an example, we'll assume that you have to compute the sum of all the elements of a very large array. Let's assume you have written a C++ extension for that purpose
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
in file *mysum.cpp*. The `extern "C"` line is required if you compile the above in C++.

The easiest way to compile *mysum.cpp* is to write a *setup.py* file, which lists the source file to compile:
```python
from setuptools import setup, Extension

setup(
	...
	ext_modules=[Extension('mysum', ['mysum.cpp'],), ...],
)
```
You might have to add *include* directories and libraries if your C++ extension depends on external packages. Calling `python setup.py build` will compile the code and produce a shared library, something like `mysum.cpython-36m-x86_64-linux-gnu.so`. 

To call  `mysum` from Python we'll use the `ctypes` module:
```python
import ctypes
```

Because C/C++ is a strongly typed language and Python is not, we need to tell Python what the arguments are and make sure the Python variables we provide can be passed to the C/C++ routine safely. Note that any mistake will likely cause a segmentation fault.

The process is the following:

 1. open the shared library `mylib = ctypes.CDLL('build/lib.linux-x86_64-3.6/wave.cpython-36m-x86_64-linux-gnu.so')` (the name of the shared library is platform dependent)
 2. specify the function return type, `mylib.mysum.restype = ctypes.c_double` in our case
 3. specify the dummy argument types, `mylib.mysum.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double)]` to match the function's signature `double mysum(int, double*)`
 4. call the C/C++ function, `mylib.mysum(n, array.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))` where `array` is a `numpy` array. 

By default, arguments will be passed by value. To pass a pointer (`double*`) you need to declare the argument type to be `ctypes.POINTER(ctypes.c_double)`. You can declare `int*` similarly using `ctypes.POINTER(ctypes.c_int)`.

In the above example, the C++ routine expects a pointer to a double as argument, which you need to get from the numpy array. Numpy arrays have a `ctypes.data_as()` method which can be used to adapt the numpy array into a `double*` pointer. For a `float64` numpy array the pointer is `array.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))`.

Except for `int` types and strings, you will need to cast the arguments into corresponding `ctype`s. For instance, if you need to pass `myvar = 2.3` to a C function expecting `double`, then cast `myvar` into `ctypes.c_double(myvar)` before passing it to the function.

Strings will need to be converted to byte strings in Python 3 (`str(mystring).encode('ascii')`).

Passing by reference, for instance `int&` can be achieved using `ctypes.byref(myvar_t)` with `myvar_t` of type `ctypes.c_int`. 

The C type `NULL` will map to None. 

For a complete list of C to ctypes type mapping see the Python [documentation](https://docs.python.org/3/library/ctypes.html).


## Exercises

We've created a version of `scatter.py` that builds and calls a C++ external function `src/wave.cpp`. Load the Boost module
```
module load Boost/1.61.0-gimkl-2017a
```
and compile the code using
```
python setup.py build
```

 1. profile the code and compare the timings with the results under `original` and `vect`
 2. rewrite Python function `isInsideContour` defined in `scatter.py` in C++ and update file `setup.py` to compile your extension. 
 3. profile the code with your version of `isInsideContour` written in C++


