import random
import json
from acc_sweep import ACCSweep

noun = ['panda','cowboy','graduate student']
adjective = ['cheery','morose','polydactyl']
adverb = ['happily','loudly','sarcastically']


sweep = ACCSweep(root='/some-shared-mount', condor_file='madlibs.condor')
sweep.create_experiment(tag='madlibs', template='template.condor')
sweep.copy_to_experiment('madlib.py')
sweep.copy_to_experiment('blanks.txt')

for i in xrange(0,20):
  config = {
    'noun': random.choice(noun),
    'adjective': random.choice(adjective),
    'adverb': random.choice(adverb),
  }
  with open('fills.json','w') as f:
    json.dump(config,f)

  job = sweep.create_job()
  sweep.copy_to_job(job,'fills.json')
