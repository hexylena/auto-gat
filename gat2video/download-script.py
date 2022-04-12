#!/usr/bin/env python3
import json
import sys
import subprocess
import os
import video_extract_script
import urllib.request

DIR = os.path.dirname(os.path.realpath(__file__))
GIT_GAT = os.path.expanduser('~/galaxy')

tutorial = sys.argv[1]
if tutorial != 'cvmfs':
    print("unsupported")
    sys.exit(1)

url = f'https://raw.githubusercontent.com/galaxyproject/training-material/main/topics/admin/tutorials/{tutorial}/tutorial.md'
response = urllib.request.urlopen(url).read().decode('utf-8').split('\n')
lines = [x + '\n' for x in response]

script = video_extract_script.process(lines)
with open(f'{tutorial}.script', 'w') as handle:
    json.dump(script, handle)
