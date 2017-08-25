import sys
import re
import json

if __name__=='__main__':
  pattern_file = sys.argv[1]
  fills_file = sys.argv[2]

  with open(pattern_file) as f:
    pattern = f.read()
  with open(fills_file) as f:
    fills = json.load(f)

  story = re.sub('__(\w+)__', lambda m: fills[m.group(1)], pattern)

  print story
