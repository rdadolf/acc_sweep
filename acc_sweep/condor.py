import os.path

class CondorTemplate(object):
  def __init__(self, templatefile):
    assert os.path.isfile(templatefile), 'Invalid template file: '+str(templatefile)
    self.tfile = templatefile


