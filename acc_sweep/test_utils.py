import tempfile
import os.path
import shutil

class TempDir(object):
  def __init__(self, prefix='test_dir_'):
    self.prefix = prefix
  def __enter__(self):
    # default parent directory is /tmp or something system-appropriate
    self.d = os.path.abspath(tempfile.mkdtemp(prefix=self.prefix))
    return self.d
  def __exit__(self, *args):
    shutil.rmtree(self.d)
