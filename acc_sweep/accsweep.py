import os
import os.path

from .common import timestamp
from .directory_manager import DirectoryManager
from .condor_manager import CondorManager

class ACCSweep(object):
  def __init__(self, root, condor_file='accsweep.condor'):
    assert os.path.isdir(root), 'No such root directory'
    self.root = os.path.abspath(root)
    self.drm = DirectoryManager(self.root, )
    self.condor = CondorManager(condor_file)

    # stateful variables (things that will/may change over the life of a sweep)
    self.xname = None
    self.xpath = None
    self.jobs = 0

  @property
  def template_variables(self):
    '''Returns a dictionary of variables that are valid to be substituted into
    condor template files.'''
    # Note: these names must be unique across the entire library.
    return {
      'root': self.root,
      'experiment_dir': self.xpath,
    }

  def _create_xname(self, tag):
    # Note: call this function only once per new experiment, as it
    # captures a timestamp.
    xname = ''
    if tag is not None:
      xname += str(tag) + '-'
    xname += timestamp()
    return xname

  def create_experiment(self, tag, template):
    '''Create a new sweep experiment and its supporting directories and files.

     - tag: a descriptive identifier for this experiment. Need not be unique,
            as a timestamp will be appended.
     - template: a condor file with experiment-wide information.'''
    self.xname = self._create_xname(tag)
    self.xpath = self.drm.create_experiment_directory(self.xname)
      
    self.condor.set_template(template)
    self.condor.substitute_and_emit(self.template_variables)

  def copy_to_experiment(self, file_or_directory):
    assert os.path.isdir(self.xpath), 'Create an experiment before copying files to it.'
    self.drm.copy_to_experiment(file_or_directory)

  def create_job(self, executable=None, arguments=None):
    jobid = self.jobs
    self.jobs += 1

    self.drm.create_job_directory(jobid)

    self.condor.add_job_block(
      jobdir=self.get_job_directory(jobid),
      executable=executable,
      arguments=arguments
    )

    return jobid

  def get_job_directory(self, jobid):
    return self.drm.path_from_jobid(jobid)

  def copy_to_job(self, jobid, file_or_directory):
    self.drm.copy_to_job(jobid,file_or_directory)
