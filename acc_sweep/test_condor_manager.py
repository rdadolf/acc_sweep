from functools import reduce
from unittest import TestCase
from .test_utils import TempDir
from .condor_manager import *

import os.path

class TestCondorManager(TestCase):

  def test_init(self):
    with TempDir() as d:
      outfile = os.path.join(d,'out.condor')
      condor = CondorManager(outfile)
      assert os.path.isfile(outfile), 'Never created condor file.'

  def test_set_template(self):
    with TempDir() as d:
      outfile = os.path.join(d,'out.condor')
      templatefile = os.path.join(d,'template.condor')
      with open(templatefile,'w') as f:
        f.write('example=$(accsweep::root)\n\n')
      condor = CondorManager(outfile)
      condor.set_template(templatefile)
      assert 'accsweep' in condor.template, 'condor template read incorrectly'

  def test_emit(self):
    with TempDir() as d:
      outfile = os.path.join(d,'out.condor')
      templatefile = os.path.join(d,'template.condor')
      with open(templatefile,'w') as f:
        f.write('example=$(accsweep::root)\n\n')
      condor = CondorManager(outfile)
      condor.set_template(templatefile)
      condor.substitute_and_emit({'root':'abc123'})
      with open(outfile,'r') as f:
        s=f.read()
      assert 'accsweep' not in s, 'Variable substitution failed in condor template.'
      assert 'abc123' in s, 'Variable substitution failed in condor template.'

  def test_add_job(self):
    with TempDir() as d:
      outfile = os.path.join(d,'out.condor')
      templatefile = os.path.join(d,'template.condor')
      condor = CondorManager(outfile)
      with open(templatefile,'w') as f:
        f.write('example=$(accsweep::root)\n\n')
      condor.set_template(templatefile)
      condor.substitute_and_emit({'root':'abc123'})
      condor.add_job_block(jobdir='def456')
      with open(outfile,'r') as f:
        s=f.read()
      assert 'accsweep' not in s, 'Variable substitution failed in condor template.'
      assert 'abc123' in s, 'Variable substitution failed in condor template.'
      assert 'def456' in s, 'Failed to add job to condor file.'
