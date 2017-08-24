import os.path

from unittest import TestCase
from .test_utils import TempDir

from .accsweep import ACCSweep

class TestACCSweep(TestCase):
  def test_init(self):
    with TempDir() as root:
      ACCSweep(root)

  def test_create_experiment(self):
    with TempDir() as root:
      swp = ACCSweep(root)
      swp.create_experiment(tag='test-experiment')

  def test_create_jobdir(self):
    with TempDir() as root:
      swp = ACCSweep(root)
      swp.create_experiment(tag='test-experient')
      job = swp.create_job()
      assert os.path.isdir(swp.get_job_directory(job)), 'Didnt create job directory 1'
      job = swp.create_job()
      assert os.path.isdir(swp.get_job_directory(job)), 'Didnt create job directory 2'

  def test_job_copy_file(self):
    with TempDir() as root:
      swp = ACCSweep(root)
      swp.create_experiment(tag='test-experient')

      for i in xrange(0,3):
        testf=os.path.join(root,'testfile')
        with open(testf,'w') as f:
          f.write(str(i))
        job = swp.create_job()
        swp.copy_to_job(job,testf)
        jobfile = os.path.join(swp.get_job_directory(job),'testfile')
        assert os.path.isfile(jobfile), 'Didnt copy job file'
        with open(jobfile,'r') as f2:
          assert f2.read().strip()==str(i), 'Jobfile content incorrect'
