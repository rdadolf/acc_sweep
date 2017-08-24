import os
import os.path
import shutil

from .common import timestamp
from .sweep_directory import SweepDirectory
from .condor import CondorTemplate

class ACCJob(object):
  # A wrapper class.
  # It's more natural to call some methods from the job directly, so we provide
  # a thin object to support this.
  def __init__(self, xpath, jid):
    self._xpath = xpath
    self.jid = jid
    self.dir = self._idemp_create_directory()

  def _idemp_create_directory(self):
    assert os.path.isdir(self._xpath), 'Invalid experiment directory: '+str(self._xpath)
    prefix,suffix = os.path.split(self.jid)
    prefix_dir = os.path.join(self._xpath, prefix)
    suffix_dir = os.path.join(prefix_dir, suffix)
    if not os.path.isdir(prefix_dir):
      os.mkdir(prefix_dir)
    if not os.path.isdir(suffix_dir):
      os.mkdir(suffix_dir)
    return suffix_dir

  def copy_file(self, file):
    shutil.copy(file, self.dir)



class ACCSweep(object):
  def __init__(self, root):
    assert os.path.isdir(root), 'No such root directory'
    self.root = root
    self.sweepd = SweepDirectory(self.root)
    self.condor = None

    # stateful variables (things that will/may change over the life of a sweep)
    self.xname = None
    self.xpath = None
    self._jobs = 0 # The total number of jobs in this experiment
    self.jid = None # The two-part hex string job identifier 'xx/xx'
    # note: jid's are contiguous, so self.jid==jobnumber2jid(self._jobs-1)

  def template_variables(self):
    '''Returns a dictionary of variables that are valid to be substituted into
    condor template files.'''
    # Note: these names must be unique across the entire library.
    return {
      'root': self.root,
      'experiment': self.xname,
      'jid': self.jid
    }


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
    self.xpath = self.sweepd.set_experiment(self.xname)
    if template is not None:
      self.set_template(template)

  def set_template(self, templatefile):
    self.condor = CondorTemplate(templatefile)

  def _jobnumber2jid(self, jobnumber):
    prefix = '%02x' % (jobnumber//256)
    suffix = '%02x' % (jobnumber%256)
    return os.path.join(prefix,suffix)

  def _jid2jobnum(self, jid):
    return int(prefix,16)*256 + int(suffix,16)

  def create_job(self):
    assert self.xpath is not None, 'No experiment set.'
    assert self._jobs<256*256, 'Overflow: too many jobs'
    self.jid = self._jobnumber2jid(self._jobs)
    self._jobs += 1

    return ACCJob(self.xpath, self.jid)

  def queue(self, job):
    pass
    #self.condor.?
