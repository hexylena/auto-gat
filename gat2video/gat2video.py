#!/usr/bin/env python3
import json
import sys
import subprocess
import os
import video_extract_script
import urllib.request

DIR = os.path.dirname(os.path.realpath(__file__))

# Eventually support all
SUPPORTED_TUTORIALS = ['ansible-galaxy', 'tus', 'singularity', 'tool-management', 'cvmfs', 'data-library', 'connect-to-compute-cluster', 'job-destinations', 'pulsar', 'gxadmin', 'monitoring', 'tiaas', 'reports', 'ftp']

tuts_with_steps = {x: (f'step-{idx if idx != 4 else 3}', f'step-{idx + 1}') for (idx, x) in enumerate(SUPPORTED_TUTORIALS)}

tutorial = sys.argv[1]
if tutorial != 'cvmfs':
    print("unsupported")
    sys.exit(1)

bounds = tuts_with_steps[tutorial]

url = f'https://raw.githubusercontent.com/galaxyproject/training-material/main/topics/admin/tutorials/{tutorial}/tutorial.md'
response = urllib.request.urlopen(url).read().decode('utf-8').split('\n')
lines = [x + '\n' for x in response]

script = video_extract_script.process(lines)
with open(f'{tutorial}.script', 'w') as handle:
    json.dump(script, handle)

# Checkout the right directory
subprocess.check_call([
    'git', 'checkout', bounds[0]
], cwd='/home/ubuntu/galaxy/')
# Install missing deps
subprocess.check_call([
    'ansible-galaxy', 'install', '-r', 'requirements.yml', '-p', 'roles'
], cwd='/home/ubuntu/galaxy/')
# And self signed certs
subprocess.check_call([
    'ansible-galaxy', 'install', 'galaxyproject.self_signed_certs'
], cwd='/home/ubuntu/galaxy/')

# Run playbook up to there.
subprocess.check_call([
    'ansible-playbook', 'galaxy.yml', '-e', '@~/.extra.yml'
], cwd='/home/ubuntu/galaxy/')


subprocess.check_call(['python3', os.path.join(DIR, 'video-builder.py'), f'{tutorial}.script', tutorial])
