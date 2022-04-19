#!/usr/bin/env python
import sys
import json
import argparse


parser = argparse.ArgumentParser(description='Concatenate multiple asciicasts')
parser.add_argument('casts', nargs='+', type=argparse.FileType('r'))
parser.add_argument('--title', type=str, help="Optional override to the title")
args = parser.parse_args()


def castId(filename: str) -> int:
    return int(filename.split('-')[-1][:-5])


casts = sorted(args.casts, key=lambda x: castId(x.name))
offset = 0
for idx, cast in enumerate(casts):
    lines = cast.readlines()
    for line in lines:
        data = json.loads(line)
        if isinstance(data, dict):
            if idx > 0:
                continue
            elif idx == 0 and args.title:
                data['title'] = args.title
        else:
            data[0] += offset

        print(json.dumps(data))

    print(json.dumps([
        data[0] + 0.1, # Get last line time and add a bit
        "o",
        "\u001b[0m" # ANSI reset
    ]))
    print(json.dumps([
        data[0] + 0.2,
        "o",
        "\r\n"
    ]))
    print(json.dumps([
        data[0] + 0.3,
        "o",
        "\u001b[H\u001b[2J\u001b[3J" # Magic
    ]))

    offset += json.loads(lines[-1])[0]
