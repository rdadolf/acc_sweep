from acc_sweep import ACCSweep

sweep = ACCSweep('/some-shared-mount')
sweep.create_experiment('prime-factors','template.condor')

sweep.copy_to_experiment('./libfactor')
sweep.copy_to_experiment('./run.py')

for i in xrange(0,100):
  job_id = sweep.create_job(
    arguments=str(i)
  )
