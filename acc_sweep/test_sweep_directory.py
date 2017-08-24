from unittest import TestCase 
from .test_utils import TempDir
from .sweep_directory import *

import os.path

class TestSweepDirectory(TestCase):
  
  def test_init(self):
    with TempDir() as d:
      swpd = SweepDirectory(d)
      assert swpd.root==d, 'Root not set correctly'

  def test_set_experiment(self):
    with TempDir() as d:
      swpd = SweepDirectory(d)
      xd = swpd.set_experiment('test-experiment-please-ignore')
      assert os.path.isdir(xd), 'No experiment directory created.'

