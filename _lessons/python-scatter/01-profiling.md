---
layout: post
title: Introduction to profiling
permalink: /python-scatter/profiling
chapter: python-scatter
---

## Objectives

You will:

* understand what profiling is
* why it is important to profile code
* know how to choose your test case

## What is profiling

Profiling helps you understand how much time is spent in different parts of 
your code when it runs. These can be functions, loops, or source code lines.

Profiling information is obtained by using profiling tools. More on how to apply
such tools at:
 * [Profiling with CProfile](profiling-cprofile)
 * [Profiling with MAP](profiling-map)

## Why should I profile my code?

Obtaining profiling information is a critical step before attempting to optimise code, as it
enables you to focus your efforts on improving the parts of the code that
will result in the biggest gains in performance.

## Choose your test case wisely

Due to the possible overhead from profiling tools, the code could run slower than normal. 
Therefore it is advisable to choose a small but representative test case to profile. That is,
something that is representative of what you eventually want to run but completes in a short time.

The run time should not be too short, however, as this could make profiling results unreliable. In general, the execution should take at least 10 seconds.

**Note:** keep in mind that with shortened computation time, the initialisation and finalisation steps may become dominant.
