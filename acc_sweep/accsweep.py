import os.path

from .common import timestamp
from .sweep_directory import SweepDirectory

class ACCSweep(object):
  def __init__(self, root):
    assert os.path.isdir(root), 'No such root directory'
    self.root = root
    self.sweepd = SweepDirectory(self.root)
    self.condor = None

    # stateful variables
    self.current_xname = None
    self.current_job = None

  def _create_xname(self, tag):
    # Note: call this function only once per new experiment, as it
    # captures a timestamp.
    xname = ''
    if tag is not None:
      xname += str(tag) + '-'
    xname += timestamp()
    return xname

  def set_experiment(self, tag=None, template=None):
    self.xname = self._create_xname(tag)
    self.sweepd.set_experiment(self.xname)
    if template is not None:
      self.set_template(template)

  def set_template(self, templatefile):
    self.condor = CondorTemplate(templatefile)
