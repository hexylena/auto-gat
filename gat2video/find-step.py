#!/usr/bin/env python3
import json
import sys
import subprocess
import os
import video_extract_script
import urllib.request

DIR = os.path.dirname(os.path.realpath(__file__))
GIT_GAT = os.path.expanduser('~/galaxy')

# Eventually support all
SUPPORTED_TUTORIALS = ['ansible-galaxy', 'tus', 'singularity', 'tool-management', 'cvmfs', 'data-library', 'connect-to-compute-cluster', 'job-destinations', 'pulsar', 'gxadmin', 'monitoring', 'tiaas', 'reports', 'ftp']
tuts_with_steps = {x: (f'step-{idx if idx != 4 else 3}', f'step-{idx + 1}') for (idx, x) in enumerate(SUPPORTED_TUTORIALS)}

tutorial = sys.argv[1]
if tutorial != 'cvmfs':
    print("unsupported")
    sys.exit(1)

bounds = tuts_with_steps[tutorial]
print(bounds[0])
print(bounds[1])
