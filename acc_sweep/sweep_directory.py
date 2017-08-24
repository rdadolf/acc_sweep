import os
import os.path
import distutils.dir_util

class SweepDirectory(object):
  def __init__(self, root):
    assert os.path.exists(root), 'Root directory does not exist'
    self.root = os.path.abspath(root)
    self._xpath = None

  def _xpath_from_tag(self, tag):
    s = os.path.join(self.root,str(tag))
    print s
    return s

  def set_experiment(self, tag):
    '''Assign the current experiment and create a directory if necessary.'''
    self._xpath = self._xpath_from_tag(tag)
    if not os.path.exists(self._xpath):
      os.mkdir(self._xpath)
    assert os.path.isdir(self._xpath)
    return self._xpath

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

