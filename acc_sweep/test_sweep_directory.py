from unittest import TestCase 
from .sweep_directory import *
import tempfile
import os.path
import shutil

class TempDir(object):
  def __init__(self, prefix='test_dir_'):
    self.prefix = prefix
  def __enter__(self):
    # default parent directory is /tmp or something system-appropriate
    self.d = os.path.abspath(tempfile.mkdtemp(prefix=self.prefix))
    return self.d
  def __exit__(self, *args):
    shutil.rmtree(self.d)

class TestSweepDirectory(TestCase):
  
  def test_init(self):
    with TempDir() as d:
      swpd = SweepDirectory(d)
      assert swpd.root==d, 'Root not set correctly'

  def test_create_experiment(self):
    with TempDir() as d:
      swpd = SweepDirectory(d)
      xd = swpd.create_experiment()
      assert os.path.isdir(xd), 'No experiment directory created.'

  def test_new_job(self):
    with TempDir() as d:
      swpd = SweepDirectory(d)
      xd = swpd.create_experiment()
      jobdir = swpd.new_job()
      assert os.path.isdir(jobdir)
