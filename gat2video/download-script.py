#!/usr/bin/env python3
import json
import sys
import subprocess
import os
import video_extract_script
import urllib.request
import argparse

DIR = os.path.dirname(os.path.realpath(__file__))
GIT_GAT = os.path.expanduser('~/galaxy')

parser = argparse.ArgumentParser(description='Download and generate a script')
parser.add_argument('tutorial')
parser.add_argument('--branch', default='main')
parser.add_argument('--markdown', type=argparse.FileType('r'), help="Load from a markdown file rather than a URL")
args = parser.parse_args()

if args.tutorial != 'cvmfs':
    print("unsupported")
    sys.exit(1)

# url = f'https://cdn.jsdelivr.net/gh/galaxyproject/training-material@{args.branch}/topics/admin/tutorials/{args.tutorial}/tutorial.md'
if args.markdown:
    response = args.markdown.read().split('\n')
else:
    url = f'https://raw.githubusercontent.com/galaxyproject/training-material/{args.branch}/topics/admin/tutorials/{args.tutorial}/tutorial.md'
    print(url)
    response = urllib.request.urlopen(url).read().decode('utf-8').split('\n')

lines = [x + '\n' for x in response]

script = video_extract_script.process(lines)
with open(f'{args.tutorial}.script', 'w') as handle:
    json.dump(script, handle)
