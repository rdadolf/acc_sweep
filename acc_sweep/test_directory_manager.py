from functools import reduce
from unittest import TestCase
from .test_utils import TempDir
from .directory_manager import *

import os.path

class TestDirectoryManager(TestCase):

  def test_init(self):
    with TempDir() as d:
      drm = DirectoryManager(d)
      assert drm.root==d, 'Root not set correctly'

  def test_create_experiment_dir(self):
    with TempDir() as d:
      drm = DirectoryManager(d)
      xdir = drm.create_experiment_directory('test-experiment-please-ignore')
      assert os.path.isdir(xdir), 'No experiment directory created.'

  def test_create_job_dir(self):
    with TempDir() as d:
      drm = DirectoryManager(d, job_levels=1, jobs_per_level=16)
      xdir = drm.create_experiment_directory('test-experiment-please-ignore')
      jdir = drm.create_job_directory(0)

      assert os.path.isdir(jdir), 'No job directory created.'
      assert reduce(os.path.join,[xdir,'0'])==jdir, 'Job directory spec mismatch'

  def test_copy_to_experiment(self):
    with TempDir() as d:
      drm = DirectoryManager(d, job_levels=1, jobs_per_level=16)
      xdir = drm.create_experiment_directory('test-experiment-please-ignore')
      testf = os.path.join(d,'testfile')
      open(testf,'w')
      drm.copy_to_experiment(testf)
      assert os.path.isfile(os.path.join(xdir,'testfile')), 'Failed to copy file to job.'
      testd=os.path.join(d,'testdir')
      os.mkdir(testd)
      drm.copy_to_experiment(testd)
      assert os.path.isdir(os.path.join(xdir,'testdir')), 'Failed to copy directory to job.'

  def test_copy_to_job(self):
    with TempDir() as d:
      drm = DirectoryManager(d, job_levels=1, jobs_per_level=16)
      drm.create_experiment_directory('test-experiment-please-ignore')
      jdir = drm.create_job_directory(0)
      testf = os.path.join(d,'testfile')
      open(testf,'w')
      drm.copy_to_job(0,testf)
      assert os.path.isfile(os.path.join(jdir,'testfile')), 'Failed to copy file to job.'
      testd = os.path.join(d,'testdir')
      os.mkdir(testd)
      drm.copy_to_job(0,testd)
      os.system('ls '+jdir)
      assert os.path.isdir(os.path.join(jdir,'testdir')), 'Failed to copy directory to job.'
