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
