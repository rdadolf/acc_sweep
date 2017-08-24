import os.path

from unittest import TestCase
from .test_utils import TempDir

from .accsweep import ACCSweep

class TestACCSweep(TestCase):
  def test_init(self):
    with TempDir() as root:
      ACCSweep(root)

  def test_set_experiment(self):
    with TempDir() as root:
      swp = ACCSweep(root)
      swp.set_experiment(tag='test-experiment')

  def test_create_jobdir(self):
    with TempDir() as root:
      swp = ACCSweep(root)
      swp.set_experiment(tag='test-experient')
      job = swp.create_job()
      assert os.path.isdir(job.dir), 'Didnt create job directory 1'
      job = swp.create_job()
      assert os.path.isdir(job.dir), 'Didnt create job directory 2'

  def test_job_copy_file(self):
    with TempDir() as root:
      swp = ACCSweep(root)
      swp.set_experiment(tag='test-experient')

      for i in xrange(0,3):
        with open('testfile','w') as f:
          f.write(str(i))
        job = swp.create_job()
        job.copy_file('testfile')
        jobfile = os.path.join(job.dir,'testfile')
        assert os.path.isfile(jobfile), 'Didnt copy job file'
        with open(jobfile,'r') as f2:
          assert f2.read().strip()==str(i), 'Jobfile content incorrect'
