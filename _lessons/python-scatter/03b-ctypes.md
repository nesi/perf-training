---
layout: post
title: Calling C/C++ extensions with ctypes
permalink: /python-scatter/ctypes
chapter: python-scatter
---

## Objectives

You will learn:

* how to call C/C++ compiled code from Python using the `ctypes` module
* how to compile a C++ extension using `setuptools`

We'll use the code in directory `cext`. Start by
```
cd cext
```

## Why extend Python with C/C++

 1. You want to call a function that is implemented in C, C++ or Fortran. This can give access to a vast collection of libraries so you won't have to rewrite the code in Python.
 2. You have identified a performance bottleneck - reimplementing some parts of your Python code in C, C++ or Fortran will give you a performance boost
 3. Make your code type safe. In contrast to C, C++ and Fortran, Python is not a typed language - you can pass any object to any Python function.  This can cause runtime failures in Python which cannot occur in C, C++ or Fortran, as the error would be caught by the compiler. 

### Pros

 * A good way to glue Python with an external library
 * Can be used to incrementally migrate code to C/C++
 * Very flexible
 * Simpler and easier to maintain than custom C extensions 

### Cons

 * Has a learning curve, one must understand how Python and C work
 * Mistakes often lead to segmentation faults, which can be hard to debug

## Learn the basics 

As an example, we'll assume that you have to compute the sum of all the elements of an array. Let's assume you have written a C++ extension for that purpose
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
You might have to add *include* directories and libraries if your C++ extension depends on external packages. 
An example of a `setup.py` file can be found [here](https://raw.githubusercontent.com/pletzer/scatter/master/cext/setup.py). 

Calling `python setup.py build` will compile the code and produce a shared library, something like `mysum.cpython-36m-x86_64-linux-gnu.so`.

The extension `.so` indicates that the above is a shared library (also called dynamic-link library or shared object). The advantage of creating a shared library over a static library is that in the former the Python interpreter needs not be recompiled. The good news is that `setuptools` knows how to compile shared library so you won't have to worry about the details.

To call  `mysum` from Python we'll use the `ctypes` module:
```python
import ctypes
```

Because C/C++ is a strongly typed language and Python is not, we need to tell Python what the arguments are and make sure the Python variables we provide can be passed to the C/C++ function safely. 

The Python code to call the above `mysum` function is:
```python
import ctypes
import numpy

# open the shared library
libfile = 'build/lib.linux-x86_64-3.6/wave.cpython-36m-x86_64-linux-gnu.so'
mylib = ctypes.CDLL(libfile)

# tell Python the return type of function mysum
mylib.mysum.restype = ctypes.c_double

# tell Python the argument types of function mysum
mylib.mysum.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double)]

# call the function
mylib.mysum(n, array.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))
```

By default, arguments will be passed by value. To pass an array of doubles (`double*`) you need to declare the argument as `ctypes.POINTER(ctypes.c_double)`. You can declare `int*` similarly by using `ctypes.POINTER(ctypes.c_int)`.

In the above example, the C++ routine expects a pointer to a double as argument. Numpy arrays have a `ctypes.data_as()` method which can be used to adapt numpy arrays into a `double*` pointer. For a `float64` numpy array named `arr`, the pointer is `arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))`.

Except for `int` types and strings, you will need to cast the arguments into corresponding `ctypes`. 
For instance, if you need to pass the floating point value `myvar` to a C function expecting `float`, then you will need to pass `ctypes.c_float(myvar)` to the function.

Strings will need to be converted to byte strings in Python 3 (`str(mystring).encode('ascii')`).

Passing by reference, for instance `int&` can be achieved using `ctypes.byref(myvar_t)` with `myvar_t` of type `ctypes.c_int`. 

The C type `NULL` will map to None.

The following summarises the translation between Python and C for some common data types: 

| Python casting                            | C type            | Comments                                      |
|-------------------------------------------|-------------------|-----------------------------------------------|
| `None`                                    | `NULL`            |                                               |
| `str(...).encode('ascii')`                | `char*`           |                                               |
| `ctypes.c_int(...)`                       | `int`             | No need to cast                               |
| `ctypes.c_double(...)`                    | `double`          |                                               |
| `(...).ctypes.POINTER(ctypes.c_double)`   | `double*`         | pass a numpy array of type float64            |
| `ctypes.byref(...)`                       | `&`               | pass by reference (suitable for output arguments)                             |      


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


