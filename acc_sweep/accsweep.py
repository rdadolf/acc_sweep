import os
import os.path

from .common import timestamp
from .directory_manager import DirectoryManager
from .condor_template import CondorTemplate

class ACCSweep(object):
  def __init__(self, root):
    assert os.path.isdir(root), 'No such root directory'
    self.root = root
    self.drm = DirectoryManager(self.root, )
    self.condor = None

    # stateful variables (things that will/may change over the life of a sweep)
    self.xname = None
    self.xpath = None
    self.jobs = 0

  def template_variables(self):
    '''Returns a dictionary of variables that are valid to be substituted into
    condor template files.'''
    # Note: these names must be unique across the entire library.
    return {
      'root': self.root,
      'experiment': self.xname,
      'experiment_dir': self.xname,
    }

  def _create_xname(self, tag):
    # Note: call this function only once per new experiment, as it
    # captures a timestamp.
    xname = ''
    if tag is not None:
      xname += str(tag) + '-'
    xname += timestamp()
    return xname

  def create_experiment(self, tag=None, template=None):
    self.xname = self._create_xname(tag)
    self.xpath = self.drm.create_experiment_directory(self.xname)
    if template is not None:
      self.set_template(template)

  def copy_to_experiment(self, file_or_directory):
    assert os.path.isdir(self.xpath), 'Create an experiment before copying files to it.'
    self.drm.copy_to_experiment(file_or_directory)


  def set_template(self, templatefile):
    self.condor = CondorTemplate(templatefile)

  def create_job(self, executable=None, arguments=None):
    jobid = self.jobs
    self.jobs += 1

    self.drm.create_job_directory(jobid)

    #condor.?

    return jobid

  def get_job_directory(self, jobid):
    return self.drm.path_from_jobid(jobid)

  def copy_to_job(self, jobid, file_or_directory):
    self.drm.copy_to_job(jobid,file_or_directory)
