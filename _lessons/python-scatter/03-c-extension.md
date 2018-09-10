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
* how to build the C++ extension

## Why extending Python with C/C++

Python is a highly flexible programming language, which allows you to express concepts succinctly. At some point you will find however that this flexibility comes at a performance cost. Python often runs an order or more slowly than compiled code. Programming languages such as C and C++ are strongly typed and this allows the compiler to optimise code in ways the Python compiler cannot. In Python every object passed to a procedure has to be interrogated, is it a string? what is its lengths? etc. In C/C++ one can pass a pointer and the compiler takes care of the rest. 

## Learn the basics 

Python has a mechanism for calling C/C++ compiled code in a shared library using the `ctypes` module
```
import ctypes
```
Module `ctypes` defines functions and objects, which can be used to encapsulate the arguments passed to C/C++ procedures.  

This involves the following steps:

 1. Open the shared library `mylib = ctypes.CDLL('path-to-shared_library.so')`
 2. Describe the interface. To call the C/C++ function you need to specify argument types and the return type. 
 3. Call the function in the shared library

## Invoking C/C++ using ctypes

## Examples

## Exercises


