#!/usr/bin/env python
import os
import shutil
import glob
import json
import subprocess

def ffprobe(fn):
    return json.loads(subprocess.check_output(['ffprobe', '-hide_banner', '-loglevel', 'warning', '-show_format', '-print_format', 'json', '-i', fn]).decode('utf-8'))

def ffs(v_in, output, offset):
    if os.path.exists(output):
        return

    if offset == 0:
        shutil.copy(v_in, output)
    else:
        subprocess.check_call([
            'ffs', '-i', v_in, '-o', output, '--apply-offset-seconds',  str(offset)
        ])

cumulative = 0
resynced = []
for video in sorted(glob.glob('video-[0-9].mp4') + glob.glob('video-[0-9][0-9].mp4'), key=lambda x: int(x.split('-')[1][0:-4])):
    duration = ffprobe(video)['format']['duration']

    in_subs = video.replace('.mp4', '.en.srt')
    out_subs = video.replace('.mp4', '.resync.srt')
    ffs(in_subs, out_subs, cumulative)
    resynced.append(out_subs)
    cumulative += float(duration)


def parseSrt(fn, offset=0):
    with open(fn, 'r') as handle:
        sections = handle.read().strip().split("\n\n")
        for section in sections:
            data = section.split("\n")
            yield (
                int(data[0]) + offset,
                data[1],
                data[2:]
            )


final_srt = []
offset = 0
for x in resynced:
    final_srt += parseSrt(x, offset)
    offset = final_srt[-1][0]
    print(offset)

with open('final.srt', 'w') as handle:
    for x in final_srt:
        handle.write(str(x[0]) + "\n")
        handle.write(x[1] + "\n")
        handle.write("\n".join(x[2]) + "\n\n")
