# ACCSweep Example: Factor

This worked example demonstrates passing job configuration information
via the command line:

```
  ./run.py 1
  ./run.py 2
  ...
```

We have a python library `libfactor` and a driver script `run.py`, which computes the prime factors of an integer passed on the command line.
The goal is to prime-factorize the first hundred integers.
The condor template file sets up the basic environment, including a path adjustment to find the `libfactor` package.
The `sweep.py` file actually sets up the 100 jobs. These are then submitted manually using `condor_q accsweep.condor` (where the latter filename is the default name for the condor job file).
