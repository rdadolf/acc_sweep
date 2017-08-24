import os.path

class CondorManager(object):
  def __init__(self, outputfile):
    self.ofile = open(outputfile, 'w')
    self.template = None

  def set_template(self, templatefile):
    assert os.path.isfile(templatefile), 'Invalid template file: '+str(templatefile)
    with open(templatefile) as f:
      self.template = f.read()

  def substitute_and_emit(self, kv):
    assert self.template is not None, 'Set a template before using it.'
    s = self.template
    for k,v in kv.items():
      s = s.replace('accsweep::'+k,v)
    print s
    self.ofile.write(s)
    self.ofile.write('\n##### Begin Job Blocks #####\n\n')
    self.ofile.flush()

  def add_job_block(self, jobdir, executable=None, arguments=None):
    self.ofile.write('initialdir='+jobdir+'\n')
    if executable is not None:
      self.ofile.write('executable='+executable+'\n')
    if arguments is not None:
      self.ofile.write('arguments='+arguments+'\n')
    self.ofile.write('queue\n\n')
    self.ofile.flush()
