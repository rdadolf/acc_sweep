import os
import os.path
import tempfile
import distutils.dir_util

from .common import timestamp

class SweepDirectory(object):
  def __init__(self, root):
    assert os.path.exists(root), 'Root directory does not exist'
    self.root = os.path.abspath(root)
    self.expdir = None # No active experiment
    self.jid = 0
    self.jobs = []

  def _jid2pair(self, jid):
    assert jid<256*256, 'Job ID overflow. Too many jobs.'
    prefix = '%02x' % (jid//256)
    suffix = '%02x' % (jid%256)
    return (prefix,suffix)
  def _pair2jid(self, prefix, suffix):
    return int(prefix,16)*256 + int(suffix,16)

  def create_experiment(self, name=None):
    '''Create a new experiment directory.

    If 'name' is not specified, this function will create a new, unique name.
    The names generated are guaranteed to be unique, so it is suggested you
    run in this mode.
    Note that timestamps are calculated from the time this function is called.'''
    tstr = timestamp() 
    self.expdir = os.path.normpath(tempfile.mkdtemp(prefix='x', suffix='-'+tstr,dir=self.root))
    return self.expdir
    
  def set_experiment(self, name):
    self.expdir = os.path.normpath(os.path.join(self.root, name))
    assert os.path.isdir(expdir), 'No such experiment.'
    return self.expdir

  def snapshot(self, source):
    '''Create a static copy of a file or directory.

    Most jobs will want a static copy of whatever code they're running.
    This copies a file or directory into the base of the experiment directory.
    '''

    assert self.expdir is not None, 'Must set an active experiment before modifying one.'

    source = os.path.realpath(source)
    assert os.path.exists(source), 'Source does not exist.'

    # Determine where the source should be copied to.
    # (normpath accounts for trailing /'s)
    name = os.path.split(os.path.normpath(source))[1]
    target = os.path.join(self.expdir, name)

    # Try to catch the situation where the caller has requestsed a snapshot of
    # the target directory. (This will fall into a disk-eating infinite loop
    # otherwise.)
    pfx = os.path.commonprefix([source,target])
    assert pfx!=source, 'Cannot copy a directory into a subdirectory of itself.'
    # The converse (pfx==target) is weird and probably wrong, but it won't
    # break anything.

    # Hand off the copying to a lower-level function.
    # FIXME: we use distutils.dir_util.copy_tree for simplicity
    # FIXME: for exclude paths, we'll need shutil.copytree

    distutils.dir_util.copy_tree(source, target)
    
  def new_job(self):
    assert self.expdir is not None, 'Must set an active experiment before modifying one.'
    jid = self.jid
    self.jid += 1

    # Create new job directory(ies)
    prefix,suffix = self._jid2pair(jid)
    prefix_dir = os.path.join(self.expdir,prefix)
    if not os.path.isdir(prefix_dir):
      os.mkdir(prefix_dir)
    suffix_dir = os.path.join(prefix_dir,suffix)
    assert not os.path.isdir(suffix_dir), 'Error: attempted to overwrite a job directory.'
    os.mkdir(suffix_dir)
    jobdir = os.path.abspath(suffix_dir)

    return jid, jobdir

  def get_job_directory(self, jid):
    return os.path.join(self.expdir, os.path.join(*self._jid2pair(jid)))

