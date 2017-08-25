# ACCSweep Example: Madlibs

This example demonstrates passing job information via files constructed for each job.
The script `madlib.py` takes two arguments, a story with blanks and a set of key-value pairs to fill it with.
The invocation for the script is identical for every job:

```
python madlib.py blanks.txt fills.json
```

The sweep file generates a custom `fills.json` file which contains different data for each job.
These files are copied to a shared directory before the jobs are submitted.


This example also contains a custom Docker container.
The image must be built and pushed to the ACC docker registry, but it will be pulled and run automatically by condor.
The build command is the standard docker one:

```
docker build -t <tagname> .
```
