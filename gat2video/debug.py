from gat2video import *
import sys
import json


with open(sys.argv[1], 'r') as handle:
    data = json.load(handle)

meta = data["meta"]
steps = data["steps"]

for g in runningGroup(steps):
    viz = g[0]['data']['visual']
    print(f"=== {viz} ===")
    __import__('pprint').pprint(g)
