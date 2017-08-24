import errno
from functools import reduce
import math
import os
import os.path
import shutil

class DirectoryManager(object):
  def __init__(self, root, job_levels=2, jobs_per_level=256):
    assert os.path.exists(root), 'Root directory does not exist'
    self.root = os.path.abspath(root)
    self.xpath = None
  
    self.job_levels = job_levels
    self.jobs_per_level = jobs_per_level
    self.max_jobs = jobs_per_level**job_levels
    self._hex_format='%0'+str(int(math.ceil(math.log(jobs_per_level,16))))+'x'

  def create_experiment_directory(self, tag):
    '''Assign the current experiment and create a directory if necessary.'''
    self.xpath = os.path.join(self.root, str(tag))
    if not os.path.exists(self.xpath):
      os.mkdir(self.xpath)
    assert os.path.isdir(self.xpath)
    return self.xpath

  def copy_to_x(self, source_file_or_directory, target_directory):
    source = os.path.realpath(source_file_or_directory)
    target = os.path.realpath(target_directory)
    assert os.path.exists(source), 'Source does not exist: '+str(source)
    assert os.path.isdir(target), 'Target directory does not exist: '+str(target)

    # Try to catch the situation where the caller is copying a directory 
    # containing the experiment directory. (This will fall into a disk-eating
    # infinite loop.)
    pfx = os.path.commonprefix([source,target])
    assert pfx!=source, 'ERROR: Attempted to copy directory into itself. This would have recursed until stack space ran out, consuming disk space rapidly in the process. Invalid directory: '+str(source)
    # The converse is weird, but it won't break anything.

    if os.path.isdir(source):
      # copytree requires the actual name, not just the target location
      dirname = os.path.split(os.path.normpath(source))[1]
      shutil.copytree(source, os.path.join(target,dirname))
    else:
      shutil.copy(source, target)

  def copy_to_experiment(self, file_or_directory):
    assert os.path.isdir(self.xpath), 'Set an active experiment before copying files.'
    self.copy_to_x(file_or_directory, self.xpath)

  def dirchain_from_jobid(self, jobid):
    subdirs = []
    j = jobid
    # We actually construct this backwards, because it's easier
    for _ in xrange(0,self.job_levels):
      subdir = self._hex_format % (j%self.jobs_per_level)
      subdirs.insert(0,subdir)
      j //= self.jobs_per_level
    return subdirs

  def path_from_jobid(self, jobid):
    return reduce(os.path.join, [self.xpath]+self.dirchain_from_jobid(jobid))

  def create_job_directory(self, jobid):
    assert os.path.isdir(self.xpath), 'Invalid experiment directory: '+str(self._xpath)
    jobdir = self.path_from_jobid(jobid)
    os.makedirs(jobdir) # will error if leaf dir exists, but not intermediates
    return jobdir

  def copy_to_job(self, jobid, file_or_directory):
    jobdir = self.path_from_jobid(jobid)
    assert os.path.isdir(jobdir), 'Invalid job directory: '+str(jobdir)
    self.copy_to_x(file_or_directory, jobdir)
